def debug_oauth_request(request, api_data):
    print(request.user)
    print(api_data)
    return request, api_data