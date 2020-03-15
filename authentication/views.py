import random
from rest_framework.views import APIView, status
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationAPIView(APIView):
    """Handles `user registration` requests.
    returns:
        - user object
        - success message
    """

    def post(self, request):
        email = request.data.get('email')
        user_name = request.data.get('user_name')
        user_email = User.objects.filter(email__iexact=email)
        user_name = User.objects.filter(user_name__iexact=user_name)
        if user_email.exists():
            return Response({
                'message': 'Email already in database',
                'success': False
            })
        elif user_name.exists():
            return Response({
                'message': 'Username already in database',
                'success': False
            })
        else:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            response = {
                'user': dict(user_data),
                'message': 'Account successfully created.',
                'success': True
            }
            return Response(response, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    """Handles `user login` requests.
    returns:
        - user object
        - success message
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        response = {
            'user': dict(user_data),
            'message': 'You have successfully logged in.',
            'success': True
        }
        return Response(response, status=status.HTTP_200_OK)
