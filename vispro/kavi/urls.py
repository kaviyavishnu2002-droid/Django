from django.urls import path
from . import views

app_name = 'kavi'

urlpatterns = [
    path('', views.home, name= 'home'),
    path('register/', views.register, name= 'register'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name='logout'),
    path('posts/', views.posts, name= 'posts'),
    path('add_post', views.add_post, name='add_post'),
    path('post_details/<int:post_id>/', views.post_details, name= 'post_details'),
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('forgot_password', views.forgot_password, name= 'forgot_password'),
    path('reset_password/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path('add_category', views.add_category, name='add_category'),
    path('article', views.article, name='article'),
    path('vis_history', views.vis_history, name = 'vis_history'),
    path('Vis_Member_Create/', views.Vis_Create, name='Vis_Create'),
    path('Vis_List', views.Vis_List, name='vis_list'),
    path('vis_delete/<int:id>/', views.vis_delete, name = 'vis_delete'),
    path('mom_list', views.Mom_List, name='mom_list'),
    path('mom_create/', views.Mom_Create, name='mom_create'),
    path('mom_edit/<int:id>/', views.mom_edit, name='mom_edit'),
    path('dad_list', views.Dad_List, name='dad_list'),
    path('dad_create/', views.Dad_Create, name='dad_create'),
    path('dad_edit/<int:id>/', views.dad_edit, name='dad_edit'),
    path('edit_member/<int:id>', views.Edit_Member, name='edit_member'),
]