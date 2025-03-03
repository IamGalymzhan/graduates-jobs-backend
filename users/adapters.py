from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    This adapter is called after a successful social login (e.g., Google).
    Instead of redirecting, it returns a JSON response with tokens + user data.
    """
    def authentication_success(self, request, sociallogin):
        """
        Called when the user is successfully authenticated via a social provider.
        """
        user = sociallogin.user
        # Ensure the user is active and saved
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "company_name": user.company_name,
                "email": user.email,
                "user_type": user.user_type,
                "profile_picture": (
                    user.profile_picture.url if user.profile_picture else None
                ),
            },
        }
        return JsonResponse(data)

    def get_login_redirect_url(self, request):
        """
        This method is normally used to determine where to redirect after login.
        Because we are returning JSON, we can just return None or an empty string.
        """
        return None
