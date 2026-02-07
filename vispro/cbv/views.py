# General modules
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy

# CBV Modules
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import CreateView,ListView, FormView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

# decorators 
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# local modules
from .models import Age_Group, Detail, Item, Book
from .forms import (
    AgeGroupForm,Members_form, Register_Form, LoginForm, 
    HomeForm, UserUpdateForm, item_form, items_form, book_form, books_form
)
from cbv.pagination import advanced_paginate

# Authentication modules
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Max, Min, Avg, Count, Sum, F, Q, OuterRef, Subquery

# Create your views here.
class Home(TemplateView):
    template_name = 'cbv/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vis Territory'
        context['middle'] = getattr(self.request, 'ip', None)  
        context['lesson'] = '10 over'
        # getattr method (objest, attribute name, default name)
        return context
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'cbv/home.html'
        return 'cbv/home2.html'

class formsview(View):
    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request, 'cbv/member_create.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = HomeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age= form.cleaned_data['age']
            return HttpResponse(f'Name:{name} and Age:{age}')
        return render(request, 'cbv/member_create.html', {'form':form})

def item(request):
    item_fo = item_form()
    items_fo = items_form()
    book_fo = book_form()
    books_fo = books_form()
    return render(request, 'cbv/item.html', {'item_fo':item_fo, 'items_fo': items_fo, 'book_fo':book_fo, 'books_fo':books_fo})

@permission_required('cbv.can_publish_detail', raise_exception=True)
def hello(request):
    return HttpResponse('hello')

def handler403(request, exception=None):
    return render(request, 'cbv/403.html', status=403)

def handler404(request, exception=None):
    return render(request, 'cbv/404.html', status=404)

@method_decorator(csrf_exempt, name='dispatch')
class Get_Post(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "GET request successful"})

    def post(self, request, *args, **kwargs):
        return JsonResponse({"message": "POST request successful"})
    
    def put(self, request, *args, **kwargs):
        return JsonResponse({"message": "Put request successful"})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({"message": "Delete request successful"})
    
    def patch(self, request, *args, **kwargs):
        return JsonResponse({'message':'patch request successful'})
    
    def head(self, request, *args, **kwargs):
        return JsonResponse({"message": "Head request successful"})
    
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Allow'] = 'GET, POST, PUT'
        response['Content-Type'] = 'application/json'
        return response

class Age_Group_Create_View(CreateView):
    template_name = 'cbv/age_create.html'
    permission_required = 'cbv.can_publish_detail'
    model = Age_Group
    form_class = AgeGroupForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Age Group'
        return context
    
class Member_From(SuccessMessageMixin, CreateView):
    template_name = 'cbv/member_create.html'
    model = Detail
    form_class = Members_form
    success_message = 'form creation succeded'
    
    def has_permission(self):
        return self.request.user.has_perm('cbv.can_approve_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Members Group'
        return context
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        form.instance.user = self.request.user
        messages.success(self.request, f'{name} is added in vis territory')
        age = form.cleaned_data["age"]
        if age <= 18:
            messages.warning(self.request, f'your age is {age}. not 18+')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'form is invalid please cureptet')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('cbv:members_list')

class Members_list(ListView):
    template_name = 'cbv/members.html'
    model = Detail
    context_object_name = 'Members'
    ordering = ['-is_active']
    paginate_by = None  # disable Django default

    # select_related (ForeignKey, OneToOne)
    # Member = Detail.objects.select_related('User')
    # prefetch_related (ManyToMany, Reverse Relations)
    # books = Detail.objects.prefetch_related('categories')
    # queryset = Detail.objects.select_related('author')\.prefetch_related('categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = self.request.GET.get("order", "")
        context["current_order"] = current_order
        context['title'] = 'Members'
        context['item'] = Item.objects.all()
        context['book'] = Book.objects.all()
        context['aggre'] = Detail.active.aggregate(
            avg_age=Avg('age'),
            max_age=Max('age'),
            min_age=Min('age'),
            total_age=Sum('age'),
            totel_members=Count('id')
        )
        context['anno'] = Detail.active.annotate(
            ageten = F('age')+10
        )
        context['annoage'] = Detail.active.values('grade').annotate(
            totalage = Sum('age')
        )
        context['qset'] = Detail.active.filter((Q(age__gte=24)&Q(age__lte=50))|Q(grade='b'))
        context['middleware_custom_value']= self.request.custom_value
        pagination = advanced_paginate(
            request=self.request,  queryset=self.get_queryset(),
            page_size=10,  page_range=2
        )
        context.update(pagination)
        context['products'] = pagination['page_obj']
        return context
    
    def get_queryset(self):
        queryset = Detail.objects.all()
        order = self.request.GET.get("order")
        if order:
            queryset = queryset.order_by(order)
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class Member_Details(DetailView):
    template_name = 'cbv/members_detail.html'
    model = Detail
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self, obj = None):
        obj = super().get_object(obj)
        if obj.user == self.request.user:
            return obj
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'detail view'
        return context
    
    def get_template_names(self):
        obj = self.get_object()
        return ['cbv/members_detail.html']

class Member_Edit(UpdateView):
    template_name = 'cbv/member_create.html'
    model = Detail
    form_class = Members_form
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy("cbv:members_list")
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Member Edit"
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj
    
class Member_Delete(DeleteView):
    model = Detail
    template_name = 'cbv/confirm_delete.html'
    success_url = reverse_lazy('cbv:members_list')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'member deleted succesfuly')
        return super().dispatch(request, *args, **kwargs)

class Age_Group_Create(CreateView):
    template_name = 'cbv/member_create.html'
    model = Age_Group
    form_class = AgeGroupForm
    success_url = reverse_lazy('cbv:age_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Age Group Create'
        return context

class Age_Group_List(ListView):
    template_name = 'cbv/age_group.html'
    model = Age_Group
    context_object_name = 'age_group'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Age Groups'
        return context
    
class Age_Group_Edit(UpdateView):
    template_name = 'cbv/member_create.html'
    model = Age_Group
    form_class = AgeGroupForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy("cbv:age_create")
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Age Group Edit"
        return context
    
class Age_Group_Delete(SuccessMessageMixin,DeleteView):
    model = Age_Group
    template_name = 'cbv/confirm_delete.html'
    success_url = reverse_lazy('cbv:age_list')
    success_message = 'one age is deleted'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'age group deleted succesfuly')
        return super().dispatch(request, *args, **kwargs)
    
class Login_View(LoginView):
    template_name = 'cbv/authenticate/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login View'
        return context
    
    def get_success_url(self):
        return reverse_lazy('cbv:home')

class Logout_view(LogoutView):
    next_page = reverse_lazy('cbv:home')

class Register_view(SuccessMessageMixin,CreateView):
    template_name = 'cbv/member_create.html'
    model = User
    form_class = Register_Form
    success_message = 'Registration succeded'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context
    
    def get_success_url(self):
        return reverse_lazy('cbv:login_cbv')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'cbv/member_create.html'
    success_url = reverse_lazy('cbv:home')

    def get_object(self):
        return self.request.user

class Remove_User(DeleteView):
    model = User
    template_name = 'cbv/confirm_delete.html'
    success_url = reverse_lazy('cbv:home')
