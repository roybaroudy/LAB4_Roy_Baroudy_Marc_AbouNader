from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Person:
    name: str
    age: int
    email: str

@dataclass
class Student(Person):
    student_id: str
    registered_courses: List[str] = field(default_factory=list)

@dataclass
class Instructor(Person):
    instructor_id: str
    assigned_courses: List[str] = field(default_factory=list)

@dataclass
class Course:
    course_id: str
    course_name: str
    instructor_id: Optional[str] = None
    enrolled_students: List[str] = field(default_factory=list)
