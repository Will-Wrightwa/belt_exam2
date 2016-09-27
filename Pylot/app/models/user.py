
from system.core.model import Model
import re

class user(Model):
    def __init__(self):
        super(user, self).__init__()

    def login(self,form_data):
        #check that form fields were not tampered with
        if not all (k in form_data for k in ("email","password")):
            return {'errors':['oops you messed with the page']}

        user = self.get_user_by_email(form_data)
        print user
        if len(user) == 0 :                                                              #email matches?
            return {'errors':["we couldn't find your email"]}
        user = user[0]
        if not self.bcrypt.check_password_hash(user['password'],form_data['password']):     #password matches?
            return {'errors':["your password was wrong"]}
        return {'user':user}

    def register(self,form_data):
        errors = []
        #check that form fields were not tampered with
        if not all (k in form_data for k in ("name","alias","email","password","confirm_password")):  #change this tuple so that it includes all form fields
            return {'errors':['oops you messed with the page']}
        # add more validations here
        if not form_data['password'] == form_data['confirm_password']:          # password matches confirm password?
            errors.append('password did not match confirm password')

        if not re.match(r"[A-z]+@[A-z]+\.[A-z]",form_data['email']):            # valid email?
            errors.append("Not a valid email")

        if len(form_data['password']) < 8:                                      # valid password?
            errors.append('password not long enough')

        if len(self.get_user_by_email(form_data)) > 0:                          # already registered?
            errors.append('email already used')

        if errors:
            return {'errors':errors}
        return {'user':self.add_user(form_data)}

    def get_users(self):
        query = "SELECT * from user"
        return self.db.query_db(query)

    def get_user_by_email(self,form_data):
        query = "SELECT * from user where email = :email"
        return self.db.query_db(query, form_data)

    def add_user(self,form_data):
        query = "INSERT into user (name, alias, email, password) values(:name, :alias, :email, :pw_hash)"
        data = form_data.copy()
        data['pw_hash'] = self.bcrypt.generate_password_hash(form_data['password'])
        _id = self.db.query_db(query, data)
        return self.get_user_by_id(_id)

    def get_user_by_id(self,_id):
        query = "SELECT * from user where id = :id"
        data = {'id': _id}
        user = self.db.query_db(query, data)[0]
        return user


    """
    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user_by_id(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True

    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """
