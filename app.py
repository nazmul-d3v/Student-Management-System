from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from config import Config
from models import db, Student, Admin

import os

from werkzeug.utils import secure_filename
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ==========================
# Upload Folder
# ==========================
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Login
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = Admin.query.filter_by(username=username).first()

        print("Username:", username)
        print("Admin:", admin)

        if admin:
            print("Password Match:", check_password_hash(admin.password, password))

        if admin and check_password_hash(admin.password, password):
            session["admin"] = admin.username
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid Username or Password!", "danger")

    return render_template("login.html")


# ==========================
# Dashboard
# ==========================
@app.route("/dashboard")
def dashboard():

    total_students = Student.query.count()

    male_students = Student.query.filter_by(
        gender="Male"
    ).count()

    female_students = Student.query.filter_by(
        gender="Female"
    ).count()

    total_departments = db.session.query(
        Student.department
    ).distinct().count()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        male_students=male_students,
        female_students=female_students,
        total_departments=total_departments
    )


# ==========================
# Add Student
# ==========================
@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        filename = ""

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        student = Student(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"],
            department=request.form["department"],
            semester=request.form["semester"],
            gender=request.form["gender"],
            address=request.form["address"],
            photo=filename
        )

        db.session.add(student)
        db.session.commit()

        flash("Student Added Successfully!", "success")

        return redirect(url_for("students"))

    return render_template("add_student.html")
# ==========================
# View Students + Search
# ==========================
@app.route("/students")
def students():

    search = request.args.get("search")

    if search:

        students = Student.query.filter(
            Student.name.contains(search) |
            Student.email.contains(search) |
            Student.department.contains(search)
        ).all()

    else:

        students = Student.query.all()

    return render_template(
        "students.html",
        students=students
    )


# ==========================
# Student Details
# ==========================
@app.route("/student/<int:id>")
def student_details(id):

    student = Student.query.get_or_404(id)

    return render_template(
        "student_details.html",
        student=student
    )


# ==========================
# Edit Student
# ==========================
@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.name = request.form["name"]
        student.email = request.form["email"]
        student.phone = request.form["phone"]
        student.department = request.form["department"]
        student.semester = request.form["semester"]
        student.gender = request.form["gender"]
        student.address = request.form["address"]

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            student.photo = filename

        db.session.commit()

        flash("Student Updated Successfully!", "success")

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


# ==========================
# Delete Student
# ==========================
@app.route("/delete-student/<int:id>")
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student Deleted Successfully!", "success")

    return redirect(url_for("students"))

# ==========================
# Admin Logout
# ==========================
@app.route("/logout")
def logout():

    session.pop("admin", None)

    flash("Logged Out Successfully!", "info")

    return redirect(url_for("login"))


# ==========================
# Run Application
# ==========================
if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = Admin.query.filter_by(
            username="admin"
        ).first()

        if not admin:

            admin = Admin(
                username="admin",
                password=generate_password_hash("admin123")
            )

            db.session.add(admin)
            db.session.commit()

            print("Default Admin Created!")

    app.run(debug=True)