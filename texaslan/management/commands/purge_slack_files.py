from django.core.management.base import BaseCommand, CommandError
from django_slack_oauth.models import SlackOAuthRequest
import requests
import time
import json
import urllib.request

class Command(BaseCommand):
    help = 'Removes old files from Slack'

    def add_arguments(self, parser):
        parser.add_argument('--no-delete', action='store_true')

    def handle(self, *args, **options):
        print("Starting Slack file purge...")

        if (options['no_delete']):
            print("-- files will NOT be deleted --")

        total_count = 0

        tokens = SlackOAuthRequest.objects.all().values_list('access_token', flat=True) 

        for token in tokens:
            count = 0
            print('Processing ' + token)

            params = {
                'token': token
                , 'ts_to': int(time.time()) - 30 * 24 * 60 * 60 # 30 days
                , 'count': 1000
                , 'types': 'spaces,snippets,images,zips,pdfs' # ignore gdocs
            }
            uri = 'https://slack.com/api/files.list'
            response = requests.get(uri, params=params)
            files = json.loads(response.text)['files']

            num_files = len(files)
            
            for file in files:
                count = count + 1
                if not options['no_delete']:
                    params = {
                        'token': token
                        , 'file': file['id']
                    }
                    delete_uri = 'https://slack.com/api/files.delete'
                    response = requests.get(delete_uri, params=params)
                    print(count, "of", num_files, " deleted -", file['id'], json.loads(response.text)['ok'])

            total_count += num_files


        if (options['no_delete']):
            self.stdout.write(self.style.SUCCESS('Successfully processed ' + str(total_count) + ' files'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully processed ' + str(total_count) + ' files'))