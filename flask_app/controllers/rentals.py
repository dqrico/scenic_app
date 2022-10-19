from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_app.models.rental import Rental



@app.route("/dashboard")
def user_dashboard():
    user_data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(user_data)
    # rentals=Rental.get_all()
    rental = Rental.get_rentals()
    # return render_template("dashboard.html", user=user,rentals=rentals, rental=rental)
    return render_template("dashboard.html", user=user, rental=rental)

@app.route("/rentals/new")
def new_rental_form():
    user_data={
        'id': session['user_id']
    }
    user= User.get_user_by_id(user_data)
    return render_template("createOne.html",user=user)
    
@app.route("/rentals/create",methods=['POST'])
def create_rental():
    if not Rental.validate_create(request.form):
        return redirect("/rentals/new")
    Rental.create(request.form)
    return redirect("/dashboard")

@app.route("/show/<int:id>")
def show_rental(id):
    user_data={
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    rental_data={
        "id":id

    }
    rental= Rental.get_one(rental_data)
    return render_template('viewOne.html',rental=rental, user=user )

@app.route("/edit/<int:id>")
def show_edit_form(id):
    user_data ={
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    rental_data ={
        'id':id
    }
    rental = Rental.get_one(rental_data)
    return render_template("editOne.html",user=user,rental=rental)

@app.route("/rentals/<int:id>/update", methods=['POST'])
def update_rental(id):
    Rental.update(request.form)
    return redirect('/dashboard')

@app.route("/rentals/<int:id>/delete", methods = ['POST'])
def delete(id):
    rental_data = {
        'id': id
    }
    rental = Rental.get_one(rental_data)
    if (rental.user_id!=session['user_id']):
        flash(f"unauthorized access to edit rental with id {id}")
        return redirect("/dashboard")
    Rental.delete(request.form)
    return redirect("/dashboard")

@app.route('/rentals/<int:id>/favorite', methods=['POST'])
def favorite_rental(id):
    Rental.favorite(request.form)
    return redirect("/dashboard")

@app.route('/rentals/<int:id>/unfavorite', methods=['POST'])
def unfavorit_rental(id):
    Rental.unfavorite(request.form)
    return redirect("/dashboard")
