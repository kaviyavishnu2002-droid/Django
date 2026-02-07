from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

app_name = 'cbv'

urlpatterns = [
    # home page url
    path('', views.Home.as_view(), name= 'home'),
    path('formview', views.formsview.as_view(), name = 'formsview'),
    path('hello', views.hello, name='hello'),
    path('item', views.item, name = 'item'),
    # members urls
    path('member_form', views.Member_From.as_view(), name='member_form'),
    path('members_list', views.Members_list.as_view(), name='members_list'),
    path('member_detail/<slug:slug>/detail', views.Member_Details.as_view(), name = 'member_detail'),
    path('member_edit/<slug:slug>/edit', views.Member_Edit.as_view(), name='member_edit'),
    path('member_delete/<slug:slug>/delete', views.Member_Delete.as_view(), name='member_delete'),
    # age group urls
    path('age_create', views.Age_Group_Create.as_view(), name='age_create'),
    path('age_list', views.Age_Group_List.as_view(), name='age_list'),
    path('age_edit/<slug:slug>/edit', views.Age_Group_Edit.as_view(), name='age_edit'),
    path('age_delete/<slug:slug>/delete', views.Age_Group_Delete.as_view(), name='age_delete'),
    # custom login/logout
    path('login_cbv', views.Login_View.as_view(), name='login_cbv'),
    path('logout_cbv', views.Logout_view.as_view(), name = 'logout_cbv'),
    path('register_cbv', views.Register_view.as_view(), name = 'register_cbv'),
    path('remove_user/<int:pk>/delete', views.Remove_User.as_view(), name='remove_user'),
    # get and post
    path('get_post', views.Get_Post.as_view(), name='get_post'),
    # Django built-in auth views with unique paths and names
    path('auth_login', LoginView.as_view(template_name='cbv/authenticate/login.html'), name='auth_login'),
    path('auth_logout', LogoutView.as_view(), name='auth_logout'),
    path('password_change', PasswordChangeView.as_view(template_name='cbv/authenticate/password_change.html'), name='password_change'),
    path('password_change_done', PasswordChangeDoneView.as_view(template_name='cbv/authenticate/password_change_done.html'), name='password_change_done'),
    path('password_reset', PasswordResetView.as_view(template_name='cbv/authenticate/password_reset.html'), name='password_reset'),
    path('password_reset_done', PasswordResetDoneView.as_view(template_name='cbv/authenticate/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='cbv/authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(template_name='cbv/authenticate/password_reset_complete.html'), name='password_reset_complete'),
    path('profileupdate', views.ProfileUpdateView.as_view(), name='profileupdate')
]
