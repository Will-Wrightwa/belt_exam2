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
        return self.load_view('friends.html',user=session['user'])

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
