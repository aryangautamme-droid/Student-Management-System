# ============================================================
# STUDENT PERFORMANCE MANAGEMENT SYSTEM
# PART - 1
# ============================================================

from abc import ABC, abstractmethod
import pickle
import os

# ============================================================
# PERSON CLASS
# ============================================================

class Person:
    def __init__(self, name, age, gender, email, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone

    def display_person(self):
        print("\n-----------------------------")
        print("Name      :", self.name)
        print("Age       :", self.age)
        print("Gender    :", self.gender)
        print("Email     :", self.email)
        print("Phone     :", self.phone)


# ============================================================
# STUDENT CLASS
# ============================================================

class Student(Person):

    def __init__(self,
                 student_id,
                 name,
                 age,
                 gender,
                 email,
                 phone,
                 course,
                 semester,
                 section,
                 admission_year):

        super().__init__(name, age, gender, email, phone)

        self.student_id = student_id
        self.course = course
        self.semester = semester
        self.section = section
        self.admission_year = admission_year

        # Encapsulation
        self.__marks = {}
        self.__attendance = {}

    # ============================================================
    # MARKS METHODS
    # ============================================================

    def add_mark(self, subject, marks):

        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100")

        self.__marks[subject] = marks

    def update_mark(self, subject, marks):

        if subject not in self.__marks:
            raise Exception("Subject not found.")

        if marks < 0 or marks > 100:
            raise ValueError("Invalid Marks")

        self.__marks[subject] = marks

    def delete_mark(self, subject):

        if subject in self.__marks:
            del self.__marks[subject]
        else:
            print("Subject not found.")

    def get_marks(self):
        return self.__marks

    # ============================================================
    # ATTENDANCE METHODS
    # ============================================================

    def add_attendance(self, subject, attended, total):

        if attended > total:
            raise ValueError("Attendance cannot exceed total classes.")

        self.__attendance[subject] = (attended, total)

    def get_attendance(self):
        return self.__attendance

    def attendance_percentage(self):

        attended = 0
        total = 0

        for value in self.__attendance.values():
            attended += value[0]
            total += value[1]

        if total == 0:
            return 0

        return round((attended / total) * 100, 2)

    # ============================================================
    # RESULT CALCULATIONS
    # ============================================================

    def total_marks(self):

        return sum(self.__marks.values())

    def average_marks(self):

        if len(self.__marks) == 0:
            return 0

        return round(self.total_marks() / len(self.__marks), 2)

    def percentage(self):

        if len(self.__marks) == 0:
            return 0

        total = len(self.__marks) * 100

        return round((self.total_marks() / total) * 100, 2)

    def cgpa(self):

        return round(self.percentage() / 9.5, 2)

    def grade(self):

        p = self.percentage()

        if p >= 90:
            return "A+"

        elif p >= 80:
            return "A"

        elif p >= 70:
            return "B+"

        elif p >= 60:
            return "B"

        elif p >= 50:
            return "C"

        elif p >= 40:
            return "D"

        else:
            return "F"

    def result(self):

        if self.percentage() >= 40:
            return "PASS"

        return "FAIL"

    # ============================================================
    # DISPLAY
    # ============================================================

    def display_student(self):

        print("\n===================================")
        print("STUDENT DETAILS")
        print("===================================")

        self.display_person()

        print("Student ID      :", self.student_id)
        print("Course          :", self.course)
        print("Semester        :", self.semester)
        print("Section         :", self.section)
        print("Admission Year  :", self.admission_year)

        print("\nSubjects & Marks")

        if len(self.__marks) == 0:
            print("No Marks Added")

        else:

            for subject, marks in self.__marks.items():
                print(subject, ":", marks)

        print("\nAttendance")

        if len(self.__attendance) == 0:
            print("No Attendance")

        else:

            for subject, value in self.__attendance.items():
                print(subject, ":", value[0], "/", value[1])

        print("-----------------------------------")
        print("Total        :", self.total_marks())
        print("Average      :", self.average_marks())
        print("Percentage   :", self.percentage())
        print("CGPA         :", self.cgpa())
        print("Grade        :", self.grade())
        print("Result       :", self.result())
        print("Attendance % :", self.attendance_percentage())
        print("===================================")
        # ============================================================
# PART - 2
# ABSTRACT REPORT CLASS & POLYMORPHISM
# ============================================================

class Report(ABC):
    """
    Abstract Report Class
    """

    @abstractmethod
    def calculate_result(self, student):
        pass

    @abstractmethod
    def generate_report(self, student):
        pass


# ============================================================
# UNDERGRADUATE REPORT
# ============================================================

class UndergraduateReport(Report):

    def calculate_result(self, student):

        return {
            "Total Marks": student.total_marks(),
            "Average": student.average_marks(),
            "Percentage": student.percentage(),
            "CGPA": student.cgpa(),
            "Grade": student.grade(),
            "Result": student.result(),
            "Attendance": student.attendance_percentage()
        }

    def generate_report(self, student):

        data = self.calculate_result(student)

        print("\n")
        print("=" * 55)
        print("        UNDERGRADUATE STUDENT REPORT")
        print("=" * 55)

        student.display_person()

        print("\nStudent Information")
        print("-" * 55)
        print("Student ID      :", student.student_id)
        print("Course          :", student.course)
        print("Semester        :", student.semester)
        print("Section         :", student.section)
        print("Admission Year  :", student.admission_year)

        print("\nMarks")
        print("-" * 55)

        marks = student.get_marks()

        if len(marks) == 0:
            print("No Marks Available")
        else:
            for subject, mark in marks.items():
                print(f"{subject:<20} : {mark}")

        print("\nAttendance")
        print("-" * 55)

        attendance = student.get_attendance()

        if len(attendance) == 0:
            print("No Attendance Available")
        else:
            for subject, value in attendance.items():
                print(f"{subject:<20} : {value[0]}/{value[1]}")

        print("\nAcademic Summary")
        print("-" * 55)

        for key, value in data.items():
            if key == "Attendance":
                print(f"{key:<20}: {value}%")
            else:
                print(f"{key:<20}: {value}")

        print("=" * 55)


# ============================================================
# POSTGRADUATE REPORT
# ============================================================

class PostgraduateReport(Report):

    def calculate_result(self, student):

        remark = "Excellent"

        if student.percentage() < 85:
            remark = "Very Good"

        if student.percentage() < 70:
            remark = "Good"

        if student.percentage() < 60:
            remark = "Average"

        if student.percentage() < 40:
            remark = "Needs Improvement"

        return {
            "Total Marks": student.total_marks(),
            "Average": student.average_marks(),
            "Percentage": student.percentage(),
            "CGPA": student.cgpa(),
            "Grade": student.grade(),
            "Result": student.result(),
            "Attendance": student.attendance_percentage(),
            "Remark": remark
        }

    def generate_report(self, student):

        data = self.calculate_result(student)

        print("\n")
        print("=" * 60)
        print("          POSTGRADUATE STUDENT REPORT")
        print("=" * 60)

        student.display_person()

        print("\nStudent Information")
        print("-" * 60)

        print("Student ID      :", student.student_id)
        print("Course          :", student.course)
        print("Semester        :", student.semester)
        print("Section         :", student.section)
        print("Admission Year  :", student.admission_year)

        print("\nMarks")
        print("-" * 60)

        marks = student.get_marks()

        if len(marks) == 0:
            print("No Marks Available")
        else:
            for subject, mark in marks.items():
                print(f"{subject:<20} : {mark}")

        print("\nAttendance")
        print("-" * 60)

        attendance = student.get_attendance()

        if len(attendance) == 0:
            print("No Attendance Available")
        else:
            for subject, value in attendance.items():
                print(f"{subject:<20} : {value[0]}/{value[1]}")

        print("\nPerformance Summary")
        print("-" * 60)

        for key, value in data.items():
            if key == "Attendance":
                print(f"{key:<20}: {value}%")
            else:
                print(f"{key:<20}: {value}")

        print("=" * 60)


# ============================================================
# POLYMORPHISM DEMO FUNCTION
# ============================================================

def print_student_report(student, report_type):
    """
    Polymorphism:
    The same function works with any class
    implementing the Report interface.
    """
    report_type.generate_report(student)
    # ============================================================
# PART - 3A-1
# STUDENT MANAGEMENT SYSTEM
# ============================================================

class StudentManagementSystem:

    def __init__(self):

        self.students = {}
        self.filename = "students.pkl"
        self.load_data()

    # ========================================================
    # SAVE DATA
    # ========================================================

    def save_data(self):

        try:

            with open(self.filename, "wb") as file:
                pickle.dump(self.students, file)

        except Exception as e:
            print("Error while saving data :", e)

    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):

        if not os.path.exists(self.filename):
            self.students = {}
            return

        try:

            with open(self.filename, "rb") as file:
                self.students = pickle.load(file)

        except Exception:

            self.students = {}

    # ========================================================
    # CHECK DUPLICATE STUDENT ID
    # ========================================================

    def student_exists(self, student_id):

        return student_id in self.students

    # ========================================================
    # GET STUDENT
    # ========================================================

    def get_student(self, student_id):

        return self.students.get(student_id)

    # ========================================================
    # DISPLAY ALL STUDENTS
    # ========================================================

    def display_all_students(self):

        if len(self.students) == 0:

            print("\nNo Student Records Found.")
            return

        print("\n")
        print("=" * 95)
        print("{:<12}{:<20}{:<15}{:<12}{:<12}{:<10}".format(
            "Student ID",
            "Name",
            "Course",
            "Semester",
            "CGPA",
            "Grade"))

        print("=" * 95)

        for student in self.students.values():

            print("{:<12}{:<20}{:<15}{:<12}{:<12}{:<10}".format(

                student.student_id,
                student.name,
                student.course,
                student.semester,
                student.cgpa(),
                student.grade()

            ))

        print("=" * 95)

    # ========================================================
    # DISPLAY COMPLETE DETAILS
    # ========================================================

    def display_student_details(self, student_id):

        if student_id not in self.students:

            print("Student Not Found.")
            return

        self.students[student_id].display_student()

    # ========================================================
    # COUNT STUDENTS
    # ========================================================

    def total_students(self):

        return len(self.students)

    # ========================================================
    # CLEAR ALL RECORDS
    # ========================================================

    def clear_records(self):

        choice = input("Delete all records? (Y/N): ").upper()

        if choice == "Y":

            self.students.clear()
            self.save_data()

            print("All records deleted successfully.")

        else:

            print("Operation Cancelled.")

    # ========================================================
    # CHECK EMPTY DATABASE
    # ========================================================

    def is_empty(self):

        return len(self.students) == 0

    # ========================================================
    # PRINT DATABASE SUMMARY
    # ========================================================

    def database_summary(self):

        print("\n")
        print("=" * 40)
        print("DATABASE SUMMARY")
        print("=" * 40)

        print("Total Students :", self.total_students())

        if self.total_students() == 0:

            print("Database Status : Empty")

        else:

            print("Database Status : Active")

        print("=" * 40)
        # ============================================================
# PART - 3A-2.1
# ADD STUDENT & UPDATE STUDENT
# ============================================================

    def add_student(self):

        try:

            print("\n========== ADD NEW STUDENT ==========")

            student_id = input("Student ID : ").strip()

            if self.student_exists(student_id):
                raise Exception("Student ID already exists.")

            name = input("Name : ")
            age = int(input("Age : "))
            gender = input("Gender : ")
            email = input("Email : ")
            phone = input("Phone : ")

            course = input("Course : ")
            semester = input("Semester : ")
            section = input("Section : ")
            admission_year = input("Admission Year : ")

            student = Student(
                student_id,
                name,
                age,
                gender,
                email,
                phone,
                course,
                semester,
                section,
                admission_year
            )

            n = int(input("\nNumber of Subjects : "))

            for i in range(n):

                print(f"\nSubject {i+1}")

                subject = input("Subject Name : ")
                marks = float(input("Marks (0-100) : "))

                student.add_mark(subject, marks)

                attended = int(input("Classes Attended : "))
                total = int(input("Total Classes : "))

                student.add_attendance(subject, attended, total)

            self.students[student_id] = student

            self.save_data()

            print("\nStudent Added Successfully.")

        except Exception as e:

            print("Error :", e)

    # =======================================================
    # UPDATE STUDENT DETAILS
    # =======================================================

    def update_student(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:

            print("Student Not Found.")
            return

        student = self.students[sid]

        print("\nLeave Blank to Keep Old Value\n")

        name = input(f"Name ({student.name}) : ")
        if name:
            student.name = name

        age = input(f"Age ({student.age}) : ")
        if age:
            student.age = int(age)

        gender = input(f"Gender ({student.gender}) : ")
        if gender:
            student.gender = gender

        email = input(f"Email ({student.email}) : ")
        if email:
            student.email = email

        phone = input(f"Phone ({student.phone}) : ")
        if phone:
            student.phone = phone

        course = input(f"Course ({student.course}) : ")
        if course:
            student.course = course

        semester = input(f"Semester ({student.semester}) : ")
        if semester:
            student.semester = semester

        section = input(f"Section ({student.section}) : ")
        if section:
            student.section = section

        admission = input(
            f"Admission Year ({student.admission_year}) : "
        )

        if admission:
            student.admission_year = admission

        self.save_data()

        print("\nStudent Updated Successfully.")
        # ============================================================
# PART - 3A-2.2
# DELETE STUDENT, MARKS & ATTENDANCE MANAGEMENT
# ============================================================

    # --------------------------------------------------------
    # DELETE STUDENT
    # --------------------------------------------------------

    def delete_student(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        choice = input("Are you sure? (Y/N): ").upper()

        if choice == "Y":
            del self.students[sid]
            self.save_data()
            print("Student Deleted Successfully.")
        else:
            print("Operation Cancelled.")

    # --------------------------------------------------------
    # ADD SUBJECT
    # --------------------------------------------------------

    def add_subject_marks(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        student = self.students[sid]

        try:
            subject = input("Subject Name : ")

            if subject in student.get_marks():
                print("Subject already exists.")
                return

            marks = float(input("Marks : "))
            student.add_mark(subject, marks)

            attended = int(input("Classes Attended : "))
            total = int(input("Total Classes : "))

            student.add_attendance(subject, attended, total)

            self.save_data()

            print("Subject Added Successfully.")

        except Exception as e:
            print("Error :", e)

    # --------------------------------------------------------
    # UPDATE MARKS
    # --------------------------------------------------------

    def update_subject_marks(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        student = self.students[sid]

        subject = input("Subject Name : ")

        if subject not in student.get_marks():
            print("Subject Not Found.")
            return

        try:

            marks = float(input("New Marks : "))
            student.update_mark(subject, marks)

            self.save_data()

            print("Marks Updated Successfully.")

        except Exception as e:
            print("Error :", e)

    # --------------------------------------------------------
    # DELETE SUBJECT
    # --------------------------------------------------------

    def delete_subject(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        student = self.students[sid]

        subject = input("Subject Name : ")

        if subject not in student.get_marks():
            print("Subject Not Found.")
            return

        student.delete_mark(subject)

        attendance = student.get_attendance()

        if subject in attendance:
            del attendance[subject]

        self.save_data()

        print("Subject Deleted Successfully.")

    # --------------------------------------------------------
    # UPDATE ATTENDANCE
    # --------------------------------------------------------

    def update_attendance(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        student = self.students[sid]

        subject = input("Subject Name : ")

        if subject not in student.get_attendance():
            print("Subject Not Found.")
            return

        try:

            attended = int(input("Classes Attended : "))
            total = int(input("Total Classes : "))

            student.add_attendance(subject, attended, total)

            self.save_data()

            print("Attendance Updated Successfully.")

        except Exception as e:
            print("Error :", e)

    # --------------------------------------------------------
    # DISPLAY SINGLE STUDENT REPORT
    # --------------------------------------------------------

    def show_student_report(self):

        sid = input("Enter Student ID : ")

        if sid not in self.students:
            print("Student Not Found.")
            return

        student = self.students[sid]

        print("\n1. Undergraduate Report")
        print("2. Postgraduate Report")

        choice = input("Choice : ")

        if choice == "1":
            report = UndergraduateReport()

        elif choice == "2":
            report = PostgraduateReport()

        else:
            print("Invalid Choice")
            return

        report.generate_report(student)
        # ============================================================
# PART - 3B-1
# SEARCH & SORTING FUNCTIONS
# ============================================================

    # --------------------------------------------------------
    # SEARCH BY STUDENT ID
    # --------------------------------------------------------

    def search_by_id(self):

        sid = input("Enter Student ID : ").strip()

        if sid not in self.students:
            print("Student Not Found.")
            return

        self.students[sid].display_student()

    # --------------------------------------------------------
    # SEARCH BY NAME
    # --------------------------------------------------------

    def search_by_name(self):

        name = input("Enter Student Name : ").lower()

        found = False

        for student in self.students.values():

            if student.name.lower() == name:

                student.display_student()
                found = True

        if not found:
            print("No Student Found.")

    # --------------------------------------------------------
    # SEARCH BY COURSE
    # --------------------------------------------------------

    def search_by_course(self):

        course = input("Enter Course : ").lower()

        found = False

        print("\n" + "=" * 80)

        for student in self.students.values():

            if student.course.lower() == course:

                print(
                    student.student_id,
                    student.name,
                    student.course,
                    student.semester,
                    student.percentage()
                )

                found = True

        print("=" * 80)

        if not found:
            print("No Student Found.")

    # --------------------------------------------------------
    # SEARCH BY SEMESTER
    # --------------------------------------------------------

    def search_by_semester(self):

        semester = input("Enter Semester : ").lower()

        found = False

        print("\n" + "=" * 80)

        for student in self.students.values():

            if str(student.semester).lower() == semester:

                print(
                    student.student_id,
                    student.name,
                    student.course,
                    student.semester,
                    student.cgpa()
                )

                found = True

        print("=" * 80)

        if not found:
            print("No Student Found.")

    # --------------------------------------------------------
    # SEARCH MENU
    # --------------------------------------------------------

    def search_menu(self):

        while True:

            print("\n========== SEARCH MENU ==========")
            print("1. Search by Student ID")
            print("2. Search by Name")
            print("3. Search by Course")
            print("4. Search by Semester")
            print("5. Back")

            choice = input("Enter Choice : ")

            if choice == "1":
                self.search_by_id()

            elif choice == "2":
                self.search_by_name()

            elif choice == "3":
                self.search_by_course()

            elif choice == "4":
                self.search_by_semester()

            elif choice == "5":
                break

            else:
                print("Invalid Choice.")

    # ========================================================
    # SORTING FUNCTIONS
    # ========================================================

    def sort_by_percentage(self):

        if self.is_empty():
            print("No Student Records.")
            return

        students = sorted(
            self.students.values(),
            key=lambda s: s.percentage(),
            reverse=True
        )

        print("\n===== SORTED BY PERCENTAGE =====")

        for s in students:

            print(
                s.student_id,
                s.name,
                s.percentage(),
                "%",
                "CGPA:",
                s.cgpa()
            )

    def sort_by_cgpa(self):

        if self.is_empty():
            print("No Student Records.")
            return

        students = sorted(
            self.students.values(),
            key=lambda s: s.cgpa(),
            reverse=True
        )

        print("\n===== SORTED BY CGPA =====")

        for s in students:

            print(
                s.student_id,
                s.name,
                s.cgpa(),
                "Percentage:",
                s.percentage()
            )

    def sort_by_name(self):

        if self.is_empty():
            print("No Student Records.")
            return

        students = sorted(
            self.students.values(),
            key=lambda s: s.name.lower()
        )

        print("\n===== SORTED BY NAME =====")

        for s in students:

            print(
                s.student_id,
                s.name,
                s.course,
                s.semester
            )

    def sort_by_roll_number(self):

        if self.is_empty():
            print("No Student Records.")
            return

        students = sorted(
            self.students.values(),
            key=lambda s: s.student_id
        )

        print("\n===== SORTED BY ROLL NUMBER =====")

        for s in students:

            print(
                s.student_id,
                s.name,
                s.course,
                s.cgpa()
            )

    # --------------------------------------------------------
    # SORT MENU
    # --------------------------------------------------------

    def sort_menu(self):

        while True:

            print("\n========== SORT MENU ==========")
            print("1. Sort by Percentage")
            print("2. Sort by CGPA")
            print("3. Sort by Name")
            print("4. Sort by Roll Number")
            print("5. Back")

            choice = input("Enter Choice : ")

            if choice == "1":
                self.sort_by_percentage()

            elif choice == "2":
                self.sort_by_cgpa()

            elif choice == "3":
                self.sort_by_name()

            elif choice == "4":
                self.sort_by_roll_number()

            elif choice == "5":
                break

            else:
                print("Invalid Choice.")
                # ============================================================
# PART - 3B-2.1
# STATISTICS (HIGHEST, LOWEST, TOP 5, AVERAGE)
# ============================================================

    # --------------------------------------------------------
    # HIGHEST SCORER
    # --------------------------------------------------------

    def highest_scorer(self):

        if self.is_empty():
            print("No Student Records.")
            return

        topper = max(
            self.students.values(),
            key=lambda s: s.percentage()
        )

        print("\n========== HIGHEST SCORER ==========")
        print("Student ID :", topper.student_id)
        print("Name       :", topper.name)
        print("Course     :", topper.course)
        print("Percentage :", topper.percentage())
        print("CGPA       :", topper.cgpa())
        print("Grade      :", topper.grade())

    # --------------------------------------------------------
    # LOWEST SCORER
    # --------------------------------------------------------

    def lowest_scorer(self):

        if self.is_empty():
            print("No Student Records.")
            return

        student = min(
            self.students.values(),
            key=lambda s: s.percentage()
        )

        print("\n========== LOWEST SCORER ==========")
        print("Student ID :", student.student_id)
        print("Name       :", student.name)
        print("Course     :", student.course)
        print("Percentage :", student.percentage())
        print("CGPA       :", student.cgpa())
        print("Grade      :", student.grade())

    # --------------------------------------------------------
    # TOP 5 STUDENTS
    # --------------------------------------------------------

    def top_five_students(self):

        if self.is_empty():
            print("No Student Records.")
            return

        students = sorted(
            self.students.values(),
            key=lambda s: s.percentage(),
            reverse=True
        )

        print("\n================ TOP 5 STUDENTS ================")
        print("{:<5}{:<12}{:<20}{:<12}{:<10}".format(
            "Rank",
            "ID",
            "Name",
            "Percentage",
            "CGPA"
        ))

        print("=" * 65)

        for i, student in enumerate(students[:5], start=1):

            print("{:<5}{:<12}{:<20}{:<12}{:<10}".format(
                i,
                student.student_id,
                student.name,
                student.percentage(),
                student.cgpa()
            ))

    # --------------------------------------------------------
    # AVERAGE MARKS OF ALL STUDENTS
    # --------------------------------------------------------

    def average_marks_all_students(self):

        if self.is_empty():
            print("No Student Records.")
            return

        total = 0

        for student in self.students.values():
            total += student.percentage()

        average = total / len(self.students)

        print("\nAverage Percentage of Class :",
              round(average, 2), "%")

    # --------------------------------------------------------
    # CLASS SUMMARY
    # --------------------------------------------------------

    def class_summary(self):

        if self.is_empty():
            print("No Student Records.")
            return

        print("\n==============================")
        print("CLASS SUMMARY")
        print("==============================")

        print("Total Students :", len(self.students))

        percentages = [
            s.percentage()
            for s in self.students.values()
        ]

        print("Highest Percentage :", max(percentages))
        print("Lowest Percentage  :", min(percentages))
        print("Average Percentage :", round(
            sum(percentages) / len(percentages), 2))

        print("==============================")
        # ============================================================
# PART - 3B-2.2
# PASS/FAIL STATISTICS & PERFORMANCE DASHBOARD
# ============================================================

    # --------------------------------------------------------
    # PASS / FAIL STATISTICS
    # --------------------------------------------------------

    def pass_fail_statistics(self):

        if self.is_empty():
            print("No Student Records.")
            return

        passed = 0
        failed = 0

        for student in self.students.values():

            if student.result() == "PASS":
                passed += 1
            else:
                failed += 1

        print("\n========== PASS / FAIL STATISTICS ==========")
        print("Total Students :", len(self.students))
        print("Passed         :", passed)
        print("Failed         :", failed)

        if len(self.students) > 0:
            print("Pass Percentage :", round((passed / len(self.students)) * 100, 2), "%")
            print("Fail Percentage :", round((failed / len(self.students)) * 100, 2), "%")

    # --------------------------------------------------------
    # ATTENDANCE SUMMARY
    # --------------------------------------------------------

    def attendance_summary(self):

        if self.is_empty():
            print("No Student Records.")
            return

        print("\n========== ATTENDANCE SUMMARY ==========")

        total = 0

        for student in self.students.values():

            att = student.attendance_percentage()

            total += att

            print(
                f"{student.student_id:<12}"
                f"{student.name:<20}"
                f"{att:.2f}%"
            )

        print("------------------------------------------")
        print("Overall Attendance :",
              round(total / len(self.students), 2), "%")

    # --------------------------------------------------------
    # PERFORMANCE DASHBOARD
    # --------------------------------------------------------

    def performance_dashboard(self):

        if self.is_empty():
            print("No Student Records.")
            return

        print("\n")
        print("=" * 75)
        print("          STUDENT PERFORMANCE DASHBOARD")
        print("=" * 75)

        print("Total Students :", len(self.students))

        topper = max(
            self.students.values(),
            key=lambda s: s.percentage()
        )

        lowest = min(
            self.students.values(),
            key=lambda s: s.percentage()
        )

        average = sum(
            s.percentage()
            for s in self.students.values()
        ) / len(self.students)

        print("\nHighest Scorer")
        print("----------------------")
        print(topper.name, "-", topper.percentage(), "%")

        print("\nLowest Scorer")
        print("----------------------")
        print(lowest.name, "-", lowest.percentage(), "%")

        print("\nAverage Percentage")
        print("----------------------")
        print(round(average, 2), "%")

        self.pass_fail_statistics()

        print("\nTop 5 Students")
        print("----------------------")

        top_students = sorted(
            self.students.values(),
            key=lambda s: s.percentage(),
            reverse=True
        )[:5]

        for i, student in enumerate(top_students, start=1):

            print(
                f"{i}. {student.name} "
                f"({student.percentage()}%)"
            )

        print("\nAttendance Summary")
        print("----------------------")

        self.attendance_summary()

        print("=" * 75)
        # ============================================================
# PART - 4A
# MAIN MENU
# ============================================================

def main():

    system = StudentManagementSystem()

    while True:

        print("\n")
        print("=" * 60)
        print("     STUDENT PERFORMANCE MANAGEMENT SYSTEM")
        print("=" * 60)

        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Display All Students")
        print("5. Display Student Details")
        print("6. Add Subject")
        print("7. Update Subject Marks")
        print("8. Delete Subject")
        print("9. Update Attendance")
        print("10. Generate Student Report")
        print("11. Search Student")
        print("12. Sort Students")
        print("13. Highest Scorer")
        print("14. Lowest Scorer")
        print("15. Top 5 Students")
        print("16. Average Marks")
        print("17. Class Summary")
        print("18. Pass/Fail Statistics")
        print("19. Attendance Summary")
        print("20. Performance Dashboard")
        print("21. Database Summary")
        print("22. Clear All Records")
        print("23. Exit")

        choice = input("\nEnter Your Choice : ")

        try:

            if choice == "1":
                system.add_student()

            elif choice == "2":
                system.update_student()

            elif choice == "3":
                system.delete_student()

            elif choice == "4":
                system.display_all_students()

            elif choice == "5":

                sid = input("Enter Student ID : ")
                system.display_student_details(sid)

            elif choice == "6":
                system.add_subject_marks()

            elif choice == "7":
                system.update_subject_marks()

            elif choice == "8":
                system.delete_subject()

            elif choice == "9":
                system.update_attendance()

            elif choice == "10":
                system.show_student_report()

            elif choice == "11":
                system.search_menu()

            elif choice == "12":
                system.sort_menu()

            elif choice == "13":
                system.highest_scorer()

            elif choice == "14":
                system.lowest_scorer()

            elif choice == "15":
                system.top_five_students()

            elif choice == "16":
                system.average_marks_all_students()

            elif choice == "17":
                system.class_summary()

            elif choice == "18":
                system.pass_fail_statistics()

            elif choice == "19":
                system.attendance_summary()

            elif choice == "20":
                system.performance_dashboard()

            elif choice == "21":
                system.database_summary()

            elif choice == "22":
                system.clear_records()

            elif choice == "23":

                print("\nThank You for Using the System.")
                break

            else:

                print("Invalid Choice!")

        except Exception as e:

            print("Error :", e)
            # ============================================================
# PART - 4B
# PROGRAM STARTS HERE
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n\nProgram Interrupted by User.")

    except Exception as e:
        print("Unexpected Error :", e)

    finally:
        print("\nProgram Closed Successfully.")
        