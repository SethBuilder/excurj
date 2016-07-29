from django.contrib import admin
from mainapp.models import User
from mainapp.models import City
from mainapp.models import Hobby
from mainapp.models import Language
from mainapp.models import UserRating
from mainapp.models import UserProfile


#admin.site.register(User)
admin.site.register(City)
admin.site.register(Hobby)
admin.site.register(Language)
admin.site.register(UserRating)
admin.site.register(UserProfile)