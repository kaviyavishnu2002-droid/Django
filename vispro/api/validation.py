import os
from rest_framework import serializers

def validate_photo(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise serializers.ValidationError("Image size must be under 2MB")

def validate_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in allowed:
        raise serializers.ValidationError("Invalid file type")

"""
examples

class MemberSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        required=False,
        validators=[validate_photo]
    )
    document = serializers.FileField(
        required=False,
        validators=[validate_extension]
    )

    class Meta:
        model = Member
        fields = '__all__'
"""