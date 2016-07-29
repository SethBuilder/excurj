from django.test import TestCase
from mainapp.models import UserProfile, UserRating, City, Hobby, Language
from django.contrib.auth.models import User

# Create your tests here.

class UserRatingTestCase(TestCase):
    # Test to check if a UserProfile's rating attribute can be updated
    def testSettingUserRating(self):

        # Create a city instance
        created_city = City.objects.create(name='glasgow', country='scotland', information='better than edinburgh')
        
        # Details for test user
        first_name = 'john'
        last_name = 'smith'
        email = 'johnsmith@gmail.com'
        
        # Create a username
        username = first_name.lower() + last_name.lower()

        # Create a new User object
        new_user = User.objects.get_or_create(username=username, email=email)[0]

        # Set user password
        new_user.password = 'password'

        # Set the new User object's first and last names
        new_user.first_name = first_name
        new_user.last_name = last_name

        # Save the new User object
        new_user.save()

        # Create a new User Profile object which is an extension of the User object
        new_user_profile = UserProfile.objects.create(user=new_user, city=created_city, )
        new_user_profile.slug = username

        # Save the new User Profile object
        new_user_profile.save()
        
        # Get the user profile's rating attribute
        profileRating = getattr(new_user_profile, 'average_rating')
        
        # Print the value of the user profile
        print profileRating
        
        # Call the UserProfile test function to update the average rating attribute
        UserProfile.setAvgRatingTest(new_user_profile, newVal=5)
        
        # Get the rating again and print it to ensure value has been updated
        profileRating = getattr(new_user_profile, 'average_rating')
        print profileRating