from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# this is the model for city
class City(models.Model):

    name = models.CharField(max_length=128, default="", unique=False)#city name
    country = models.CharField(max_length=128, default="Scotland")#country name
    information = models.CharField(max_length=3000, default="")#information about city
    image = models.ImageField(upload_to='city_images', default=0)#city image
    slug = models.SlugField(unique=False)#city slug

    #save function
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# this is the model for hobbies
class Hobby(models.Model):
    hobby = models.CharField(max_length=128)#hobby name

    #save function
    def save(self, *args, **kwargs):
        self.slug = slugify(self.hobby)
        super(Hobby, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.hobby


# this is the model for languages
class Language(models.Model):
    language = models.CharField(max_length=128)#language name

    #save function
    def save(self, *args, **kwargs):
        self.slug = slugify(self.language)
        super(Language, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.language


# this is model for user
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')#each user profile is associated with one user

    hobbies = models.ManyToManyField(Hobby, blank=True)#m2m relationship between profiles and hobbies
    languages = models.ManyToManyField(Language, blank=True)#m2m relationship between profiles and languages

    profilepic = models.ImageField(upload_to='profile_pictures', blank=True)#optinal profile pic
    city = models.ForeignKey(City)#each profile is associated with a city
    slug = models.SlugField(unique=False)#slug for profile

    average_rating = models.IntegerField(default=0)#avg rating for user
    ratings_count = models.IntegerField(default=0)#number of ratings user received

    #save function
    def save(self, *args, **kwargs):

        # Uncomment if you don't want the slug to change every time the name changes
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    #updates avg rating
    def update_average_rating(self, new_rating, *args, **kwargs):

        old_total = self.average_rating * self.ratings_count

        self.ratings_count += 1

        # Find new average
        self.average_rating = (old_total + new_rating) / self.ratings_count
        print self.user.first_name + str(self.average_rating)
        super(UserProfile, self).save(*args, **kwargs)

    def get_range_average(self):
        print self.average_rating
        return range(self.average_rating)
        
    # Function used for basic test in tests.py        
    def setAvgRatingTest(self, newVal):
        self.average_rating = newVal


# this is the model for user ratings
class UserRating(models.Model):
    user = models.ForeignKey(UserProfile, related_name="rated_user")#one user can have many ratings
    rating_user = models.ForeignKey(UserProfile, related_name="rating_user")#one user can have many rating users
    comment = models.CharField(max_length=500, blank=True)#comment
    rating = models.IntegerField(default=0,validators=[MaxValueValidator(5), MinValueValidator(0)#rating out of 5
        ])
    #save function
    def save(self, *args, **kwargs):
        self.user.update_average_rating(self.rating)
        super(UserRating, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.rating)

    def get_range(self):
        return range(self.rating)



