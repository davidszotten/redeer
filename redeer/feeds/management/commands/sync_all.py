from django.core.management.base import NoArgsCommand

from redeer.feeds.sync import sync_all

class Command(NoArgsCommand):
    help = 'Sync all feeds'

    def handle(self, *args, **options):
        sync_all()

        self.stdout.write('Sync successful')
