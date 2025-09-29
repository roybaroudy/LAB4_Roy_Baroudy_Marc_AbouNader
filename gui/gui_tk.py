import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from school import db, services, storage
import os

db.init_db()

class App(tk.Tk):
    """
    Main application window for the School Management System. Inherits from the Tkinter main window class.

    :param title: Sets the window title to "School Management System".
    :type title: str
    :param nb: A Notebook widget to hold different tabs for Students, Instructors, Courses, Registrations, and Search.
    :type nb: ttk.Notebook
    :param students_tab: Frame for managing students.
    :type students_tab: ttk.Frame
    :param instructors_tab: Frame for managing instructors.
    :type instructors_tab: ttk.Frame
    :param courses_tab: Frame for managing courses.
    :type courses_tab: ttk.Frame
    :param reg_tab: Frame for managing registrations.
    :type reg_tab: ttk.Frame
    :param search_tab: Frame for searching records.
    :type search_tab: ttk.Frame

    :return: None

    """
    def __init__(self):
        """
        constructor method to initialize the main application window and its components.
        """
        super().__init__()
        self.title("School Management System")
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)
        self.students_tab = ttk.Frame(nb)
        self.instructors_tab = ttk.Frame(nb)
        self.courses_tab = ttk.Frame(nb)
        self.reg_tab = ttk.Frame(nb)
        self.search_tab = ttk.Frame(nb)
        nb.add(self.students_tab, text="Students")
        nb.add(self.instructors_tab, text="Instructors")
        nb.add(self.courses_tab, text="Courses")
        nb.add(self.reg_tab, text="Registrations")
        nb.add(self.search_tab, text="Search")
        self.build_students()
        self.build_instructors()
        self.build_courses()
        self.build_reg()
        self.build_search()
        self.refresh_all()

    def build_students(self):
        """
        Build the student management interface.

        :param f: The frame to hold the student management widgets.
        :type f: ttk.Frame
        :param frm: A frame to hold the input fields and buttons.
        :type frm: ttk.Frame
        :param sid: StringVar for student ID input.
        :type sid: tk.StringVar
        :param sname: StringVar for student name input.
        :type sname: tk.StringVar
        :param sage: StringVar for student age input.
        :type sage: tk.StringVar
        :param semail: StringVar for student email input.
        :type semail: tk.StringVar
        :param student_tv: Treeview widget to display the list of students.
        :type student_tv: ttk.Treeview

        :return: None
        """
        f = self.students_tab
        frm = ttk.Frame(f); frm.pack(side="top", fill="x", padx=8, pady=8)
        self.sid = tk.StringVar(); self.sname = tk.StringVar(); self.sage = tk.StringVar(); self.semail = tk.StringVar()
        for i,(lbl,var) in enumerate([("ID",self.sid),("Name",self.sname),("Age",self.sage),("Email",self.semail)]):
            ttk.Label(frm, text=lbl).grid(row=0, column=2*i, sticky="w"); ttk.Entry(frm, textvariable=var, width=24).grid(row=0, column=2*i+1, padx=4)
        ttk.Button(frm, text="Add", command=self.add_student).grid(row=1, column=0, pady=6)
        ttk.Button(frm, text="Edit", command=self.edit_student).grid(row=1, column=1)
        ttk.Button(frm, text="Delete", command=self.delete_student).grid(row=1, column=2)
        ttk.Button(frm, text="Save JSON", command=self.save_json).grid(row=1, column=3)
        ttk.Button(frm, text="Load JSON", command=self.load_json).grid(row=1, column=4)
        self.student_tv = ttk.Treeview(f, columns=("id","name","age","email"), show="headings", height=10)
        for c in ("id","name","age","email"):
            self.student_tv.heading(c, text=c.title())
            self.student_tv.column(c, width=140, anchor="center")
        self.student_tv.pack(fill="both", expand=True, padx=8, pady=8)
        self.student_tv.bind("<<TreeviewSelect>>", self.on_student_sel)

    def build_instructors(self):
        """
        Build the instructor management interface.

        :param f: The frame to hold the instructor management widgets.
        :type f: ttk.Frame
        :param frm: A frame to hold the input fields and buttons.
        :type frm: ttk.Frame
        :param iid: StringVar for instructor ID input.
        :type iid: tk.StringVar
        :param iname: StringVar for instructor name input.
        :type iname: tk.StringVar
        :param iage: StringVar for instructor age input.
        :type iage: tk.StringVar
        :param iemail: StringVar for instructor email input.
        :type iemail: tk.StringVar
        :param instructor_tv: Treeview widget to display the list of instructors.
        :type instructor_tv: ttk.Treeview

        :return: None
        """
        f = self.instructors_tab
        frm = ttk.Frame(f); frm.pack(side="top", fill="x", padx=8, pady=8)
        self.iid = tk.StringVar(); self.iname = tk.StringVar(); self.iage = tk.StringVar(); self.iemail = tk.StringVar()
        for i,(lbl,var) in enumerate([("ID",self.iid),("Name",self.iname),("Age",self.iage),("Email",self.iemail)]):
            ttk.Label(frm, text=lbl).grid(row=0, column=2*i, sticky="w"); ttk.Entry(frm, textvariable=var, width=24).grid(row=0, column=2*i+1, padx=4)
        ttk.Button(frm, text="Add", command=self.add_instructor).grid(row=1, column=0, pady=6)
        ttk.Button(frm, text="Edit", command=self.edit_instructor).grid(row=1, column=1)
        ttk.Button(frm, text="Delete", command=self.delete_instructor).grid(row=1, column=2)
        self.instructor_tv = ttk.Treeview(f, columns=("id","name","age","email"), show="headings", height=10)
        for c in ("id","name","age","email"):
            self.instructor_tv.heading(c, text=c.title())
            self.instructor_tv.column(c, width=140, anchor="center")
        self.instructor_tv.pack(fill="both", expand=True, padx=8, pady=8)
        self.instructor_tv.bind("<<TreeviewSelect>>", self.on_instructor_sel)

    def build_courses(self):
        """
        Build the course management interface.

        :param f: The frame to hold the course management widgets.
        :type f: ttk.Frame
        :param top: A frame to hold the input fields and buttons.
        :type top: ttk.Frame
        :param cid: StringVar for course ID input.
        :type cid: tk.StringVar
        :param cname: StringVar for course name input.
        :type cname: tk.StringVar
        :param cinstr: Combobox for selecting the instructor for the course.
        :type cinstr: ttk.Combobox
        :param course_tv: Treeview widget to display the list of courses.
        :type course_tv: ttk.Treeview
        
        :return: None
        """
        f = self.courses_tab
        top = ttk.Frame(f); top.pack(side="top", fill="x", padx=8, pady=8)
        self.cid = tk.StringVar(); self.cname = tk.StringVar()
        ttk.Label(top, text="Course ID").grid(row=0, column=0, sticky="w"); ttk.Entry(top, textvariable=self.cid, width=20).grid(row=0, column=1, padx=4)
        ttk.Label(top, text="Course Name").grid(row=0, column=2, sticky="w"); ttk.Entry(top, textvariable=self.cname, width=30).grid(row=0, column=3, padx=4)
        ttk.Label(top, text="Instructor").grid(row=0, column=4, sticky="w")
        self.cinstr = ttk.Combobox(top, values=[], width=25); self.cinstr.grid(row=0, column=5, padx=4)
        ttk.Button(top, text="Add", command=self.add_course).grid(row=1, column=0, pady=6)
        ttk.Button(top, text="Edit", command=self.edit_course).grid(row=1, column=1)
        ttk.Button(top, text="Delete", command=self.delete_course).grid(row=1, column=2)
        self.course_tv = ttk.Treeview(f, columns=("id","name","instructor_id","instructor_name"), show="headings", height=10)
        for i,c in enumerate(("id","name","instructor_id","instructor_name")):
            self.course_tv.heading(c, text=c.title())
            self.course_tv.column(c, width=160 if i<2 else 180, anchor="center")
        self.course_tv.pack(fill="both", expand=True, padx=8, pady=8)
        self.course_tv.bind("<<TreeviewSelect>>", self.on_course_sel)

    def build_reg(self):
        """
        Build the registration management interface.
        :param f: The frame to hold the registration management widgets.
        :type f: ttk.Frame
        :param top: A frame to hold the input fields and buttons.
        :type top: ttk.Frame
        :param reg_student: Combobox for selecting a student to register.
        :type reg_student: ttk.Combobox
        :param reg_course: Combobox for selecting a course to register the student in.
        :type reg_course: ttk.Combobox
        :param reg_tv: Treeview widget to display the list of registrations.        
        :type reg_tv: ttk.Treeview

        :return: None
        """
        f = self.reg_tab
        top = ttk.Frame(f); top.pack(side="top", fill="x", padx=8, pady=8)
        ttk.Label(top, text="Student").grid(row=0, column=0)
        self.reg_student = ttk.Combobox(top, values=[], width=25); self.reg_student.grid(row=0, column=1, padx=4)
        ttk.Label(top, text="Course").grid(row=0, column=2)
        self.reg_course = ttk.Combobox(top, values=[], width=25); self.reg_course.grid(row=0, column=3, padx=4)
        ttk.Button(top, text="Register", command=self.register).grid(row=0, column=4, padx=6)
        ttk.Button(top, text="Unregister", command=self.unregister).grid(row=0, column=5, padx=6)
        self.reg_tv = ttk.Treeview(f, columns=("student_id","student_name","course_id","course_name"), show="headings", height=12)
        for c in ("student_id","student_name","course_id","course_name"):
            self.reg_tv.heading(c, text=c.title()); self.reg_tv.column(c, width=180, anchor="center")
        self.reg_tv.pack(fill="both", expand=True, padx=8, pady=8)

    def build_search(self):
        """
        Build the search interface.

        :param f: The frame to hold the search widgets.
        :type f: ttk.Frame
        :param top: A frame to hold the search input field and button.
        :type top: ttk.Frame
        :param q: StringVar for the search query input.
        :type q: tk.StringVar
        :param search_tv: Treeview widget to display the search results.
        :type search_tv: ttk.Treeview

        :return: None
        """
        f = self.search_tab
        top = ttk.Frame(f); top.pack(side="top", fill="x", padx=8, pady=8)
        self.q = tk.StringVar()
        ttk.Entry(top, textvariable=self.q, width=50).grid(row=0, column=0, padx=4)
        ttk.Button(top, text="Search", command=self.do_search).grid(row=0, column=1, padx=4)
        self.search_tv = ttk.Treeview(f, columns=("type","id","name","extra"), show="headings", height=15)
        for c in ("type","id","name","extra"):
            self.search_tv.heading(c, text=c.title()); self.search_tv.column(c, width=180, anchor="center")
        self.search_tv.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh_all(self):
        """
        Refresh all data displayed in the application, including students, instructors, courses, and registrations.

        :return: None
        """
        self.student_tv.delete(*self.student_tv.get_children())
        for s in services.db.get_students():
            self.student_tv.insert("", "end", values=s)
        self.instructor_tv.delete(*self.instructor_tv.get_children())
        for i in services.db.get_instructors():
            self.instructor_tv.insert("", "end", values=i)
        self.course_tv.delete(*self.course_tv.get_children())
        for c in services.db.get_courses():
            self.course_tv.insert("", "end", values=c)
        self.reg_tv.delete(*self.reg_tv.get_children())
        for r in services.db.get_registrations():
            self.reg_tv.insert("", "end", values=r)
        self.cinstr["values"] = [""] + [x[0] for x in services.db.get_instructors()]
        self.reg_student["values"] = [x[0] for x in services.db.get_students()]
        self.reg_course["values"] = [x[0] for x in services.db.get_courses()]

    def on_student_sel(self, e):
        """
        Handle the event when a student is selected in the student Treeview.
        :param e: The event object.
        :type e: tk.Event
        :param sel: The selected item in the Treeview.
        :type sel: tuple
        :param v: The values of the selected student item.
        :type v: tuple

        :return: None
        """
        sel = self.student_tv.selection()
        if not sel: return
        v = self.student_tv.item(sel[0])["values"]
        self.sid.set(v[0]); self.sname.set(v[1]); self.sage.set(v[2]); self.semail.set(v[3])

    def on_instructor_sel(self, e):
        """
        Handle the event when an instructor is selected in the instructor Treeview.

        :param e: The event object.
        :type e: tk.Event
        :param sel: The selected item in the Treeview.
        :type sel: tuple
        :param v: The values of the selected instructor item.
        :type v: tuple

        :return: None
        """
        sel = self.instructor_tv.selection()
        if not sel: return
        v = self.instructor_tv.item(sel[0])["values"]
        self.iid.set(v[0]); self.iname.set(v[1]); self.iage.set(v[2]); self.iemail.set(v[3])

    def on_course_sel(self, e):
        """
        Handle the event when a course is selected in the course Treeview.

        :param e: The event object.
        :type e: tk.Event
        :param sel: The selected item in the Treeview.
        :type sel: tuple
        :param v: The values of the selected course item.
        :type v: tuple

        :return: None
        """
        sel = self.course_tv.selection()
        if not sel: return
        v = self.course_tv.item(sel[0])["values"]
        self.cid.set(v[0]); self.cname.set(v[1]); self.cinstr.set(v[2] if v[2] else "")

    def add_student(self):
        """
        Add a new student using the input fields.

        :return: None
        """
        try:
            services.add_student(self.sid.get(), self.sname.get(), self.sage.get(), self.semail.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def edit_student(self):
        """ 
        Edit the selected student using the input fields.

        :return: None
        """
        try:
            services.edit_student(self.sid.get(), self.sname.get(), self.sage.get(), self.semail.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_student(self):
        """
        Delete the selected student.

        :return: None
        """
        if not self.sid.get(): return
        services.remove_student(self.sid.get())
        self.refresh_all()

    def add_instructor(self):
        """
        Add a new instructor using the input fields.
        
        :return: None
        """
        try:
            services.add_instructor(self.iid.get(), self.iname.get(), self.iage.get(), self.iemail.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def edit_instructor(self):
        """
        Edit the selected instructor using the input fields.

        :return: None
        """
        try:
            services.edit_instructor(self.iid.get(), self.iname.get(), self.iage.get(), self.iemail.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_instructor(self):
        """
        Delete the selected instructor.

        :return: None
        """
        if not self.iid.get(): return
        services.remove_instructor(self.iid.get())
        self.refresh_all()

    def add_course(self):
        """
        Add a new course using the input fields.

        :return: None
        """
        try:
            services.add_course(self.cid.get(), self.cname.get(), self.cinstr.get() or None)
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def edit_course(self):
        """
        Edit the selected course using the input fields.

        :return: None
        """
        try:
            services.edit_course(self.cid.get(), self.cname.get(), self.cinstr.get() or None)
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_course(self):
        """
        Delete the selected course.

        :return: None
        """
        if not self.cid.get(): return
        services.remove_course(self.cid.get())
        self.refresh_all()

    def register(self):
        """
        Register a student for a course using the selected student and course.

        :return: None
        """
        try:
            services.register(self.reg_student.get(), self.reg_course.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def unregister(self):
        """
        Unregister a student from a course using the selected student and course.

        :return: None
        """
        try:
            services.unregister(self.reg_student.get(), self.reg_course.get())
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def do_search(self):
        """
        Perform a search using the input query and display the results.

        :return: None
        """
        term = self.q.get()
        s,i,c = services.query(term)
        self.search_tv.delete(*self.search_tv.get_children())
        for x in s:
            self.search_tv.insert("", "end", values=("Student", x[0], x[1], x[3]))
        for x in i:
            self.search_tv.insert("", "end", values=("Instructor", x[0], x[1], x[3]))
        for x in c:
            self.search_tv.insert("", "end", values=("Course", x[0], x[1], x[2] if x[2] else ""))

    def save_json(self):
        """
        Save the current data to a JSON file.

        :return: None
        """
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not path: return
        storage.export_json(path)

    def load_json(self):
        """
        Load data from a JSON file.
        
        :return: None
        """
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path: return
        storage.import_json(path)
        self.refresh_all()

if __name__ == "__main__":

    App().mainloop()
