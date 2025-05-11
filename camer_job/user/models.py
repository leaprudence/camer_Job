from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from datetime import datetime , timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255)

    
class User(models.Model):
    name = models.CharField(max_length=150 , default = 'Inconnu') # Ajout du champ username
    email = models.EmailField(unique=True, default='no_email@mail.com')
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', default='no_image')
    matricule = models.CharField(max_length=22 , unique=True ,null= True )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='users'  
    )
    last_login = models.DateTimeField(null=True, blank=True)  # Ajoutez ce champ
    
    def __str__(self):
        return self.name
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    def is_token_expired(self):
        if self.token_created_at:
            expiration_time = self.token_created_at + timedelta(hours=1)  # Token valide 1 heure
            return now() > expiration_time
        return True
    

