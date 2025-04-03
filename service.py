# Incorrect placement (not in services.py or submodule)
def fetch_and_create_user(email, name):
    # Violates separation of concerns: combines fetching and creating logic
    existing_user = User.objects.filter(email=email).first()
    if existing_user:
        return existing_user
    new_user = User(email=email, name=name)
    new_user.save()
    return new_user


def get_active_users_and_activate(email_list):
    active_users = User.objects.filter(is_active=True, email__in=email_list)
    for user in active_users:
        user.is_active = False  # Modifies state
        user.save()
    return active_users  # 
