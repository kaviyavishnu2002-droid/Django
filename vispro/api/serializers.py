import os
from rest_framework import serializers
from cbv.models import Detail,Age_Group
from .models import Api_Members
from kavi.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class Age_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Age_Group
        fields = '__all__'
        read_only_fields = ['slug']  # Cannot be set via POST / PUT / PATCH

class Members_Serializer(serializers.ModelSerializer):
    age_range = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:agegroup-detail'
        # lookup_field = 'slug' , if there is lookup_field = 'slug' in views
    )
    # age_range = serializers.StringRelatedField(read_only = True)  # StringRelatedField (READ only)
    # age_range = Age_Serializer(read_only=True)      # nested serializer method and show all details
    age_range_id = serializers.PrimaryKeyRelatedField(   # PrimaryKeyRelatedField (WRITE only)
        queryset=Age_Group.objects.all(),
        source='age_range',
        write_only=True
    )
    with_about = serializers.SerializerMethodField()

    class Meta:
        model = Detail
        fields = '__all__' # ['id', 'name', 'user', 'age', 'age_range', 'age_range_id', 'with_about']
        read_only_fields = ['slug']
    
    def get_with_about(self, obj):
        return f'{obj.name}-{obj.age}'

    def validate_age(self, value):   # validate age is triger create or update[post, pauch, put].
        if value < 8:
            raise serializers.ValidationError("Age cannot be within 8")
        return value

class Api_Srializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required = True, 
        min_length = 3, 
        max_length = 50, 
        error_messages={
            "required": "Name is mandatory",
            "min_length": "Name must contain at least 3 characters",
            "max_length": "Name must contain within 50 characters"
        }
    )
    user = serializers.StringRelatedField()
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'user',
        write_only = True
    )

    class Meta:
        model = Api_Members
        fields = '__all__'
        read_only_fields = ['slug']
        
    def validate_document(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        allowed = ['.jpg', '.jpeg', '.png', '.pdf']

        if ext not in allowed:
            raise serializers.ValidationError("Invalid file type")

        return value

class Api_Srializer2(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Api_Members
        fields = ['user', 'name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class tokenapiserializer(serializers.Serializer):
    username = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'city']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'password']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.bio = profile_data.get('bio', profile.bio)
            profile.city = profile_data.get('city', profile.city)
            profile.save()
        return instance
