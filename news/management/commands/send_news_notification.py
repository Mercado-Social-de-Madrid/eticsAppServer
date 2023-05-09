from django.core.management.base import BaseCommand
from news.models import News, send_news_notification


class Command(BaseCommand):
    help = 'Send notification of an existing news (use if there was an error when saving news)'

    def add_arguments(self, parser):
        parser.add_argument('news_id', type=str, help='News uuid')

    def handle(self, *args, **options):

        news_id = options['news_id']

        news = News.objects.get(pk=news_id)

        if news:
            send_news_notification(news)