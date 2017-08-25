from django.conf import settings

def photos_url(request):
	photos_url = settings.PHOTOS_DRIVE_FOLDER_URL
	return {'photos_url': photos_url}