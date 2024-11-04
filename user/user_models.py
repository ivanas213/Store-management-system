from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
database = SQLAlchemy()

# Association model for many-to-many relationship between users and roles
class UserRole(database.Model):
    __tablename__ = "userroles"
    userRoleId = database.Column(database.Integer, primary_key=True)            # Primary key for the user-role association
    userID = database.Column(database.Integer, database.ForeignKey("users.userID"), nullable=False)  # Foreign key referencing users table
    roleID = database.Column(database.Integer, database.ForeignKey("roles.roleID"), nullable=False)  # Foreign key referencing roles table

# Model representing the user entity
class User(database.Model):
    __tablename__ = "users"
    userID = database.Column(database.Integer, primary_key=True)                # Unique ID for each user
    forename = database.Column(database.String(256), nullable=False)            # User's first name, required field
    surname = database.Column(database.String(256), nullable=False)             # User's last name, required field
    email = database.Column(database.String(256), nullable=False, unique=True)  # User's email, required and unique
    password = database.Column(database.String(256), nullable=False)            # User's password, required
    roles = database.relationship("Role", secondary=UserRole.__table__, back_populates="users")  # Many-to-many relationship with roles

# Model representing the role entity
class Role(database.Model):
    __tablename__ = "roles"
    roleID = database.Column(database.Integer, primary_key=True)                # Unique ID for each role
    name = database.Column(database.String(256), nullable=False)                # Role name, required field
    users = database.relationship("User", secondary=UserRole.__table__, back_populates="roles")  # Many-to-many relationship with users
