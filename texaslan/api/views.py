from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from ..users.models import User
from allauth.account.utils import send_email_confirmation
from texaslan.site_settings.models import SiteSettingService

class AuthRegisterUser(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            send_email_confirmation(request._request, new_user)
            return Response(serializer.data,
                    status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class Status(APIView):

    def get(self, request, format=None):
        return Response({ 'rush': SiteSettingService.is_rush_open()})
