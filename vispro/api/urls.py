from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
# jwt authertication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

router = DefaultRouter()
router.register(r'normalviewset', views.Normalviewset, basename='filtered-members')
router.register(r'modelviewset', views.Modelviewset, basename='members')
router.register(r'readonlyviewset', views.Readonlyviewset, basename='memreadonlyviewset')
router.register(r'memberviewset2', views.MemberViewSet, basename='memberviewset2')
router.register(r'genericviewset', views.Genericviewset, basename='genericviewset')

app_name = 'api'

urlpatterns = [
    # Api View
    path('apihome/', views.home, name='apihome'),
    path('mem/', views.Members, name='members'),
    path('apimem', views.Api_Mem, name='api_mem_list'),
    path('api_mem/<int:id>/', views.Api_Mem, name='api_mem_detail'),
    path('update_api/<int:id>/', views.update_api_member, name = 'update_api'),
    path('classapi/', views.Class_Apimembers_List.as_view(), name='classapi'),
    path('classapidetail/<int:pk>/', views.Class_Apimembers_Edit.as_view(), name='classapidetail'),
    path('cachevis/', views.Cache_vis.as_view(), name='cachevis'),
    path('dapiview/', views.DashboardAPIView.as_view(), name= 'dashboardapiview'),
    # Generic ApiView
    path('agegenericsview/', views.AgegroupGenerics_MyView.as_view(), name='agegenericsview'),
    path('agegenericsview/<int:pk>/', views.AgegroupGenerics_MyView_Detail.as_view(), name='agegroup-detail'),
    path('detailgenericsview/', views.DetailGenerics_MyView.as_view(), name='detailgenericsview'),
    path('detailgenericsview/<int:pk>/', views.DetailGenerics_MyView_Detail.as_view(), name='detailgenericviewdetail'),
    path('', views.Generics_MyView.as_view(), name='genericsview'),
    path('genericsview/<int:pk>/', views.Generics_MyView_Detail.as_view(), name='genericsview_detail'),
    path('memgenapi/', views.MembersGenericAPIView.as_view(), name='memgen'),
    path('memgenapi/<int:pk>/', views.MembersDetailGenericAPIView.as_view(), name='memdetagen'),
    path('memlistcreate/', views.MemListCreateAPIView.as_view()),
    path('memretdele/<int:pk>/', views.MemRetrieveUpdateDestroyAPIView.as_view()),
    path('memlistapiview/', views.Memlistapiview.as_view()),
    path('memcreateapiview/', views.MemCreateApiView.as_view()),
    path('memretriveapiview/<int:pk>/', views.MemRetriveApiView.as_view()),
    path('memupdateapiview/<int:pk>/', views.MemUpdateAPIView.as_view()),
    path('memdestroyapiview/<int:pk>/', views.MemDestroyAPIView.as_view()),
    path('memretriveupdateapiview/<int:pk>/', views.MemRetrieveUpdateAPIView.as_view()),
    path('memretrivedestroyapiview/<int:pk>/', views.MemRetrieveDestroyAPIView.as_view()),

    # authenticaion urls
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # jwt authentication
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # jwt authentication

    path('logingenericapiview/', views.LoginGenericAPIView.as_view(), name='logingenericapiview'),
    path('loginapi/', views.LoginAPIView.as_view()),
    path('logoutapiview/', views.LogoutApiView.as_view()),
    path('logoutgenericapiview/', views.LogoutGenericApiView.as_view()),
    path('registerview/', views.RegisterView.as_view(), name='registerview'),
    path('updateview/<int:pk>/', views.UpdateUserView.as_view(), name='updateview'),
    path('tokenapi/', views.TokenAPI.as_view(), name='tokenapi'),
    path('sloginview/', views.Sessionlogin_view, name='sloginview'),
    path('slogoutview/', views.Sessionlogout_view, name='slogoutview'),
    path('tlogin/', obtain_auth_token),
    path('tloginview/', views.token_login, name='tloginview'),
    path('tlogoutview/', views.token_logout, name='tlogoutview'),
    path('jwtlogoutview/', views.jwtlogout_view, name='jwtlogoutview'),

    # spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),

]
urlpatterns += router.urls