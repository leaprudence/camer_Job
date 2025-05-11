from django.shortcuts import redirect
from django.contrib import messages

class ResetTokenMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'reset-password' in request.path:
            token = request.resolver_match.kwargs.get('token', None)
            if not token:
                messages.error(request, "Token invalide ou manquant.")
                return redirect('forgot_password')

        response = self.get_response(request)
        return response