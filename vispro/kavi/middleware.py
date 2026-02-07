from django.urls import reverse
from django.shortcuts import redirect

class authredirectmiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            paths_to_redirect = [reverse('kavi:login'), reverse('kavi:register')]

            if request.path in paths_to_redirect:
                return redirect(reverse('kavi:home'))
            
        elif not request.user.is_authenticated:
            paths_to_redirect = [reverse('kavi:posts')]

            if request.path in paths_to_redirect:
                return redirect(reverse('kavi:login'))
            
        response = self.get_response(request)
        return response