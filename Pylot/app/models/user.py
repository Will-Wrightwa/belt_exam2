
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

    def get_my_friends_left(self,_id):
        query = "SELECT friend1.alias as alias, friend1.id as id from friendships  LEFT JOIN user AS friend1 ON friendships.friend1_user_id = friend1.id where friendships.friend2_user_id = :id"
        data = {'id': _id}
        return self.db.query_db(query, data)

    def get_my_friends_right(self,_id):
        query = "SELECT friend2.alias as alias, friend2.id as id from friendships  LEFT JOIN user AS friend2 ON friendships.friend2_user_id = friend2.id where friendships.friend1_user_id = :id"
        data = {'id': _id}
        return self.db.query_db(query, data)
    def get_my_friends(self,_id):
        my_friendsa = self.get_my_friends_right(_id)
        my_friendsb = self.get_my_friends_left(_id)
        my_friends = my_friendsa + my_friendsb
        return my_friends



    def get_notmy_friends(self,_id):
        friends = self.get_my_friends(_id)
        friends_ids = [row['id'] for row in friends]
        query = "SELECT alias, id from user where user.id not in :friends_ids and  user.id <> :id"
        data = {'id': _id, 'friends_ids':friends_ids}
        notmy_friends = self.db.query_db(query, data)
        print notmy_friends
        return notmy_friends
    def add_friend(self,my_id,friend_id):

        sql = "INSERT into friendships (friend1_user_id, friend2_user_id) values(:friend1_user_id,:friend2_user_id)"
        data = {'friend1_user_id': my_id, 'friend2_user_id': friend_id}
        self.db.query_db(sql, data)
        return True
    def unfriend(self,my_id,friend_id):
        sql ="DELETE FROM belt_exam2.friendships WHERE (friend1_user_id= :my_id  AND friend2_user_id = :friend_id) OR (friend2_user_id = :my_id AND friend1_user_id = :friend_id) ;"
        data = {'my_id': my_id, 'friend_id': friend_id}
        return self.db.query_db(sql,data)
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
