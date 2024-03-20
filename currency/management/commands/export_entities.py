import json

from django.core.management.base import BaseCommand

from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Export entities profile to a json file'

    def add_arguments(self, parser):
        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export entities')

    def handle(self, *args, **options):
        jsonfile = options['jsonfile']

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

        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(data)
            f.write(json_entities)
            f.close()
