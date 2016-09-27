from system.core.router import routes

routes['default_controller'] = 'friends'
routes['POST']['/login'] = 'friends#login'
routes['POST']['/register'] = 'friends#register'
routes['GET']['/logout'] = 'friends#logout'
routes['GET']['/friends'] = 'friends#friends'
routes['GET']['/user/<_id>'] = 'friends#profile'
routes['GET']['/unfriend/<id>'] = 'friends#unfriend'

"""
    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
