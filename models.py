from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ==========================
# Student Model
# ==========================
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    semester = db.Column(db.String(30))
    gender = db.Column(db.String(20))
    address = db.Column(db.Text)
    photo = db.Column(db.String(200))

    def __repr__(self):
        return f"<Student {self.name}>"


# ==========================
# Admin Model
# ==========================
class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"