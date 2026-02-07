from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

class authredirectmiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.custom_value = "Injected by middleware"
        if request.user.is_authenticated:
            paths_to_redirect = [reverse('cbv:login_cbv'), reverse('cbv:register_cbv'), reverse('fbv:login_fbv')]

            if request.path in paths_to_redirect:
                return redirect(reverse('cbv:home'))
            
        elif not request.user.is_authenticated:
            paths_to_redirect = [reverse('cbv:members_list')]

            if request.path in paths_to_redirect:
                return redirect(reverse('cbv:login_cbv'))
        
        blocked_ips = ['192.168.1.10']

        ip = (
            request.META.get('HTTP_X_FORWARDED_FOR', '')
            .split(',')[0]
            or request.META.get('REMOTE_ADDR')
        )
        request.ip = ip

        if ip in blocked_ips:
            return HttpResponseForbidden("Access Denied")
        
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse("Site under maintenance", status = 503)
        
        response = self.get_response(request)
        return response
