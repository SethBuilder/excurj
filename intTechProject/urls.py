from django.conf.urls import url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from intTechProject import views
from django.conf.urls import include
from registration.backends.simple.views import RegistrationView
from django.views.generic import RedirectView
from django_messages.views import *


# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/baseProfile/"

urlpatterns = patterns('',
                       url(r'^admin/', admin.site.urls),
                       url(r'^$', views.index, name="index"),
                       url(r'^city/(?P<city_name_slug>[\w-]+)$', views.city, name='city'),
                       url(r'^user/(?P<user_name_slug>\w+)$', views.user, name='user'),
                       url(r'^cityloc', views.cityloc, name="cityloc"),
                       url(r'^', include('registration.backends.simple.urls')),
                       url(r'^createprofile/', views.createprofile, name="createprofile"),
                       url(r'^submitreview/', views.submitreview, name="submitreview"),
                       url(r'^about/', views.about, name="about"),
                       url(r'^search/$', views.search, name="search"),
                       url(r'^updateprofile/', views.updateprofile, name="updateprofile"),
                       url(r'^messages/', include('django_messages.urls')),
                       url(r'^$', RedirectView.as_view(url='inbox/'), name='messages_redirect'),
                       url(r'^inbox/$', inbox, name='messages_inbox'),
                       url(r'^outbox/$', outbox, name='messages_outbox'),
                       url(r'^compose/$', compose, name='messages_compose'),
                       url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
                       url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
                       url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
                       url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
                       url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
                       url(r'^trash/$', trash, name='messages_trash'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


