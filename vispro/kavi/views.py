from django.shortcuts import render,redirect
from .forms import RegisterForm, add_category_form,loginform, add_moviesform,forgot_passwordform, Vis_Member_Form, Mom_create_Form, Dad_Create_Form
from django.contrib import messages
from .models import movies,category, Article, Author,Vis_Members,Mom, Dad,Vis_Member_Created_Details
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.apps import apps
from django.http import HttpResponse
from django.db.models import Avg,F
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'kavi/home.html')

def add_category(request):
    if request.method=='POST':
        form = add_category_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kavi:add_category')
    else:
        form = add_category_form()
    return render(request, 'kavi/add_category.html', {'form':form})

def add_post(request):
    form = add_moviesform()
    if request.method=='POST':
        form = add_moviesform(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user= request.user
            user.save()
            return redirect('kavi:posts')
        else:
            messages.error(request, 'posts is unvalid')
    return render(request, 'kavi/add_post.html', {'form':form})

def posts(request):
    post = movies.objects.order_by('-is_published')
    return render(request, 'kavi/posts.html', {'post':post})

def post_details(request, post_id):
    if request.user and request.user.has_perm('kavi.view_movies'):
        pass
    post = movies.objects.get(id= post_id)
    return render(request, 'kavi/post_details.html', {'post':post})
    '''else:
        return redirect('kavi:home')'''

def post_edit(request, post_id):
    post = movies.objects.get(id= post_id)
    categorys = category.objects.all()
    if request.method=='POST':
        form = add_moviesform(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('kavi:post_details',post_id)
    else:
        form = add_moviesform(instance=post)
    return render(request, 'kavi/add_post.html', {'form':form, 'post':post, 'category':categorys})
    
def post_delete(request, post_id):
    post = movies.objects.get(id= post_id)
    post.delete()
    return redirect('kavi:posts')

def article(request):
    art = Article.objects.first()

    return render(request, 'kavi/article.html', {'art':art})

def Vis_List(request):
    members = Vis_Members.objects.all()
    categorys = None
    if request.method == 'POST':
        categorys, created = category.objects.get_or_create(
            name = request.POST.get('name')
        )
    all_categorys = category.objects.all()
    return render(request, 'kavi/vis_mem.html', {'members': members, 'category':categorys, "all_category":all_categorys})

def Vis_Create(request):
    if request.method == 'POST':
        form = Vis_Member_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Form saved successfully ✅")
            return redirect("kavi:vis_list")
        else:
            messages.error(request, "Form is invalid ❌ Please correct the errors below.")
    else:
        form = Vis_Member_Form()
    vis = Vis_Members.objects.all()

    return render(request, 'kavi/vis_member_create.html', {'form':form, "vis":vis})

def Edit_Member(request, id):
    post = Vis_Members.objects.get(id=id)

    if request.method == 'POST':
        form = Vis_Member_Form(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('kavi:vis_list')
        else:
            HttpResponse("form is unvalid")
    else:
        form = Vis_Member_Form(instance=post)
    return render(request, 'kavi/vis_member_create.html', {'form':form})

def vis_delete(request, id):
    vis = Vis_Members.objects.get(id = id)
    vis.delete()
    messages.success(request, 'deleted successed')
    return redirect("kavi:vis_list")

def vis_history(request):
    history = Vis_Member_Created_Details.objects.all().order_by('updated_at')
    return render(request, 'kavi/vis_history.html', {'history':history})

def Mom_List(request):
    members = Mom.objects.all()
    return render(request, 'kavi/Mom.html', {'members': members})

def Mom_Create(request):
    if request.method == 'POST':
        form = Mom_create_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "form saving is success")
        else:
            messages.error(request, "form is unvalid")
    else:
        form = Mom_create_Form()
    mom = Mom.objects.filter(
        salary__gt=10000,  marrital_status=True
        ).exclude(salary__gt=20000
        ).order_by('-name').only('name')
    ids = mom.values_list('id', flat=True)
    
    avg_salary_mom = Mom.objects.aggregate(avg_salary =Avg('salary'))
    half_salary = Mom.objects.annotate(half = F('salary')/2)

    return render(request, 'kavi/mom_create.html', {
        'form':form, 'mom':mom, 'ids':ids,
        'avg_sal':avg_salary_mom, 'half_salary':half_salary
        })

def mom_edit(request, id):
    mom = Mom.objects.get(id = id)
    return render(request, 'kavi/mom_detail.html', {'mom':mom})

def Dad_List(request):
    members = Dad.objects.all()
    return render(request, 'kavi/Dad.html', {'members': members})

def Dad_Create(request):
    if request.method == 'POST':
        form = Dad_Create_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "form saving is success")
        else:
            messages.error(request, "form is unvalid")
    else:
        form = Dad_Create_Form()
    dad = Dad.objects.all()
    return render(request, 'kavi/dad_create.html', {'form':form, "dad":dad})

def dad_edit(request, id):
    dad = Dad.objects.get(id = id)
    return render(request, 'kavi/dad_detail.html', {'dad':dad})


def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            readers_group,created = Group.objects.get_or_create(name = 'Readers')
            user.groups.add(readers_group)
            print('Register Success')
            messages.success(request, 'Regisration is success')
            return redirect('kavi:login')
        else:
            messages.error(request, 'form is unvalid')
    else:
        form = RegisterForm()
    return render(request, 'kavi/register.html', {'form':form})

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password= password)
        if user:
            auth_login(request, user)
            messages.success(request, 'login succesfull')
            return redirect('kavi:home')
        else:
            messages.error(request, 'username and password do not match')

    return render(request, 'kavi/login.html')

def logout(request):
    auth_logout(request)
    return redirect('kavi:login')

def forgot_password(request):
    form = forgot_passwordform()

    if request.method=='POST':
        form = forgot_passwordform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domin = current_site.domain
            subject = 'reset password requested'
            message = render_to_string('kavi/resetpasswordemail.html', {
                'domin':domin,
                'uid':uid,
                'token':token
            })
            send_mail(subject, message, 'noreply@example.com', [email])
            messages.success(request, 'email has been sent')

    return render(request, 'kavi/forgot_password.html', {'form':form})

def reset_password(request):
    '''if request.method=='POST':
        form = reset_passwordform(request.POST)
        if form.is_valid():
            new_pass = form.cleaned_data['new_pass']
            try:
                uid = urlsafe_base64_decode(uid64)
                user = User.objects.get(pk= uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
        default_token_generator.check_token(user, token)'''
    pass