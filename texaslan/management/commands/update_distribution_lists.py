from django.core.management.base import BaseCommand, CommandError
from texaslan.users.models import UserService

import os
import subprocess
import shlex
import sys

class Command(BaseCommand):
    help = 'Syncs primary email addresses to Google Groups'

    def get_group_members_from_gsuite(self, group_email):
        cmd = 'gam print group-members group %s' % (group_email)

        args = shlex.split(cmd)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        out = out.decode("utf-8") 

        members = []
        if proc.returncode == 0:
            if out:
                out = out.split('\n')
                for i in range(1, len(out)):
                    row = out[i].split(',')
                    if len(row) >= 3 and row[2].lower() != 'lanbot@texaslan.org':
                        members.append(row[2].lower())
        return members

    def sync_list(self, email, in_database):
        print('Syncing ' + email + '...')
        in_database = [x.lower() for x in in_database]
        in_database = set(in_database)
        in_group = set(self.get_group_members_from_gsuite(email))

        add_to_group = [x for x in in_database if x not in in_group]
        remove_from_group = [x for x in in_group if x not in in_database]

        print('Adding: ' + str(add_to_group))
        if len(add_to_group) != 0:
            with open('users-to-add.txt', 'a') as out:
                for e in add_to_group:
                    out.write(e + '\n')
                out.close()

            cmd_add = 'gam update group ' + email + ' add member file users-to-add.txt'
            print(cmd_add)

            args = shlex.split(cmd_add)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            print(out.decode("utf-8"))
            print(err.decode("utf-8"))
            os.remove('users-to-add.txt')
        else:
            print('No users to add.')

        if len(remove_from_group) != 0:
            print('Removing: ' + str(remove_from_group))
            with open('users-to-remove.txt', 'a') as out:
                for e in remove_from_group:
                    out.write(e + '\n')
                out.close()

            cmd_remove = 'gam update group ' + email + ' remove file users-to-remove.txt'
            print(cmd_remove)

            args = shlex.split(cmd_remove)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()

            print(out.decode("utf-8"))
            print(err.decode("utf-8"))
            os.remove('users-to-remove.txt')
        else:
            print('No users to remove.')

        print('Done syncing ' + email)

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        print("Starting to update distribution lists...")

        if (options['dry_run']):
            print("-- changes will NOT be made --")

        actives = UserService.get_active_users_emails()
        inactives = UserService.get_inactive_users_emails()
        gm = actives + list(set(inactives) - set(actives))

        self.sync_list('gm@texaslan.org', gm)
        self.sync_list('open-rushees@texaslan.org', UserService.get_open_rushie_users_emails())
        self.sync_list('closed-rushees@texaslan.org', UserService.get_closed_rushie_users_emails())
        self.sync_list('pledges@texaslan.org', UserService.get_pledge_users_emails())
        self.sync_list('actives@texaslan.org', actives)
        # Let's not sync these groups for now as @texaslan.org accounts have been provisioned for these users
        # self.sync_list('officers@texaslan.org', UserService.get_officer_users_emails())
        # self.sync_list('board@texaslan.org', UserService.get_board_users_emails())
        self.sync_list('inactives@texaslan.org', inactives)
        self.sync_list('alumni@texaslan.org', UserService.get_alumni_users_emails())
