import json
import requests
from django.http import JsonResponse
from rest_framework_jwt.views import verify_jwt_token
from rest_framework.response import Response
from rest_framework import status

def is_api_call(request):
    return request.path.startswith('/api/v1')

def is_jwt_endpoint(request):
    return request.path.startswith('/api/v1/jwt') or request.path.startswith('/api/v1/status')

def needs_jwt_verification(request):
    return is_api_call(request) and not is_jwt_endpoint(request)

def valid_jwt(request):
    return create_verification_request(request).status_code == status.HTTP_200_OK

def strip_token(request):
    return request.META.get('HTTP_AUTHORIZATION', '')[7:]

def parse_verification_uri(request):
    return 'http://' + request.META['HTTP_HOST'] + '/api/v1/jwt/verify/'

def create_verification_request(request):
    token = strip_token(request)
    uri = parse_verification_uri(request)
    response = requests.post(uri, json={"token": token})
    return response

class JWTAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if needs_jwt_verification(request) and not valid_jwt(request):
            return JsonResponse({'error': 'invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)
        response = self.get_response(request)
        return response
