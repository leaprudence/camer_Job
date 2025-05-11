from django.urls import path
from .views import index, home, myJobs  

urlpatterns = [
    path('index', index, name='index'),
    path('home', home, name= 'home'),
    path('my_jobs', myJobs, name ='myJobs' )
]
