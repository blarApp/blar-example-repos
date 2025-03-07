import logging

from celery import chain
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.response import Response
from rest_framework.views import APIView

from blar.agents.custom_agents.agentic.PullRequest import PullRequestWorkflow
from blar.agents.custom_agents.agentic.WikiRagReviewer import WikiRagReviewerWorkflow
from blar.agents.custom_agents.agentic.WikiWriter import WikiWriterWorkFlow
from blar.agents.helpers import check_user_company
from blar.agents.models import (
    ENVIRONMENT,
    ChatRoom,
    Message,
    MessageFeedback,
    MessageTag,
)
from blar.agents.selectors import (
    get_chat_room,
    get_chat_room_company,
    get_chat_room_messages,
    list_chat_rooms,
)
from blar.agents.serializers import InputTagSerializer
from blar.agents.services import (
    create_chat,
    create_message_tag,
    get_or_create_chat,
    retrieve_pr_messages,
    save_message,
    soft_delete_chat,
)
from blar.agents.tasks import execute_code_error_agent
from blar.api.mixins import ApiAuthMixin
from blar.api.pagination import LimitOffsetPagination, get_paginated_response
from blar.graph_db_manager.neo4j_manager import Neo4jManager
from blar.integrations.github.adapters.primary.pull_request_dto import PullRequestDTO
from blar.integrations.github.api_client import GitHubAPIClient
from blar.integrations.github.services import (
    update_or_create_pull_request,
)
from blar.integrations.models import CodeError, PullRequest
from blar.integrations.selectors import get_pr
from blar.repo_graph.apis.github_repo.selectors import get_repo
from blar.repo_graph.services import delete_pr_repo_graph
from blar.repo_graph.tasks import add_repo_diff_task
from blar.users.models import BaseUser
from blar.users.serializers import UserSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)


class MessageTagApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        message = serializers.CharField()
        tags = InputTagSerializer(many=True)
        chat_room_id = serializers.CharField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class MessageSerializer(serializers.ModelSerializer):
            user = UserSerializer()

            class Meta:
                model = Message
                exclude = ["chat_room"]

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Process valid data
        data = serializer.validated_data
        if "chat_room_id" in data and data["chat_room_id"]:
            chat_room = get_chat_room(id=data["chat_room_id"])
        else:
            chat_room = create_chat(
                company=request.user.company,
                user=request.user,
                agent=data.get("agent"),
                message=data["message"],
                environment=ENVIRONMENT.MAIN.value,
            )

        message = save_message(chat_room=chat_room, message=data["message"], user=request.user)

        for tag in data["tags"]:
            user = BaseUser.objects.get(id=tag["id"])
            create_message_tag(message=message, user=user)

        # Serialize the created message using MessageSerializer
        message_serializer = self.OutputSerializer.MessageSerializer(message)

        return Response(message_serializer.data, status=status.HTTP_201_CREATED)


class ChatRoomApi(ApiAuthMixin, APIView):
    content_negotiation_class = IgnoreClientContentNegotiation

    class PostInputSerializer(serializers.Serializer):
        agent = serializers.ChoiceField(
            choices=["debugger", "cyber_security", "optimizer", "general", "pull_request_chat"]
        )
        node_ids = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=False)

        def validate(self, data):
            if "chat_room_id" in data:
                data.pop("node_ids", None)
                data.pop("agent", None)
            else:
                if "node_ids" not in data:
                    raise serializers.ValidationError("node_id is required if chat_room_id is not provided.")
                if "agent" not in data:
                    raise serializers.ValidationError("agent is required if chat_room_id is not provided.")
            return data

    class PostOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ChatRoom
            fields = [
                "id",
                "name",
                "agent",
                "environment",
            ]

    def delete(self, request, id):
        company = request.user.company
        chat_room = get_chat_room_company(id=id, company=company)

        soft_delete_chat(chat_room=chat_room)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat_room = create_chat(
            company=request.user.company,
            user=request.user,
            agent=serializer.validated_data["agent"],
            environment=ENVIRONMENT.MAIN.value,
        )

        return Response(
            self.PostOutputSerializer(chat_room).data,
            status=status.HTTP_201_CREATED,
        )

    class ChatRoomSerializer(serializers.ModelSerializer):
        trigger_type = serializers.CharField(source="trigger_type.model")
        trigger_id = serializers.CharField()
        trigger = serializers.SerializerMethodField()
        company_name = serializers.CharField(source="company.name")
        created_at = serializers.DateTimeField()
        agent = serializers.CharField()
        name = serializers.CharField()
        messages = serializers.SerializerMethodField()
        environment = serializers.CharField()

        class Meta:
            model = ChatRoom
            fields = [
                "id",
                "trigger_type",
                "trigger_id",
                "trigger",
                "company_name",
                "agent",
                "name",
                "created_at",
                "messages",
                "task_state",
                "environment",
            ]

        class MessageSerializer(serializers.ModelSerializer):
            user = UserSerializer()
            user_thumbs_up = serializers.SerializerMethodField()
            user_thumbs_down = serializers.SerializerMethodField()

            class Meta:
                model = Message
                fields = [
                    "id",
                    "message",
                    "is_blar",
                    "created_at",
                    "user",
                    "user_thumbs_up",
                    "user_thumbs_down",
                ]

            def get_user_thumbs_up(self, obj):
                return obj.user_thumbs_up

            def get_user_thumbs_down(self, obj):
                return obj.user_thumbs_down

        def get_messages(self, obj):
            messages = obj.messages.order_by("created_at")
            return self.MessageSerializer(messages, many=True).data

        def get_trigger(self, obj):
            if isinstance(obj.trigger, BaseUser):
                return {
                    "email": obj.trigger.email,
                    "first_name": obj.trigger.first_name,
                    "last_name": obj.trigger.last_name,
                    "color": obj.trigger.color,
                    "secondary_color": obj.trigger.secondary_color,
                }
            elif isinstance(obj.trigger, CodeError):
                return {
                    "error_id": obj.trigger.error_id,
                    "source": obj.trigger.source,
                    "priority": obj.trigger.priority,
                    "state": obj.trigger.state,
                }

            return {}

    def get(self, request, id):
        company = request.user.company

        try:
            chat_room = get_chat_room_messages(company=company, chat_id=id, request=request)
        except Http404:
            return Response(
                {"error": "Chat room not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        messagesSerializer = self.ChatRoomSerializer(chat_room)

        return Response(
            messagesSerializer.data,
            status=status.HTTP_200_OK,
        )


class ChatRoomInformationApi(ApiAuthMixin, APIView):
    content_negotiation_class = IgnoreClientContentNegotiation

    class GetOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ChatRoom
            fields = ["id", "name", "agent", "environment"]

    def get(self, request, id):
        company = request.user.company

        try:
            chat_room = get_chat_room_company(id=id, company=company)
        except Http404:
            return Response(
                {"error": "Chat room not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            self.GetOutputSerializer(chat_room).data,
            status=status.HTTP_200_OK,
        )


class ChatRoomsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20

    class FilterSerializer(serializers.Serializer):
        trigger_type = serializers.ChoiceField(
            choices=[("baseuser", "BaseUser"), ("codeerror", "CodeError"), ("pullrequest", "PullRequest")],
            required=False,
        )
        name = serializers.CharField(required=False, help_text="Filter by name with case-insensitive containment")

        # Filters for CodeError fields when the trigger is CodeError
        code_error_source = serializers.CharField(
            required=False,
            help_text="Filter by source with case-insensitive containment",
        )
        code_error_priority = serializers.ListField(
            child=serializers.ChoiceField(choices=CodeError.PRIORITY_CHOICES),
            required=False,
            help_text="Filter by priority level (multiple values allowed)",
        )
        code_error_state = serializers.ListField(
            child=serializers.ChoiceField(choices=CodeError.STATE_CHOICES),
            required=False,
            help_text="Filter by state (multiple values allowed)",
        )
        code_error_assigned_to = serializers.ChoiceField(
            choices=["me", "unassigned", "all"],
            required=False,
            help_text="Filter by assigned_to (me, unassigned, all)",
        )

    class OutputSerializer(serializers.ModelSerializer):
        trigger_type = serializers.CharField(source="trigger_type.model")
        trigger_id = serializers.CharField()
        trigger = serializers.SerializerMethodField()
        company_name = serializers.CharField(source="company.name")
        created_at = serializers.DateTimeField()
        agent = serializers.CharField()
        name = serializers.CharField()
        users = serializers.SerializerMethodField()
        has_unread_messages = serializers.BooleanField()
        last_message_time = serializers.DateTimeField()

        class Meta:
            model = ChatRoom
            fields = [
                "id",
                "trigger_type",
                "trigger_id",
                "trigger",
                "company_name",
                "created_at",
                "agent",
                "name",
                "created_at",
                "users",
                "has_unread_messages",
                "last_message_time",
            ]

        def get_trigger(self, obj):
            # Customize this method based on the `trigger` content type (BaseUser, CodeError, etc.)
            if isinstance(obj.trigger, BaseUser):
                return {"email": obj.trigger.email}
            elif isinstance(obj.trigger, CodeError):
                assigned_to = obj.trigger.assigned_to

                return {
                    "error_id": obj.trigger.error_id,
                    "source": obj.trigger.source,
                    "priority": obj.trigger.priority,
                    "state": obj.trigger.state,
                    "assigned_to": {
                        "id": assigned_to.id if assigned_to else None,
                        "email": assigned_to.email if assigned_to else None,
                        "first_name": assigned_to.first_name if assigned_to else None,
                        "last_name": assigned_to.last_name if assigned_to else None,
                        "color": assigned_to.color if assigned_to else None,
                        "secondary_color": (assigned_to.secondary_color if assigned_to else None),
                    },
                }
            elif isinstance(obj.trigger, PullRequest):
                return {
                    "pull_request_id": obj.trigger.id,
                    "title": obj.trigger.title,
                }
            return None

        def get_users(self, obj):
            users = set()
            for message in obj.messages.all():
                if message.user:
                    users.add(message.user)
                for tag in message.tags.all():
                    if tag.user:
                        users.add(tag.user)
            return [
                {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "color": user.color,
                    "secondary_color": user.secondary_color,
                }
                for user in users
            ]

    def get(self, request):
        # Make sure the filters are valid, if passed
        company = request.user.company
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        chat_rooms = list_chat_rooms(company=company, filters=filters_serializer.validated_data, request=request)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=chat_rooms,
            request=request,
            view=self,
        )


class ExecuteCodeErrorAgentApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        error_id = request.data.get("error_id")
        code_error = CodeError.objects.get(id=error_id)
        execute_code_error_agent(code_error=code_error)

        return Response(
            status=status.HTTP_201_CREATED,
        )


class MarkChatAsReadApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        chat_room_id = serializers.CharField()

    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat_room_id = serializer.validated_data["chat_room_id"]
        user = request.user

        # Update the MessageTag instances
        MessageTag.objects.filter(message__chat_room_id=chat_room_id, user=user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )

        return Response({"detail": "Messages marked as read."}, status=status.HTTP_200_OK)


class IncrementThumbsUpApi(ApiAuthMixin, APIView):
    def post(self, request, message_id, *args, **kwargs):
        message = get_object_or_404(Message, id=message_id)
        check_user_company(user=request.user, message=message)
        if not message.is_blar:
            raise ValidationError("Thumbs up can only be submitted for 'is_blar' messages.")

        feedback, _ = MessageFeedback.objects.get_or_create(message=message, user=request.user)
        if feedback.thumbs_down:
            feedback.thumbs_down = False
        feedback.thumbs_up = True
        feedback.save()
        return Response({"created"}, status=status.HTTP_201_CREATED)


class IncrementThumbsDownApi(ApiAuthMixin, APIView):
    def post(self, request, message_id, *args, **kwargs):
        message = get_object_or_404(Message, id=message_id)
        check_user_company(user=request.user, message=message)
        if not message.is_blar:
            raise ValidationError("Thumbs down can only be submitted for 'is_blar' messages.")

        feedback, _ = MessageFeedback.objects.get_or_create(message=message, user=request.user)
        if feedback.thumbs_up:
            feedback.thumbs_up = False
        feedback.thumbs_down = True
        feedback.save()
        return Response({"created"}, status=status.HTTP_201_CREATED)


class SubmitFeedbackApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        feedback_text = serializers.CharField(max_length=500)

    def post(self, request, message_id, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback_text = serializer.validated_data["feedback_text"]
        message = get_object_or_404(Message, id=message_id)
        if not message.is_blar:
            raise ValidationError("Feedback can only be submitted for 'is_blar' messages.")
        check_user_company(user=request.user, message=message)

        feedback, _ = MessageFeedback.objects.get_or_create(message=message, user=request.user)
        feedback.feedback_text = feedback_text
        feedback.save()
        return Response({"feedback_text": feedback.feedback_text}, status=status.HTTP_200_OK)


class WikiRagReviewerAgentApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        chat_room_id = serializers.CharField(required=False)
        message = serializers.CharField()
        tags = serializers.ListField(child=serializers.DictField(), required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Message
            fields = "__all__"

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = request.user.company
        data = serializer.validated_data
        company_id = str(company.id)
        wiki_rag_reviewer_graph = WikiRagReviewerWorkflow(company_id=company_id)
        wiki_rag_reviewer_graph_initial_state = {"company_context": [], "query": data["message"]}
        wiki_app = wiki_rag_reviewer_graph.build_workflow()
        report = wiki_app.invoke(wiki_rag_reviewer_graph_initial_state)
        return Response(report, status=status.HTTP_201_CREATED)


class PullRequestReportApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        company_id = serializers.CharField(max_length=255)
        pull_request_number = serializers.IntegerField()
        repo_id = serializers.CharField(max_length=255)
        delete_graph = serializers.BooleanField(required=False, default=False)
        create_graph = serializers.BooleanField(required=False, default=False)

    def post(self, request, *args, **kwargs):
        logger.info(f"Starting PullRequestReportApi processing with data: {request.data}")

        data = {
            "company_id": str(request.user.company.id),
            "pull_request_number": request.data.get("pull_request_number"),
            "repo_id": request.data.get("repo_id"),
            "delete_graph": request.data.get("delete_graph", False),
            "create_graph": request.data.get("create_graph", False),
        }

        serializer = self.InputSerializer(data=data)
        if not serializer.is_valid():
            logger.error(f"Invalid input data: {serializer.errors}")
            return Response(
                {"error": "Invalid request data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        logger.info(f"Data validated successfully: {data}")

        try:
            repo_db = get_repo(repo_id=data['repo_id'], company_id=data['company_id'])
            logger.info(f"Retrieved repo: {repo_db.name}")

            pull_request = get_pr(
                pr_number=data['pull_request_number'],
                company_id=data['company_id'],
                repo=repo_db,
            )

            if pull_request is None:
                logger.info(f"PR not found in database, fetching from GitHub: PR #{data['pull_request_number']}")
                github_client = GitHubAPIClient.create(company=repo_db.company)
                pr_response = github_client.get(
                    f"/repos/{repo_db.name}/pulls/{data['pull_request_number']}"
                )
                if pr_response.status_code == 200:
                    logger.info("Successfully retrieved PR data from GitHub")
                    pr_data = pr_response.json()
                    adapted_pr_data = {
                        "branch_name": pr_data['base']['ref'],
                        "pull_request_number": pr_data['number'],
                        "state": pr_data['state'],
                        "changed_files": pr_data.get('changed_files', 0),
                        "description": pr_data.get('body', '') or None,
                        "title": pr_data.get('title', ''),
                        "commits": pr_data.get('commits', 0),
                        "mergeable": pr_data.get('mergeable', False)
                        if pr_data.get('mergeable') is not None else False,
                        "repo_name": pr_data['base']['repo']['full_name'],
                        "commits_url": pr_data['commits_url'].split("api.github.com")[1],
                        "action": 'opened',
                    }

                    pull_request_dto = PullRequestDTO(data=adapted_pr_data)

                    if pull_request_dto.is_valid():
                        pull_request = update_or_create_pull_request(
                            pull_request_dto=pull_request_dto,
                            repo_db=repo_db,
                            company=repo_db.company,
                        )
                        logger.info(f"Created/Updated PR in database: {pull_request.id}")
                    else:
                        logger.error(f"Invalid PullRequestDTO data: {pull_request_dto.errors}")
                        return Response(
                            {"error": "Error adapting Pull Request data"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                else:
                    logger.error(
                        f"Failed to fetch PR from GitHub. Status: {pr_response.status_code}, Response: {pr_response.text}"
                    )
                    return Response(
                        {"error": "Error fetching Pull Request data from GitHub"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                logger.info(f"Found existing PR in database: {pull_request.id}")

            # Only execute the task chain if 'create_graph' is True
            if data.get('create_graph'):
                logger.info("Starting workflow processing")
                trigger_type = ContentType.objects.get(model="pullrequest")
                chat_room, created = get_or_create_chat(
                    company=pull_request.company,
                    trigger_type=trigger_type,
                    trigger_id=pull_request.id,
                    agent="pull_request_chat",
                    name=pull_request.title,
                    environment=ENVIRONMENT.DEV,
                    update_thread=True,
                )

                task_chain = chain(
                    add_repo_diff_task.s(
                        repo_id=data['repo_id'],
                        company_id=data['company_id'],
                        pull_request_number=data['pull_request_number'],
                    ),
                ).apply_async()

                try:
                    task_chain.get()
                except Exception as e:
                    logger.error(f"Error executing task chain: {str(e)}")
                    return Response(
                        {"error": "Failed to process pull request"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                previous_messages = retrieve_pr_messages(chat_room=chat_room)
                logger.info(f"Retrieved {len(previous_messages)} previous messages")

                company_graph_manager = Neo4jManager.get_neo4j_manager_instance(
                    environment=ENVIRONMENT.DEV, company=pull_request.company
                )
                logger.info("Initialized Neo4j manager")

                try:
                    logger.info("Initializing PullRequestWorkflow")
                    pull_request_workflow = PullRequestWorkflow(
                        company_graph_manager=company_graph_manager,
                        pull_request=pull_request,
                        repo_db=repo_db,
                        previous_comments=previous_messages,
                    )
                    initial_state = pull_request_workflow.get_init_state()
                    pull_request_workflow.build_workflow()
                    logger.info("Invoking workflow")
                    report = pull_request_workflow.invoke(initial_state)
                    if "summary_report" in report:
                        save_message(chat_room=chat_room, message=report["summary_report"])
                    if "final_issues_report" in report:
                        save_message(chat_room=chat_room, message=report["final_issues_report"])
                    return Response(report, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Error in pull request workflow: {str(e)}")
                    return Response(
                        {"error": "Failed to generate pull request report"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                finally:
                    if data.get('create_graph') and data.get('delete_graph'):
                        logger.info("Deleting PR repository graph in finally block")
                        delete_pr_repo_graph(
                            company_id=data['company_id'],
                            repo_id=data['repo_id'],
                            pr_number=data['pull_request_number'],
                        )
            else:
                logger.info("create_graph flag is False, skipping task chain execution")
                return Response(
                    {"message": "Pull request processed without graph creation"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            logger.error(f"Error in pull request processing: {str(e)}")
            return Response(
                {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
            )


class WikiWriterApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        chat_room_id = serializers.CharField(required=False)
        message = serializers.CharField()
        tags = serializers.ListField(child=serializers.DictField(), required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Message
            fields = "__all__"

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = request.user.company
        company_graph_manager = Neo4jManager.get_neo4j_manager_instance(environment=ENVIRONMENT.MAIN, company=company)
        data = serializer.validated_data
        company_id = str(company.id)
        wiki_writer_graph = WikiWriterWorkFlow(company_id=company_id, graph_maanger=company_graph_manager)
        wiki_Writer_graph_initial_state = {"company_context": [], "company_context_query": data["message"]}
        wiki_writer_app = wiki_writer_graph.build_workflow()
        report = wiki_writer_app.invoke(wiki_Writer_graph_initial_state)
        return Response(report, status=status.HTTP_201_CREATED)
