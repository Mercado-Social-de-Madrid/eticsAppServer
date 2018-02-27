"""boniatos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

import currency.urls as currency_urls
import offers.urls as offers_urls
import wallets.urls as wallets_urls
import news.urls as news_urls
from api.urls import get_api

urlpatterns = [
    url(r'^', include(currency_urls)),
    url(r'^', include(offers_urls)),
    url(r'^', include(wallets_urls)),
    url(r'^', include(news_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(get_api('v1').urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
