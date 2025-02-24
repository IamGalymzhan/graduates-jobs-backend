from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Skill

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "full_name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.full_name,
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
    skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(), required=False
    )  # ✅ Accepts only existing skill IDs

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "profile_picture", "education", "skills", "status", "resume"]

    def update(self, instance, validated_data):
        skills = self.context["request"].data.getlist("skills")  # ✅ Extract skills manually

        # Convert skill IDs to integers
        skills = [int(skill) for skill in skills if skill.isdigit()]

        instance = super().update(instance, validated_data)  # ✅ Update other fields

        if skills:
            instance.skills.set(skills)  # ✅ Correctly update ManyToMany field

        return instance
