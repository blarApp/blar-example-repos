from .person import Person

class Student(Person):
    """A class representing a student, inheriting from Person."""

    def __init__(self, name: str, age: int, student_id: str, major: str):
        super().__init__(name, age)
        self.student_id = student_id
        self.major = major
    
    def introduce_self(self) -> str:
        """Return a string introducing the student, overriding the parent method."""
        base_intro = super().introduce_self()
        return f"{base_intro} I am a student majoring in {self.major} (ID: {self.student_id})."

    def study(self, subject: str) -> str:
        """Simulate the student studying a subject."""
        return f"{self.name} is studying {subject}."
