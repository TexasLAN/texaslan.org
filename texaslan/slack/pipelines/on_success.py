from django_slack_oauth.models import SlackOAuthRequest

def register_token(request, api_data):
    SlackOAuthRequest.objects.create(
    	associated_user=request.user,
        access_token=api_data.pop('access_token'),
        extras=api_data
    )

    return request, api_data