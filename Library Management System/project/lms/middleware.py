# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == reverse('lms:home'):
                return redirect('lms:dashboard')
        elif request.path == reverse('lms:dashboard'):
            return redirect('lms:home')
        
        response = self.get_response(request)
        return response
