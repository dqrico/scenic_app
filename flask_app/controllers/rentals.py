from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.rental import Rental
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/dashboard")
def user_dashboard():
    user_data = {
        'id' : session['user_id']
    }
    #passing session data to template
    return render_template("dashboard.html", user=User.get_user_by_id(user_data), rentals=Rental.get_all())


@app.route("/rentals/new")
def new_rental_form():
    user_data = {
        'id' : session['user_id']
    }
    #passing session data to template
    return render_template("create_rental.html", user=User.get_user_by_id(user_data))

@app.route("/rentals/create", methods=["POST"])
def create_rental():
    if not Rental.validate_create(request.form):
        return redirect("/rentals/new")
    Rental.create(request.form)
    return redirect("/dashboard")

@app.route("/rentals/<int:id>")
def show_rental(id):
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(user_data)
    rental_data = {
        'id' : id
    }
    rental = Rental.get_one(rental_data)
    return render_template("show_rental.html", rental=rental, user=user)

@app.route("/rentals/<int:id>/edit")
def show_edit_form(id):
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(user_data)
    rental_data = {
        'id' : id
    }
    rental = Rental.get_one(rental_data)
    return render_template("edit_rental.html", rental=rental, user=user)

@app.route("/rentals/<int:id>/update", methods=["POST"])
def update_rental(id):
    Rental.update(request.form)
    return redirect("/dashboard")

@app.route("/rentals/<int:id>/delete", methods=["POST"])
def delete(id):
    Rental.delete(request.form)
    return redirect("/dashboard")