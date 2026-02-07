from django.urls import path
from . import views

app_name = 'fbv'

urlpatterns = [
    path('', views.Home, name='home'),
    path('js', views.Js, name='js'),
    path('js2', views.Js2, name="js2"),
    path('js3', views.Js3, name="js3"),
    path('loginpage/', views.login_page, name='login_page'),
    path('login/', views.login_view, name='login'),
    path('login_fbv/', views.Login_FBV, name='login_fbv'),
    path('logout_fbv/', views.Logout_FBV, name='logout_fbv'),
    path('register_fbv', views.Register_FBV, name='register_fbv'),
    path('createmember/', views.create_member, name='createmember'),
    path('addperm/', views.add_Permission, name='addperm'),
    path('addgroup', views.Add_Group, name='addgroup'),
    path('webhook/', views.webhook, name='webhook'),
    path('paymentcallback/', views.payment_callback, name='paymentcallback'),
]
