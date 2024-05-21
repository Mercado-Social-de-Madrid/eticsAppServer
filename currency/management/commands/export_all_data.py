import json

from django.core.management.base import BaseCommand

from currency.models import Category, Person, Entity
from news.models import News


def get_categories():
    items = Category.objects.all()

    data = []
    for item in items:
        data.append({
            'id': str(item.id),
            'name': item.name,
            'description': item.description,
            'color': item.color,
        })

    return data

def get_consumers():
    items = Person.objects.all()

    data = []
    for item in items:
        data.append({
            'id': str(item.id),
            'nif': item.nif,
            'name': item.name,
            'surname': item.surname,
            'email': item.email,
            'password': item.user.password,
            'address': item.address,
            'member_id': item.member_id,
            'profile_image': item.profile_image.name,
            'profile_thumbnail': item.profile_thumbnail.name,
            'registered': str(item.registered),
            'is_intercoop': item.is_intercoop,
            'inactive': item.inactive,
            'is_guest_account': item.is_guest_account,
            'fav_entities': list(map(lambda entity: str(entity.id), item.fav_entities.all())),
        })
    return data

def get_news():
    items = News.objects.all()

    data = []
    for item in items:
        data.append({
            'id': str(item.id),
            'title': item.title,
            'description': item.description,
            'short_description': item.short_description,
            'banner_image': item.banner_image.name,
            'banner_thumbnail': item.banner_thumbnail.name,
            'published_date': str(item.published_date),
            'more_info_text': item.more_info_text,
            'more_info_url': item.more_info_url,

        })
    return data

def get_providers():
    entities = Entity.objects.all()

    data = []
    for entity in entities:
        gallery_data = {
            'title': entity.gallery.title,
            'photos': list(map(lambda photo: {
                'order': photo.order,
                'title': photo.title,
                'image': photo.image.name,
                'image_thumbnail': photo.image_thumbnail.name,
                'uploaded': str(photo.uploaded),
            }, entity.gallery.photos.all()))
        } if entity.gallery else None

        try:
            benefit = {
                'id': str(entity.benefit.id),
                'published_date': str(entity.benefit.published_date),
                'last_updated': str(entity.benefit.last_updated),
                'benefit_for_entities': entity.benefit.benefit_for_entities,
                'benefit_for_members': entity.benefit.benefit_for_members,
                'includes_intercoop_members': entity.benefit.includes_intercoop_members,
                'in_person': entity.benefit.in_person,
                'online': entity.benefit.online,
                'discount_code': entity.benefit.discount_code,
                'discount_link_entities': entity.benefit.discount_link_entities,
                'discount_link_members': entity.benefit.discount_link_members,
                'discount_link_text': entity.benefit.discount_link_text,
                'active': entity.benefit.active,
            }
        except:
            benefit = None

        offers = list(map(lambda offer: {
            'id': str(offer.id),
            'title': offer.title,
            'description': offer.description,
            'banner_image': offer.banner_image.name,
            'banner_thumbnail': offer.banner_thumbnail.name,
            'published_date': str(offer.published_date),
            'discount_percent': offer.discount_percent,
            'discounted_price': offer.discounted_price,
            'active': offer.active,
            'begin_date': str(offer.begin_date),
            'end_date': str(offer.end_date),

        }, entity.offers.all()))

        data.append({
            'id': str(entity.id),
            'cif': entity.cif,
            'name': entity.name,
            'email': entity.email,
            'password': entity.user.password,
            'description': entity.description,
            'short_description': entity.short_description,
            'address': entity.address,
            'phone_number': entity.phone_number,
            'member_id': entity.member_id,
            'logo': entity.logo.name,
            'logo_thumbnail': entity.logo_thumbnail.name,

            'num_workers': entity.num_workers,
            'legal_form': entity.legal_form,
            'inactive': entity.inactive,
            'hidden': entity.hidden,
            'registered': str(entity.registered),

            'gallery_data': gallery_data,
            'balance_detail': entity.balance_detail,

            'categories': list(map(lambda cat: str(cat.id), entity.categories.all())),

            'latitude': entity.latitude,
            'longitude': entity.longitude,
            'facebook_link': entity.facebook_link,
            'twitter_link': entity.twitter_link,
            'instagram_link': entity.instagram_link,
            'telegram_link': entity.telegram_link,
            'webpage_link': entity.webpage_link,

            'benefit': benefit,
            'offers': offers,

        })
    return data


class Command(BaseCommand):
    help = 'Export all data'

    def handle(self, *args, **options):

        data = {
            'categories': get_categories(),
            'news': get_news(),
            'consumers': get_consumers(),
            'providers': get_providers(),
        }

        with open('all_data.json', 'w') as f:
            json_data = json.dumps(data)
            f.write(json_data)
            f.close()

