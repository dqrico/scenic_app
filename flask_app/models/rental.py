from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Rental:
    db_name = 'scenic_app'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.city = db_data['city']
        self.state = db_data['state']
        self.rate = db_data['rate']
        self.beds = db_data['beds']
        self.amenity_1 = db_data['amenity_1']
        self.amenity_2 = db_data['amenity_2']
        self.image = db_data['image']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO rentals (name, description, city, state, rate, beds, amenity_1, amenity_2, image, user_id) VALUES (%(name)s,%(description)s,%(city)s,%(state)s,%(rate)s,%(beds)s,%(amenity_1)s,%(amenity_2)s,%(iamge)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query =  "SELECT * FROM rentals JOIN users ON rentals.user_id=users.id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        rentals = []
        for row in results:
            rental = cls(row)
            user_data = {
                "id":row['users.id'],
                "first_name":row['first_name'], 
                "last_name":row['last_name'], 
                "email":row['email'], 
                "password":row['password'], 
                "created_at":row['users.created_at'],
                "updated_at":row['users.updated_at']
            }
            rentals.append(rental)
        return rentals
    
    @classmethod
    def  get_one(cls,data):
        query = '''
                SELECT * from rentals JOIN users AS creators ON rentals.user_id=creators.id
                LEFT JOIN favorited_rentals ON favorited_rentals.rental_id=tentals.id
                LEFT JOIN users AS users_who_favorited ON favorited_rentals.user_id=users_who_favorited.id
                WHERE rentals.id=%(id)s;'''
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results)<1:
            return False
        new_park=True
        for row in results:
            if new_rental:
                park= cls(row)
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
                Rental.creator = creator
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
                Rental.users_who_favorited.append(user_who_favorited)
                Rental.user_ids_who_favorited.append(row['users_who_favorited.id'])
        return Rental

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
                rental = cls(row)
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
    def update(cls, data):
        rental_id = int(data['id'])
        query = "UPDATE rentals SET name=%(name)s, description=%(description)s, city=%(city)s, state=%(state)s, rate=%(rate)s, beds=%(beds)s, amenity_1=%(amenity_1)s, amenity_2=%(amenity_2)s, image=%(image)s WHERE id={rental_id};".format(rental_id=rental_id)
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM rentals WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_rental(rental):
        print(rental)
        is_valid = True
        if len(rental['name']) < 3:
            is_valid = False
            flash("Rental name must be at least 2 characters","rental")
        if len(rental['description']) < 3:
            is_valid = False
            flash("Description must be at least 2 characters","rental")
        if len(rental['city']) < 3:
            is_valid = False
            flash("City must be at least 2 characters","rental")
        if len(rental['state']) < 3:
            is_valid = False
            flash("State must be at least 2 characters","rental")
        if len(rental['rate']) < 3:
            is_valid = False
            flash("Rate must be at least 2 characters","rental")
        if len(rental['beds']) < 3:
            is_valid = False
            flash("Beds must be at least 2 characters","rental")
        if len(rental['amenity_1']) < 3:
            is_valid = False
            flash("Amenity 1 must be at least 2 characters","rental")
        if len(rental['amenity_2']) < 3:
            is_valid = False
            flash("Amenity 2 must be at least 2 characters","rental")
        return is_valid
