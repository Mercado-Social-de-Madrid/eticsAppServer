from django.core.management.base import BaseCommand

from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Add http at start of links which don\'t have it already'

    def handle(self, *args, **options):

        count = 0

        for entity in Entity.objects.all():

            if entity.facebook_link and not entity.facebook_link.startswith('http'):
                if not entity.facebook_link.startswith("https://facebook.com/"):
                    entity.facebook_link = "https://www.facebook.com/" + entity.facebook_link.replace("@", "").strip()
                else:
                    entity.facebook_link = "http://" + entity.facebook_link
                count += 1

            if entity.webpage_link and not entity.webpage_link.startswith('http'):
                entity.webpage_link = "http://" + entity.webpage_link.strip()
                print(entity.webpage_link)
                count += 1

            if entity.twitter_link and not entity.twitter_link.startswith('http'):
                if not entity.twitter_link.startswith("https://twitter.com/"):
                    entity.twitter_link = "https://twitter.com/" + entity.twitter_link.replace("@", "").strip()
                else:
                    entity.twitter_link = "http://" + entity.twitter_link
                count += 1

            if entity.telegram_link and not entity.telegram_link.startswith('http'):
                if not entity.telegram_link.startswith("https://telegram.me/"):
                    entity.telegram_link = "https://telegram.me/" + entity.telegram_link.replace("@", "").strip()
                else:
                    entity.telegram_link = "http://" + entity.telegram_link
                count += 1

            if entity.instagram_link and not entity.instagram_link.startswith('http'):
                if not entity.instagram_link.startswith("https://instagram.com/"):
                    entity.instagram_link = "https://instagram.com/" + entity.instagram_link.replace("@", "").strip()
                else:
                    entity.instagram_link = "http://" + entity.instagram_link
                count += 1

            entity.save()

        print 'Fixed links: ' + str(count)