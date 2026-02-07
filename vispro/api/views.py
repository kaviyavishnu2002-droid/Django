# DRF Common Methods
from django.shortcuts import render, redirect
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import  throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

# imports
from api.pagination import CustomResponsePagination
from cbv.models import Detail, Age_Group
from .serializers import (
    Members_Serializer, Age_Serializer, Api_Srializer, 
    Api_Srializer2, LoginSerializer, LogoutSerializer, RegisterSerializer, UserSerializer
)
from .models import Api_Members, ArchivedOrder
from .permissions import IsOwnerOnly, IsAdminUser
from .throttle import RoleBasedThrottle, BurstUserThrottle, CustomIPThrottle
from .utils import success_response, error_response

# authentication and authorization
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAdminUser, 
    IsAuthenticatedOrReadOnly, DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    DjangoObjectPermissions, SAFE_METHODS,
    BasePermission
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

#  Methods
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,
    DestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ViewSet,ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# api view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#  @throttle_classes([UserRateThrottle])
def home(request):
    version = request.version
    return Response(
        {'message':f'username:{request.user.username}, '
               f'staff:{request.user.is_staff}, '
               f'superuser:{request.user.is_superuser}, '
               f'version:{version}'})
'''
    if version == 'v1':
        return Response({"name": "Vishnu"})
    return Response({"first_name": "Vishnu", "last_name": "Kumar"})'''

@api_view(['GET','POST'])
def Members(request):
    if request.method == 'GET':
        detail = Detail.objects.all()
        models = Members_Serializer(detail, many = True)
        return Response(models.data)
    elif request.method == 'POST':
        serializer = Members_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST', 'PUT', 'PATCH', 'DELETE'])
def Api_Mem(request, id = None):
    if request.method == 'GET':
        if not id:
            quiery_set = Api_Members.objects.all()
            serializer = Api_Srializer(quiery_set, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                quiery_set = Api_Members.objects.get(id = id)
            except Api_Members.DoesNotExist:
                return Response(
                    {"error": "Member not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = Api_Srializer(quiery_set)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        serializer = Api_Srializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        try:
            quiery_set = Api_Members.objects.get(id = id)
        except Api_Members.DoesNotExist:
            return Response(
                {'message':'objest does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = Api_Srializer(quiery_set, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        try:
            quiery_set = Api_Members.objects.get(id = id)
        except Api_Members.DoesNotExist:
            return Response(
                {'message':'objest does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = Api_Srializer(quiery_set, data = request.data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            quiery_set = Api_Members.objects.get(id = id)
        except Api_Members.DoesNotExist:
            return Response(
                {'message':'objest does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        quiery_set.delete()
        return Response({'message':f'{quiery_set.name} is deleted'}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'PUT', 'PATCH'])
def update_api_member(request, id):
    if request.method == 'GET':
        queryset = Api_Members.objects.all()
        serializer = Api_Srializer(queryset, many = True)
        return Response(serializer.data)
    try:
        queryset = Api_Members.objects.get(id=id)
    except Api_Members.DoesNotExist:
        return Response(
            {'message': 'Object does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = Api_Srializer(
        queryset,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""ApiView"""
@method_decorator(cache_page(60 * 5), name='get')
class Class_Apimembers_List(APIView):
    def get(self, request):
        queryset = Api_Members.objects.all()
        serializer = Api_Srializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Api_Srializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Student created successfully",
                status_code=201
            )
        return error_response(
            message="Validation failed",
            errors=serializer.errors
        )
    
class Class_Apimembers_Edit(APIView):
    def get_object(self, pk):
        try:
            return Api_Members.objects.get(pk = pk)
        except Api_Members.DoesNotExist:
            return None
    
    def get(self, request, pk):
        member = self.get_object(pk)
        if not member:
            return Response({'errors':'object does not exits'})
        serializer = Api_Srializer(member)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        member = self.get_object(pk)
        serializer = Api_Srializer(member, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        member = self.get_object(pk)
        serializer = Api_Srializer(member, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return Response({'message':'deleted successfull'})

class DashboardAPIView(APIView): # Per-User Caching (IMPORTANT)
    def get(self, request):
        key = f'dashboard_{request.user.id}'
    #   key = f'user_{request.user.id}_data'
    #   cache.set('key', 'value', timeout=60)
    #   cache.get('key')
    #   cache.delete('key')
    #   cache.clear()
        data = cache.get(key)
        if not data:
            data = {
                "orders": 10,
                "notifications": 3
            }
            cache.set(key, data, timeout=300)
        return Response(data)

@method_decorator(cache_page(60 * 5), name='get')
class Cache_vis(APIView):
    def get(self, request):
        return Response({"data": "vis territory"})
    
"""Generic ApiView"""
class AgegroupGenerics_MyView(GenericAPIView):
    queryset = Age_Group.objects.all()
    serializer_class = Age_Serializer

    def get(self, request):
        members = self.get_queryset()
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Student created successfully",
                status_code=201
            )
        return error_response(
            message="Validation failed",
            errors=serializer.errors
        )
    
class AgegroupGenerics_MyView_Detail(GenericAPIView):
    queryset = Age_Group.objects.all()
    serializer_class = Age_Serializer

    def get(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member)
        return Response(serializer.data)
    
    def put(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(
            member,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        member = self.get_object()
        member.delete()
        return Response(status=204)

class DetailGenerics_MyView(GenericAPIView):
    queryset = Detail.objects.all()
    serializer_class = Members_Serializer

    def get(self, request):
        members = self.get_queryset()
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailGenerics_MyView_Detail(GenericAPIView):
    throttle_scope = 'Detail-detail'
    queryset = Detail.objects.all()
    serializer_class = Members_Serializer

    def get(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member)
        return Response(serializer.data)
    
    def put(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(
            member,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        member = self.get_object()
        member.delete()
        return Response(status=204)

class Generics_MyView(GenericAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

    def get(self, request):
        members = self.get_queryset()
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Generics_MyView_Detail(GenericAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

    def get(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member)
        return Response(serializer.data)
    
    def put(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        member = self.get_object()
        serializer = self.get_serializer(
            member,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        member = self.get_object()
        member.delete()
        return Response(status=204)

class MembersGenericAPIView(GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class MembersDetailGenericAPIView(GenericAPIView,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

class MemListCreateAPIView(ListCreateAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class Memlistapiview(ListAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemCreateApiView(CreateAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemRetriveApiView(RetrieveAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemUpdateAPIView(UpdateAPIView):
    queryset = Api_Members.objects.all() # UpdateAPIView supports: PUT,PATCH
    serializer_class = Api_Srializer     # ❌ It does NOT support: GET

class MemDestroyAPIView(DestroyAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

class MemRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer

"""authentication pages"""
class LoginGenericAPIView(GenericAPIView):  # (GenericAPIView ALWAYS requires a serializer)
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"error": "User account is disabled"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK
        )

class LogoutGenericApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = RefreshToken(serializer.validated_data["refresh"])
        token.blacklist()

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        key = f'dashboard_{request.user.id}'
        data = cache.get(key)

        if not data:
            data = {
                "orders": 10,
                "notifications": 3
            }
            cache.set(key, data, timeout=300)

        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def Sessionlogin_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)   # creates session
        return Response({"message": "Login successful"})
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['GET'])
def Sessionlogout_view(request):
    logout(request)
    return Response({"message": "logout successful"})

@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})

@api_view(['POST'])
def jwtlogout_view(request):
    refresh_token = request.data.get('refresh')
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response({"message": "Logged out successfully"})

"""Model Viewset-4types""" 
class Normalviewset(ViewSet):

    def list(self, request):
        products = Api_Members.objects.all()
        serializer = Api_Srializer(products, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        product = Api_Members.objects.get(pk=pk)
        serializer = Api_Srializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = Api_Members.objects.filter(is_archived=False)
        serializer = Api_Srializer(products, many=True)
        return Response(serializer.data)

class Modelviewset(ModelViewSet):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomResponsePagination
    throttle_classes = [ScopedRateThrottle]

    def get_throttles(self):
        if self.action == 'list':
            self.throttle_scope = 'Detail'
        elif self.action == 'create':
            self.throttle_scope = 'Detail_list'
        else:
            self.throttle_scope = 'Detail_detail'
        return super().get_throttles()

    @method_decorator(cache_page(60 * 1)) # only list is cached
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Api_Members.objects.all() # filter(user = self.request.user)
        name = self.request.query_params.get('name')
        age = self.request.query_params.get('age')
        grade = self.request.query_params.get('grade')
        if name:
            queryset = queryset.filter(name__icontains= name)
        if age and age.isdigit():
            queryset = queryset.filter(age=int(age))
        if grade:
            queryset = queryset.filter(grade__icontains=grade)
        return queryset

    # which serializer class should be used for the current request.
    def get_serializer_class(self):
        '''if self.request.method == 'GET':
            return Api_Srializer2
        return Api_Srializer'''
        if self.action == 'list':
            return Api_Srializer2   # Use self.action in ViewSets, not request.method.
        elif self.action == 'retrieve':
            return Api_Srializer
        elif self.action == 'create':
            return Api_Srializer
        return Api_Srializer
        '''if self.request.version == 'v2':
            return Api_Srializer
        return Api_Srializer2'''
    
    # that runs after serializer validation but before the object is saved to the database.
    def perform_create(self, serializer):
        if Api_Members.objects.filter(
            name=serializer.validated_data['name']
        ).exists():
            raise ValidationError("this name already exists")
        serializer.save(user=self.request.user, created_at =timezone.now())
        
    # runs after validation and before saving an updated object.
    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.photo and self.request.FILES.get('photo'): # input type= file and name= photo
            instance.photo.delete(save=False)

        serializer.save(last_modified=timezone.now())
        cache.delete('Api_Members_list')

    # method executed just before an object is deleted from the database.
    def perform_destroy(self, instance): # soft delete(most common)
        ArchivedOrder.objects.create(
            action = 'archived',
            data=Api_Srializer(instance).data, # data is a json
            archived_by=self.request.user
        )
        instance.is_archived = True
        instance.save(update_fields=['is_archived'])
        cache.delete('Api_Members_list')
        
    def get_permissions(self):
        '''permission_map = {
            'create': [IsAuthenticated],
            'list': [IsAdminUser],
            'retrieve': [IsAdminUser],
            'update': [IsAdminUser],
            'partial_update': [IsAdminUser],
            'destroy': [IsAdminUser],
        }

        permission_classes = permission_map.get(
            self.action, [IsAdminUser] # isadminuser is a default, if not self.action
        )
        return [permission() for permission in permission_classes]'''
        if not self.request.method in ['GET']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            return queryset
        return queryset.filter(age__lt=30)

    # retrieving a single model instance
    def get_object(self):
        obj = super().get_object()
        if obj.is_archived:
            raise NotFound("Archived item")
        return obj

    @action(detail=False, methods=['get'])
    def ages(self, request):                 # detail for all data
        students = self.get_queryset().values('name', 'age')
        return Response(students)
    @action(detail=True, methods=['get'])
    def age(self, request, pk=None):      # detail for one data
        student = self.get_object()
        return Response({'name': student.name, 'age': student.age})

class Readonlyviewset(ReadOnlyModelViewSet):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstUserThrottle]
    filter_backends = [
        SearchFilter, # Basic Search
        DjangoFilterBackend, # Field Filtering
        OrderingFilter # 
    ] 
    filterset_fields = ['name', 'age', 'grade'] # /url/?name=Phone&grade=a
    ordering_fields = ['name', 'age'] # /url/?ordering=name,-age
    search_fields = ['name']  # /url/?search=vis
    """search_fields = ['^name']   # starts with
    search_fields = ['=name']   # exact match
    search_fields = ['@name']   # full-text search (PostgreSQL)"""

class Genericviewset(GenericViewSet):
    queryset = Api_Members.objects.all()
    serializer_class = Api_Srializer
    filter_backends = [SearchFilter]
    filterset_fields = ['name']

    def list(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
        except Api_Members.DoesNotExist:
            return Response({'message':'item not found'})
        serializer = self.get_serializer(product)
        if product:
            return Response(serializer.data)
        return Response({'message':'items does not exists'})

    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class MemberViewSet(ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = Members_Serializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False if obj.is_active else True
        obj.save(update_fields=['is_active']) # Updates only one column
        return redirect('cbv:members_list')

class TokenAPI(APIView):

    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)
