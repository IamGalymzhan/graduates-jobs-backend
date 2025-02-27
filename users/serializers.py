from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Skill

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "full_name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)  # ✅ Changed from username to email
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "company_name": user.company_name,
                "email": user.email,
                "user_type": user.user_type,
                "profile_picture": user.profile_picture.url if user.profile_picture else None,
            },
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "profile_picture", "education", "skills", "status"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["skills"] = [{"id": skill.id, "name": skill.name} for skill in instance.skills.all()]

        if request and request.resolver_match.url_name == "student-list":
            data.pop("email", None)
            data.pop("resume", None)

        return data

