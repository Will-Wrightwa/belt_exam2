from system.core.controller import *

class friends(Controller):
    def __init__(self, action):
        super(friends, self).__init__(action)
        self.load_model('user')

    def index(self):
        if 'user' in session:
            return redirect('/friends')
        return self.load_view('index.html')

    def friends(self):
        if not 'user' in session:
            return redirect('/')
        friends = self.models['user'].get_my_friends(session['user']['id'])
        print friends
        if len(friends) > 0:
            notfriends = self.models['user'].get_notmy_friends(session['user']['id'])
        else:
            notfriends = self.models['user'].get_other_users(session['user']['id'])
        return self.load_view('friends.html',user=session['user'],friends=friends,not_friends=notfriends)

    def login(self):

        result = self.models['user'].login(request.form)
        if 'errors' in result:
            for error in result['errors']:
                flash(error,"login")
            return redirect('/')
        session['user'] = result['user']
        return redirect('/friends')

    def register(self):
        result = self.models['user'].register(request.form)
        if 'errors' in result:
            for error in result['errors']:
                flash(error,"register")
            return redirect('/')
        session['user'] = result['user']
        return redirect('/friends')

    def logout(self):
        session.clear()
        return redirect("/")

    def profile(self,_id):
        friend = self.models['user'].get_user_by_id(_id)
        return self.load_view('profile.html',user=session['user'],friend=friend)
    def add_friend(self):
        if not "id" in request.form:
            flash("dont mess with the page!")
            return redirect('/friends')
        self.models['user'].add_friend(session['user']['id'], request.form['id'])
        return redirect('/friends')
    def unfriend(self):
        if not "id" in request.form:
            flash("dont mess with the page!")
            return redirect('/friends')
        self.models['user'].unfriend(session['user']['id'], request.form['id'])
        return redirect('/friends')
