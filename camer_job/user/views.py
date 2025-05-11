from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User , Role , Profile
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.crypto import get_random_string

from django.http import JsonResponse


def check_user_exists(request):
    print(request)  # Juste pour montrer que l'objet est utilisé
    user_exists = User.objects.exists()  # Vérifie si des utilisateurs existent
    return JsonResponse({'exists': user_exists})

def register(request):
    if request.method == 'POST':
      name = request.POST.get('name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      image = request.POST.get('image')
      matricule = request.POST.get('matricule')
      role_id = request.POST.get('role')
      
      # verifie si le mot de passe existe deja
      if User.objects.filter(matricule=matricule).exists():
         
          return render(request, 'user/register.html', {'error': 'Ce matricule existe déjà.'})# Vérifie la valeur de role_id
      
      if User.objects.filter(email=email).exists():
       
        return render(request, 'user/register.html', {'error': 'Cet email existe déjà.'})
     # hacher le mot de passe
      password_confirm = request.POST.get('password-confirm')
      if password != password_confirm:
      
       return render(request, 'user/register.html', {'error': 'Les mots de passe ne correspondent pas.'})
     
      hashed_password = make_password(password)
     
      role = Role.objects.get(id=role_id)
      
   
      donnees = User (name = name , email = email , password = hashed_password , image = image , matricule = matricule , role = role )
     
      donnees.save()
      subject = "Bienvenue sur camer_job"
      message = f"Bienvenue, {donnees.name} !"
      from_email = settings.EMAIL_HOST_USER
      to_list = [donnees.email]
      send_mail(subject , message , from_email , to_list) 
      profil = Profile.objects.create(user = donnees)
      profil.save()
      print("✅ Utilisateur enregistré, on redirige vers login")
      return redirect("login")
    return render (request , 'user/register.html')
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # Vérifiez le mot de passe haché
                login(request, user)
                return redirect('index')  # Rediriger vers la page d'accueil
            else:
                return render(request, 'user/login.html', {'error': 'Mot de passe invalide.'})
        except User.DoesNotExist:
            return render(request, 'user/login.html', {'error': 'Utilisateur non trouvé.'})

    return render(request, 'user/login.html')



def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Générer un token unique (par exemple, une chaîne aléatoire)
            token = get_random_string(32)
            user.profile.reset_token = token  # Stockez ce token dans un modèle lié à l'utilisateur
            user.profile.token_created_at = timezone.now()  # Set the time of token creation
            user.profile.save()
            # Lien de réinitialisation
            reset_link = f"{request.scheme}://{request.get_host()}/reset/{token}/"
            # Envoyer l'email
            send_mail(
                'Réinitialisation du mot de passe',
                f'Cliquez sur ce lien pour réinitialiser votre mot de passye : {reset_link}',
                'noreply@user.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Un e-mail de réinitialisation a été envoyé.")

        else:
            messages.error(request, "Aucun utilisateur trouvé avec cet e-mail.")
        
            return redirect('forgot')

    return render(request, 'user/forgot_password.html')


def reset(request, token):
    
    profile = get_object_or_404(Profile, reset_token=token)
    

    # Vérifier si le token a expiré
    if profile.is_token_expired():
        messages.error(request, "Le lien de réinitialisation a expiré. Veuillez recommencer.")
        return redirect('forgot')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = profile.user
            user.set_password(new_password)
            user.save()

            profile.reset_token = None
            profile.token_created_at = None
            profile.save()

            messages.success(request, "Mot de passe réinitialisé avec succès.")
            return redirect('login')
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")

    return render(request, 'user/reset_password.html')

def profile(request):
    return render(request , 'user/profile.html')