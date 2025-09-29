import json, os
from . import db

def export_json(path):
    s = db.get_students()
    i = db.get_instructors()
    c = db.get_courses()
    r = db.get_registrations()
    obj = {"students":[{"student_id":x[0],"name":x[1],"age":x[2],"email":x[3]} for x in s],
           "instructors":[{"instructor_id":x[0],"name":x[1],"age":x[2],"email":x[3]} for x in i],
           "courses":[{"course_id":x[0],"course_name":x[1],"instructor_id":x[2]} for x in c],
           "registrations":[{"student_id":x[0],"course_id":x[2]} for x in r]}
    with open(path,"w",encoding="utf-8") as f:
        json.dump(obj,f,indent=2)

def import_json(path):
    if not os.path.exists(path):
        return
    db.init_db()
    data = json.load(open(path,"r",encoding="utf-8"))
    for x in data.get("students",[]):
        try:
            db.insert_student(x["student_id"],x["name"],x["age"],x["email"])
        except:
            pass
    for x in data.get("instructors",[]):
        try:
            db.insert_instructor(x["instructor_id"],x["name"],x["age"],x["email"])
        except:
            pass
    for x in data.get("courses",[]):
        try:
            db.insert_course(x["course_id"],x["course_name"],x.get("instructor_id"))
        except:
            pass
    for x in data.get("registrations",[]):
        try:
            db.register_student(x["student_id"],x["course_id"])
        except:
            pass
