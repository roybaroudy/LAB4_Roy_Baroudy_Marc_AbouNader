"""
School Management System - PyQt5 GUI
====================================

This module provides a PyQt5-based graphical user interface (GUI)
for managing a school system. It supports:

* Students
* Instructors
* Courses
* Registrations
* Search
* Export/Backup

The system uses SQLite for persistence and JSON/CSV for import/export.

Author:
    Marc Abou Nader
"""

import sys, os, csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox
)
from school import db, services, storage

db.init_db()


class TabStudents(QWidget):
    """
    Tab for managing students.

    Provides a form and table to add, edit, delete, save, and load student records.
    """

    def __init__(self):
        """
        Initialize the Students tab.

        Sets up form fields, table, and buttons for student management.
        """
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.sid = QLineEdit(); self.sname = QLineEdit(); self.sage = QLineEdit(); self.semail = QLineEdit()
        top.addWidget(QLabel("ID")); top.addWidget(self.sid)
        top.addWidget(QLabel("Name")); top.addWidget(self.sname)
        top.addWidget(QLabel("Age")); top.addWidget(self.sage)
        top.addWidget(QLabel("Email")); top.addWidget(self.semail)
        v.addLayout(top)

        btns = QHBoxLayout()
        b1 = QPushButton("Add"); b2 = QPushButton("Edit"); b3 = QPushButton("Delete")
        b4 = QPushButton("Save JSON"); b5 = QPushButton("Load JSON")
        b1.clicked.connect(self.add); b2.clicked.connect(self.edit)
        b3.clicked.connect(self.delete); b4.clicked.connect(self.save_json)
        b5.clicked.connect(self.load_json)
        for b in (b1, b2, b3, b4, b5): btns.addWidget(b)
        v.addLayout(btns)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        v.addWidget(self.table)
        self.table.cellClicked.connect(self.on_sel)
        self.refresh()

    def refresh(self):
        """
        Reload all students into the table from the database.

        :return: None
        """
        rows = services.db.get_students()
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount(); self.table.insertRow(i)
            for j, val in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def on_sel(self, r, c):
        """
        Fill the form fields when a table row is selected.

        :param r: Row index
        :type r: int
        :param c: Column index
        :type c: int
        :return: None
        """
        self.sid.setText(self.table.item(r, 0).text())
        self.sname.setText(self.table.item(r, 1).text())
        self.sage.setText(self.table.item(r, 2).text())
        self.semail.setText(self.table.item(r, 3).text())

    def add(self):
        """
        Add a new student to the database.

        :raises Exception: If adding fails (e.g., duplicate ID)
        :return: None
        """
        try:
            services.add_student(self.sid.text(), self.sname.text(),
                                 self.sage.text(), self.semail.text())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def edit(self):
        """
        Edit the selected student's details.

        :raises Exception: If update fails
        :return: None
        """
        try:
            services.edit_student(self.sid.text(), self.sname.text(),
                                  self.sage.text(), self.semail.text())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def delete(self):
        """
        Delete the selected student from the database.

        :return: None
        """
        if not self.sid.text(): return
        services.remove_student(self.sid.text())
        self.refresh()

    def save_json(self):
        """
        Save student records to a JSON file.

        Opens a file dialog to select the save location.
        :return: None
        """
        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if not path: return
        storage.export_json(path)

    def load_json(self):
        """
        Load student records from a JSON file.

        Opens a file dialog to choose the file.
        :return: None
        """
        path, _ = QFileDialog.getOpenFileName(self, "Load JSON", "", "JSON Files (*.json)")
        if not path: return
        storage.import_json(path)
        self.refresh()


class TabInstructors(QWidget):
    """
    Tab for managing instructors.

    Provides a form and table to add, edit, and delete instructors.
    """

    def __init__(self):
        """Initialize the Instructors tab with fields and table."""
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.iid = QLineEdit(); self.iname = QLineEdit()
        self.iage = QLineEdit(); self.iemail = QLineEdit()
        top.addWidget(QLabel("ID")); top.addWidget(self.iid)
        top.addWidget(QLabel("Name")); top.addWidget(self.iname)
        top.addWidget(QLabel("Age")); top.addWidget(self.iage)
        top.addWidget(QLabel("Email")); top.addWidget(self.iemail)
        v.addLayout(top)

        btns = QHBoxLayout()
        b1 = QPushButton("Add"); b2 = QPushButton("Edit"); b3 = QPushButton("Delete")
        b1.clicked.connect(self.add); b2.clicked.connect(self.edit); b3.clicked.connect(self.delete)
        for b in (b1, b2, b3): btns.addWidget(b)
        v.addLayout(btns)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        v.addWidget(self.table)
        self.table.cellClicked.connect(self.on_sel)
        self.refresh()

    def refresh(self):
        """Reload instructors into the table."""
        rows = services.db.get_instructors()
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount(); self.table.insertRow(i)
            for j, val in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def on_sel(self, r, c):
        """Fill fields with selected instructor record."""
        self.iid.setText(self.table.item(r, 0).text())
        self.iname.setText(self.table.item(r, 1).text())
        self.iage.setText(self.table.item(r, 2).text())
        self.iemail.setText(self.table.item(r, 3).text())

    def add(self):
        """Add a new instructor."""
        try:
            services.add_instructor(self.iid.text(), self.iname.text(),
                                    self.iage.text(), self.iemail.text())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def edit(self):
        """Edit the selected instructor."""
        try:
            services.edit_instructor(self.iid.text(), self.iname.text(),
                                     self.iage.text(), self.iemail.text())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def delete(self):
        """Delete the selected instructor."""
        if not self.iid.text(): return
        services.remove_instructor(self.iid.text())
        self.refresh()


class TabCourses(QWidget):
    """
    Tab for managing courses.

    Allows adding new courses and assigning instructors.
    """

    def __init__(self):
        """Initialize the Courses tab with fields and table."""
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.cid = QLineEdit(); self.cname = QLineEdit(); self.cinstr = QComboBox()
        top.addWidget(QLabel("Course ID")); top.addWidget(self.cid)
        top.addWidget(QLabel("Course Name")); top.addWidget(self.cname)
        top.addWidget(QLabel("Instructor")); top.addWidget(self.cinstr)
        v.addLayout(top)

        btns = QHBoxLayout()
        b1 = QPushButton("Add"); b2 = QPushButton("Edit"); b3 = QPushButton("Delete")
        b1.clicked.connect(self.add); b2.clicked.connect(self.edit); b3.clicked.connect(self.delete)
        for b in (b1, b2, b3): btns.addWidget(b)
        v.addLayout(btns)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor ID", "Instructor Name"])
        v.addWidget(self.table)
        self.table.cellClicked.connect(self.on_sel)
        self.refresh()

    def refresh(self):
        """Reload courses and instructors into the table and dropdown."""
        self.cinstr.clear()
        self.cinstr.addItem("")
        for ins in services.db.get_instructors():
            self.cinstr.addItem(ins[0])
        rows = services.db.get_courses()
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount(); self.table.insertRow(i)
            for j, val in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem("" if val is None else str(val)))

    def on_sel(self, r, c):
        """Fill fields with selected course record."""
        self.cid.setText(self.table.item(r, 0).text())
        self.cname.setText(self.table.item(r, 1).text())
        self.cinstr.setCurrentText(self.table.item(r, 2).text())

    def add(self):
        """Add a new course."""
        try:
            services.add_course(self.cid.text(), self.cname.text(), self.cinstr.currentText() or None)
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def edit(self):
        """Edit the selected course."""
        try:
            services.edit_course(self.cid.text(), self.cname.text(), self.cinstr.currentText() or None)
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def delete(self):
        """Delete the selected course."""
        if not self.cid.text(): return
        services.remove_course(self.cid.text())
        self.refresh()


class TabReg(QWidget):
    """
    Tab for registering students to courses.
    """

    def __init__(self):
        """Initialize the Registrations tab with dropdowns and table."""
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.stu = QComboBox(); self.crs = QComboBox()
        top.addWidget(QLabel("Student")); top.addWidget(self.stu)
        top.addWidget(QLabel("Course")); top.addWidget(self.crs)
        b1 = QPushButton("Register"); b2 = QPushButton("Unregister")
        b1.clicked.connect(self.reg); b2.clicked.connect(self.unreg)
        top.addWidget(b1); top.addWidget(b2)
        v.addLayout(top)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Student ID", "Student Name", "Course ID", "Course Name"])
        v.addWidget(self.table)
        self.refresh()

    def refresh(self):
        """Reload students, courses, and registrations."""
        self.stu.clear(); self.crs.clear()
        for s in services.db.get_students():
            self.stu.addItem(s[0])
        for c in services.db.get_courses():
            self.crs.addItem(c[0])
        rows = services.db.get_registrations()
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount(); self.table.insertRow(i)
            for j, val in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def reg(self):
        """Register a student in a course."""
        try:
            services.register(self.stu.currentText(), self.crs.currentText())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def unreg(self):
        """Unregister a student from a course."""
        try:
            services.unregister(self.stu.currentText(), self.crs.currentText())
            self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))


class TabSearch(QWidget):
    """
    Tab for searching records (students, instructors, courses).
    """

    def __init__(self):
        """Initialize the Search tab with input and table."""
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.q = QLineEdit(); b = QPushButton("Search"); b.clicked.connect(self.go)
        top.addWidget(self.q); top.addWidget(b); v.addLayout(top)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Type", "ID", "Name", "Extra"])
        v.addWidget(self.table)

    def go(self):
        """Perform a search and display results."""
        s, i, c = services.query(self.q.text())
        self.table.setRowCount(0)
        for x in s:
            r = self.table.rowCount(); self.table.insertRow(r)
            for j, val in enumerate(("Student", x[0], x[1], x[3])):
                self.table.setItem(r, j, QTableWidgetItem(str(val)))
        for x in i:
            r = self.table.rowCount(); self.table.insertRow(r)
            for j, val in enumerate(("Instructor", x[0], x[1], x[3])):
                self.table.setItem(r, j, QTableWidgetItem(str(val)))
        for x in c:
            r = self.table.rowCount(); self.table.insertRow(r)
            for j, val in enumerate(("Course", x[0], x[1], x[2] if x[2] else "")):
                self.table.setItem(r, j, QTableWidgetItem(str(val)))


class TabExport(QWidget):
    """
    Tab for exporting and backing up data.
    """

    def __init__(self):
        """Initialize the Export tab with CSV and DB backup buttons."""
        super().__init__()
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        b1 = QPushButton("Export Students CSV")
        b2 = QPushButton("Export Instructors CSV")
        b3 = QPushButton("Export Courses CSV")
        b4 = QPushButton("Backup Database")
        b1.clicked.connect(self.csv_students); b2.clicked.connect(self.csv_instructors)
        b3.clicked.connect(self.csv_courses); b4.clicked.connect(self.backup_db)
        top.addWidget(b1); top.addWidget(b2); top.addWidget(b3); top.addWidget(b4)
        v.addLayout(top)

    def csv_students(self):
        """Export students to a CSV file."""
        path, _ = QFileDialog.getSaveFileName(self, "Export Students CSV", "", "CSV Files (*.csv)")
        if not path: return
        rows = services.db.get_students()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["student_id", "name", "age", "email"]); w.writerows(rows)

    def csv_instructors(self):
        """Export instructors to a CSV file."""
        path, _ = QFileDialog.getSaveFileName(self, "Export Instructors CSV", "", "CSV Files (*.csv)")
        if not path: return
        rows = services.db.get_instructors()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["instructor_id", "name", "age", "email"]); w.writerows(rows)

    def csv_courses(self):
        """Export courses to a CSV file."""
        path, _ = QFileDialog.getSaveFileName(self, "Export Courses CSV", "", "CSV Files (*.csv)")
        if not path: return
        rows = services.db.get_courses()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["course_id", "course_name", "instructor_id", "instructor_name"]); w.writerows(rows)

    def backup_db(self):
        """Backup the SQLite database."""
        path, _ = QFileDialog.getSaveFileName(self, "Backup DB", "", "SQLite DB (*.db)")
        if not path: return
        services.db.backup_db(path)


class Main(QWidget):
    """
    Main application window.

    Hosts all the management tabs.
    """

    def __init__(self):
        """Initialize the main window with all tabs."""
        super().__init__()
        self.setWindowTitle("School Management System")
        v = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(TabStudents(), "Students")
        tabs.addTab(TabInstructors(), "Instructors")
        tabs.addTab(TabCourses(), "Courses")
        tabs.addTab(TabReg(), "Registrations")
        tabs.addTab(TabSearch(), "Search")
        tabs.addTab(TabExport(), "Export/Backup")
        v.addWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.resize(1000, 600)
    m.show()
    sys.exit(app.exec_())
