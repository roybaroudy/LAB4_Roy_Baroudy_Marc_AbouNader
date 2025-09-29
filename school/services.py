from . import db, validators

def add_student(student_id, name, age, email):
    if not validators.non_negative_age(age):
        raise ValueError("invalid age")
    if not validators.valid_email(email):
        raise ValueError("invalid email")
    db.insert_student(student_id, name, age, email)

def edit_student(student_id, name, age, email):
    if not validators.non_negative_age(age):
        raise ValueError("invalid age")
    if not validators.valid_email(email):
        raise ValueError("invalid email")
    db.update_student(student_id, name, age, email)

def remove_student(student_id):
    db.delete_student(student_id)

def add_instructor(instructor_id, name, age, email):
    if not validators.non_negative_age(age):
        raise ValueError("invalid age")
    if not validators.valid_email(email):
        raise ValueError("invalid email")
    db.insert_instructor(instructor_id, name, age, email)

def edit_instructor(instructor_id, name, age, email):
    if not validators.non_negative_age(age):
        raise ValueError("invalid age")
    if not validators.valid_email(email):
        raise ValueError("invalid email")
    db.update_instructor(instructor_id, name, age, email)

def remove_instructor(instructor_id):
    db.delete_instructor(instructor_id)

def add_course(course_id, course_name, instructor_id=None):
    db.insert_course(course_id, course_name, instructor_id if instructor_id else None)

def edit_course(course_id, course_name, instructor_id):
    db.update_course(course_id, course_name, instructor_id if instructor_id else None)

def remove_course(course_id):
    db.delete_course(course_id)

def assign_instructor(course_id, instructor_id):
    rows = db.get_courses()
    found = [x for x in rows if x[0]==course_id]
    if not found:
        raise ValueError("course not found")
    db.update_course(course_id, found[0][1], instructor_id)

def register(student_id, course_id):
    db.register_student(student_id, course_id)

def unregister(student_id, course_id):
    db.unregister_student(student_id, course_id)

def snapshot():
    return db.get_students(), db.get_instructors(), db.get_courses(), db.get_registrations()

def query(term):
    return db.search(term)
