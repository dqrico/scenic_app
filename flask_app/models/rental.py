from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Rental:
    db_name="scenic_app"

    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.description=data['description']
        self.city=data['city']
        self.state=data['state']
        self.rate=data['rate']
        self.beds=data['beds']
        self.amenity_1=data['amenity_1']
        self.amenity_2=data['amenity_2']
        self.image=data['image']
        self.user_id = data['user_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user = None
        self.users_who_favorited =[]
        self.user_ids_who_favorited = []


    
    @classmethod
    def get_all(cls):
        query ='''SELECT * FROM rentals JOIN users AS creators ON rentals.user_id = creators.id
            LEFT JOIN favorited_rentals ON rentals.id = favorited_rentals.rental_id
            LEFT JOIN users AS users_who_favorited ON favorited_rentals.user_id = users_who_favorited.id;'''
        results =connectToMySQL(cls.db_name).query_db(query)
        rentals=[]
        for row in results:
            new_rental = True
            user_who_favorited_data = {
                'id' : row['users_who_favorited.id'],
                'first_name':row['users_who_favorited.first_name'],
                'last_name':row['users_who_favorited.last_name'],
                'email':row['users_who_favorited.email'],
                'password':row['users_who_favorited.password'],
                'created_at':row['users_who_favorited.created_at'],
                'updated_at':row['users_who_favorited.updated_at']
            }
            number_of_rentals=len(rentals)
            if number_of_rentals > 0:
                last_rental=rentals[number_of_rentals-1]
                if last_rental.id == row['id']:
                    last_rental.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    last_rental.users_who_favorited.append(User(user_who_favorited_data))
                    new_rental = False

            if new_rental:
                rental= cls(row)
                user_data ={
                    'id' : row['creators.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['creators.created_at'],
                    'updated_at':row['creators.updated_at']
                }
                user = User(user_data)
                rental.user = user
                if row['users_who_favorited.id']:
                    rental.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    rental.users_who_favorited.append(User(user_who_favorited_data))
                rentals.append(rental)
        return rentals

    @classmethod
    def get_one(cls,data):
        query='''SELECT * FROM rentals
                JOIN users AS creators ON rentals.user_id=creators.id
                LEFT JOIN favorited_rentals ON favorited_rentals.rental_id=rentals.id
                LEFT JOIN users AS users_who_favorited ON favorited_rentals.user_id=users_who_favorited.id
                WHERE rentals.id=%(id)s;'''

        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results)<1:
            return False
        new_rental=True
        for row in results:
            if new_rental:
                rental= cls(row)
                user_data ={
                    'id' : row['creators.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['creators.created_at'],
                    'updated_at':row['creators.updated_at']
                }
                creator= User(user_data)
                rental.creator = creator
                new_rental= False
            if row['users_who_favorited.id']:
                user_who_favorited_data={
                    'id' : row['users_who_favorited.id'],
                    'first_name': row['users_who_favorited.first_name'],
                    'last_name': row['users_who_favorited.last_name'],
                    'email': row['users_who_favorited.email'],
                    'password': row['users_who_favorited.password'],
                    'created_at': row['users_who_favorited.created_at'],
                    'updated_at': row['users_who_favorited.updated_at']
                }
                user_who_favorited = User(user_who_favorited_data)
                rental.users_who_favorited.append(user_who_favorited)
                rental.user_ids_who_favorited.append(row['users_who_favorited.id'])
        return rental

    @classmethod
    def create(cls,data):
        query = "INSERT INTO rentals(name,description,city,state,rate,beds,amenity_1,amenity_2,image,user_id) VALUES(%(name)s,%(description)s,%(city)s,%(state)s,%(rate)s,%(beds)s,%(amenity_1)s,%(amenity_2)s,%(image)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def update(cls,data):
        query = "UPDATE rentals SET name=%(name)s, description=%(description)s, city=%(city)s, state=%(state)s,rete=%(rate)s;beds=%(beds)s,amenity_1=%(amenity_1)s,amenity_2=%(amenity_2)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query="DELETE FROM rentals WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def favorite(cls,data):
        query = 'INSERT INTO favorited_rentals(user_id, rental_id) VALUES(%(user_id)s, %(id)s);'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def unfavorite(cls,data):
        query='DELETE FROM favorited_rentals WHERE user_id=%(user_id)s AND rental_id=%(id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_create(rental):
        is_valid=True
        if len(rental['name']) <3:
            flash("rental must be greater then 2")
            is_valid = False
        if len(rental['description'])<3:
            is_valid = False
            flash("description must be greater then 2")
        if len(rental['city'])<3:
            is_valid = False
            flash("city must be greater then 2")
        if len(rental['state'])<3:
            is_valid = False
            flash("state must be greater then 2")
        if len(rental['rate'])<3:
            is_valid = False
            flash("rate must be greater then 2")
        if len(rental['beds'])<3:
            is_valid = False
            flash("beds must be greater then 2")
        if len(rental['amenity_1'])<3:
            is_valid = False
            flash("amenity_1 must be greater then 2")
        if len(rental['amenity_2'])<3:
            is_valid = False
            flash("amenity_2 must be greater then 2")
        return is_valid
