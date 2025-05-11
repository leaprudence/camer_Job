from django.urls import path
from .views import register , login_view , forgot , reset , profile , check_user_exists

urlpatterns = [
    path('register', register, name= 'register'),
    path('login', login_view, name='login'),
    path('forgot' , forgot , name= 'forgot' ),
    path('check' , check_user_exists, name= 'check' ),
    path('reset/<str:token>/' , reset , name='reset'),
    path('profile' , profile , name='profile'),
]
