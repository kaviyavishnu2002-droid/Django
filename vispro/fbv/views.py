from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import (
    Authentication_Form, Normal_LoginForm, 
    Normal_Register_Form, Usercreation_Form
)
from kavi.models import Profile
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from cbv.forms import Register_Form
from django.db import transaction
import logging
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()

logger = logging.getLogger(__name__) # django / django.request / app name

def Home(request):
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")

    if request.user.is_authenticated:
        logger.info("Authenticated user accessed home page")
        return HttpResponse("User is authenticated")

    logger.warning("Anonymous user accessed home page")
    return HttpResponse("Welcome to home page")

def Js(request):
    return render(request, "fbv/js.html", {'user':request.user, 'title':'vis world'})

def Js2(request):
    return render(request, "fbv/js2.html")

def Js3(request):
    return render(request, "fbv/js3.html")

@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse(
                {"error": "Invalid credentials"},
                status=401
            )

        login(request, user)

        return JsonResponse({
            "message": "Login successful",
            "user": user.username
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )

def login_page(request):
    return render(request, "fbv/login.html")

def Login_FBV(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email, password = password)
        if user:
            login(request, user)
            messages.success(request, 'login successfully and welcome to vis territory')
            return redirect('cbv:home')
        else:
            messages.error(request, 'invalid username or password')

    form = Authentication_Form()
    if request.method == 'POST':
        form = Authentication_Form(request, data=request.POST)  
                            # for authenticationform
        if form.is_valid():
            user = form.get_user()  # get_user()
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('cbv:home')
        else:
            messages.error(request, 'login failed')

    return render(request, 'fbv/authenticate/login.html',{'form':form})

def Logout_FBV(request):
    logout(request)
    return redirect('cbv:home')

def Register_FBV(request):
    if request.method == 'POST':
        form = Register_Form(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.first_name = 'vishnu'
                    user.save()

                    if len(user.username) <= 5:
                        raise ValidationError("length of username is must over then 5")
                        # raise Exception("Invalid username")
                        # transaction.set_rollback(True) → works but dangerous

                messages.success(request, 'Registration successful')
                return redirect('fbv:home')
            except ValidationError as e:
                messages.error(request, str(e))
            # except Exception:
            #     messages.error(request, 'Registration rolled back')

        else:
            messages.error(request, 'registration failed')
    else:
        form = Register_Form()
    return render(request, 'fbv/authenticate/login.html', {'form':form})

@permission_required('api.add_apimembers', raise_exception=True)
def create_member(request):
    pass

def add_Permission(request):
    perm = Permission.objects.get(codename='add_book')
    request.user.user_permissions.add(perm)

def Add_Group(request):
    editors = Group.objects.get(name='Editors')
    request.user.groups.add(editors)

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        return HttpResponse("Webhook received")

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        return HttpResponse("Payment processed")

# A request comes to /webhook/
# Django sees @csrf_exempt
# Django skips CSRF validation
# Request is accepted, even without CSRF token

@transaction.atomic   # for rollback method
def view(request):     # if any error appeared, will function do rollback
    User.objects.create(...)
    Profile.objects.create(...)
    raise Exception()

# Explicit Savepoints (Advanced)
def view(request):
    with transaction.atomic():

        User.objects.create(...)

        sid = transaction.savepoint()

        try:
            Profile.objects.create(...)

        except Exception:
            transaction.savepoint_rollback(sid)


# Most Django code is synchronous:ORM, Admin, Signals, Management commands
# Solution: async_to_sync
# users = await sync_to_async(User.objects.all)()

from asgiref.sync import async_to_sync, sync_to_async
# result = async_to_sync(Js)()

# Thread Sensitivity (Very Important)
@sync_to_async(thread_sensitive=True)
def get_user():
    return User.objects.get(id=1)

import httpx   # pip install httpx

async def httpxfileview(request):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.example.com")

import aiofiles # pip install aiofiles

async def Aiofilesview(request):
    async with aiofiles.open("file.txt") as f:
        data = await f.read()

