from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, EventSerializer
from ..users.models import User
from ..events.models import Event as EventModel
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

class Event(APIView):
    serializer_class = EventSerializer

    def _extract_user_id_from_middleware(self, request):
        request.data['creator'] = request.user.get('id')

    def post(self, request, format=None):
        self._extract_user_id_from_middleware(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                    status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        events = [self.serializer_class(event).data for event in EventModel.objects.all().order_by('-start_time')]
        return Response(events,
                status=status.HTTP_200_OK)

