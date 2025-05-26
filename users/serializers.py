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
        fields = ["id", "full_name", "email", "profile_picture", "education", "skills", "status", "resume"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["skills"] = [{"id": skill.id, "name": skill.name} for skill in instance.skills.all()]

        if request and request.resolver_match.url_name == "student-list":
            data.pop("email", None)
            data.pop("resume", None)

        return data

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "email", "company_name", "company_website", "company_description"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

class UniversalProfileSerializer(serializers.ModelSerializer):
    """
    A universal serializer that handles both student and employer profiles
    based on the user type
    """
    # Override company_website to handle empty strings
    company_website = serializers.URLField(required=False, allow_blank=True)
    # Make email read-only
    email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            "id", "full_name", "email", "user_type",
            # Student fields
            "profile_picture", "education", "skills", "status", "resume",
            # Employer fields  
            "company_name", "company_website", "company_description"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Add skills representation for students
        if instance.user_type == "student":
            data["skills"] = [{"id": skill.id, "name": skill.name} for skill in instance.skills.all()]
            # Remove employer fields for students
            data.pop("company_name", None)
            data.pop("company_website", None) 
            data.pop("company_description", None)
        else:
            # Remove student fields for employers
            data.pop("profile_picture", None)
            data.pop("education", None)
            data.pop("skills", None)
            data.pop("status", None)
            data.pop("resume", None)

        return data

    def validate_company_website(self, value):
        """
        Custom validation for company_website to handle empty strings
        """
        if value == "":
            return None
        return value

    def validate(self, data):
        """
        Custom validation to ensure only relevant fields are validated for each user type
        """
        user = self.instance
        if user:
            if user.user_type == "student":
                # Remove employer fields from validation for students
                data.pop("company_name", None)
                data.pop("company_website", None)
                data.pop("company_description", None)
            elif user.user_type == "employer":
                # Remove student fields from validation for employers
                data.pop("profile_picture", None)
                data.pop("education", None)
                data.pop("skills", None)
                data.pop("status", None)
                data.pop("resume", None)
        
        return data

    def update(self, instance, validated_data):
        # Handle skills separately for students
        if instance.user_type == "student" and "skills" in validated_data:
            skills_data = validated_data.pop("skills")
            instance.skills.set(skills_data)
        
        # Only update fields that are relevant to the user type (excluding email)
        if instance.user_type == "student":
            # Only allow student fields (no email)
            allowed_fields = ["full_name", "profile_picture", "education", "status", "resume"]
        else:
            # Only allow employer fields (no email, no profile_picture)
            allowed_fields = ["full_name", "company_name", "company_website", "company_description"]
        
        # Update only allowed fields
        for attr, value in validated_data.items():
            if attr in allowed_fields:
                setattr(instance, attr, value)
        
        instance.save()
        return instance

