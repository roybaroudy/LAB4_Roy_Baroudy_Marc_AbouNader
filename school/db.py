import sqlite3, os, shutil, datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "school.db")

def get_conn():
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS instructors(
        instructor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        course_id TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        instructor_id TEXT,
        FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations(
        student_id TEXT NOT NULL,
        course_id TEXT NOT NULL,
        PRIMARY KEY(student_id, course_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()

def backup_db(dst_path: str):
    src = DB_PATH
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copyfile(src, dst_path)

def insert_student(student_id, name, age, email):
    conn = get_conn()
    conn.execute("INSERT INTO students(student_id,name,age,email) VALUES(?,?,?,?)",(student_id,name,int(age),email))
    conn.commit()
    conn.close()

def update_student(student_id, name, age, email):
    conn = get_conn()
    conn.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?",(name,int(age),email,student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_conn()
    conn.execute("DELETE FROM students WHERE student_id=?",(student_id,))
    conn.commit()
    conn.close()

def get_students():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT student_id,name,age,email FROM students ORDER BY student_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_instructor(instructor_id, name, age, email):
    conn = get_conn()
    conn.execute("INSERT INTO instructors(instructor_id,name,age,email) VALUES(?,?,?,?)",(instructor_id,name,int(age),email))
    conn.commit()
    conn.close()

def update_instructor(instructor_id, name, age, email):
    conn = get_conn()
    conn.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?",(name,int(age),email,instructor_id))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    conn = get_conn()
    conn.execute("DELETE FROM instructors WHERE instructor_id=?",(instructor_id,))
    conn.commit()
    conn.close()

def get_instructors():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT instructor_id,name,age,email FROM instructors ORDER BY instructor_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_course(course_id, course_name, instructor_id=None):
    conn = get_conn()
    conn.execute("INSERT INTO courses(course_id,course_name,instructor_id) VALUES(?,?,?)",(course_id,course_name,instructor_id))
    conn.commit()
    conn.close()

def update_course(course_id, course_name, instructor_id):
    conn = get_conn()
    conn.execute("UPDATE courses SET course_name=?, instructor_id=? WHERE course_id=?",(course_name,instructor_id,course_id))
    conn.commit()
    conn.close()

def delete_course(course_id):
    conn = get_conn()
    conn.execute("DELETE FROM courses WHERE course_id=?",(course_id,))
    conn.commit()
    conn.close()

def get_courses():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT c.course_id,c.course_name,c.instructor_id,i.name
    FROM courses c LEFT JOIN instructors i ON c.instructor_id=i.instructor_id
    ORDER BY c.course_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def register_student(student_id, course_id):
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO registrations(student_id,course_id) VALUES(?,?)",(student_id,course_id))
    conn.commit()
    conn.close()

def unregister_student(student_id, course_id):
    conn = get_conn()
    conn.execute("DELETE FROM registrations WHERE student_id=? AND course_id=?",(student_id,course_id))
    conn.commit()
    conn.close()

def get_registrations():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT r.student_id,s.name,r.course_id,c.course_name
    FROM registrations r
    JOIN students s ON s.student_id=r.student_id
    JOIN courses c ON c.course_id=r.course_id
    ORDER BY r.student_id,r.course_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def search(term):
    like = f"%{term}%"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT student_id,name,age,email FROM students WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?",(like,like,like))
    students = cur.fetchall()
    cur.execute("SELECT instructor_id,name,age,email FROM instructors WHERE instructor_id LIKE ? OR name LIKE ? OR email LIKE ?",(like,like,like))
    instructors = cur.fetchall()
    cur.execute("SELECT course_id,course_name,IFNULL(instructor_id,'') FROM courses WHERE course_id LIKE ? OR course_name LIKE ?",(like,like))
    courses = cur.fetchall()
    conn.close()
    return students, instructors, courses
