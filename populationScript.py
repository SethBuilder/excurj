import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intTechProject.settings')

django.setup()

from django.contrib.auth.models import User
from mainapp.models import City, Hobby, UserProfile, Language, UserRating


# Create an array of City objects to be assigned to users
def get_cities():
    # Details for currently available cities. If the project were to go on this list would be expanded
    city_names = ['Glasgow', 'Madrid', 'Stockholm', 'Sao Paulo', 'Shanghai', 'Paris', 'Munich', 'Budapest']
    countries = ['Scotland', 'Spain', 'Sweden', 'Brazil', 'China', 'France', 'Germany', 'Hungary']

    cities = []

    # Load the description of each city (obtained from WikiTravel) from a file
    city_descriptions_file = open("static/populationScriptFiles/cityDescriptions.txt", 'r')
    city_descriptions = city_descriptions_file.readlines()

    # Loop through the city list and create a new City object for each
    for i in range(len(city_names)):
        # Create a new city object with the relevant name, country and description
        created_city = City.objects.get_or_create(name=city_names[i], country=countries[i],
                                                  information=city_descriptions[i])[0]

        # Load the city's profile image (obtained from WikiTravel) from the relevant file
        new_city_image = "%s/" + city_names[i] + ".jpg"

        # Add the new city image to the newly created City object
        created_city.image = new_city_image % 'city_images'

        # Save the object and append it to the array of City objects
        created_city.save()
        cities.append(created_city)

    # Return the array of City objects
    return cities


# Create a new user with a random first name (either male of female), a random surname and a random city
def create_user_details(male_names, female_names, last_names, created_city):
    # Create a male profile if random number is 1 (50% chance), female profile otherwise
    if random.randint(0, 1) == 1:
        first_name = male_names[random.randint(0, len(male_names) - 1)].strip().title()
    else:
        first_name = female_names[random.randint(0, len(female_names) - 1)].strip().title()

    # Assign user a random surname
    last_name = last_names[random.randint(0, len(last_names) - 1)].strip().title()

    # Create an email address in the form <first name>.<surname>@<random email suffix>
    email_suffixes = ['live.com', 'live.co.uk', 'hotmail.com', 'gmail.com', 'yahoo.com', 'apple.com', 'aol.com']
    email_suffix = email_suffixes[random.randint(0, len(email_suffixes) - 1)].strip()
    email = first_name.lower() + '.' + last_name.lower() + '@' + email_suffix

    # Create a username
    username = first_name.lower() + last_name.lower()

    # Create a new User object
    new_user = User.objects.get_or_create(username=username, email=email)[0]

    # Set all passwords to be passwords for testing
    new_user.password = 'password'

    # Set the new User object's first and last names
    new_user.first_name = first_name
    new_user.last_name = last_name

    # Save the new User object
    new_user.save()

    # Create a new User Profile object which is an extension of the User object
    # Two separate objects have to be used as the User object is a native Django one and cannot host the required fields
    new_user_profile = UserProfile.objects.get_or_create(user=new_user, city=created_city, )[0]
    new_user_profile.slug = username

    # Assign the user a random profile picture (each picture is the same but with a different coloured background)
    profile_picture = "%s/profile_picture" + str(random.randint(0, 4)) + ".jpg"
    new_user_profile.profilepic = profile_picture % 'profile_pictures'

    # Save the new User Profile object
    new_user_profile.save()

    # Return the User object
    return new_user


# Assign user a random number of hobbies between 0 and 6 (up to a total of seven hobbies)
def create_hobbies(user_details, hobby_names):
    # Create an empty array to hold the user's hobbies
    user_hobbies = []

    # Loop through hobby assign process a random number (between 0 and 6 times)
    for new_hobby in range(random.randint(0, 6)):

        # Choose a random hobby from the given hobby list
        hob = hobby_names[random.randint(0, len(hobby_names) - 1)].strip().title()

        # Check if the hobby has already been assigned to the user
        if hob not in user_hobbies:
            # If it has not then add it to the hobby array
            user_hobbies.append(hob)

            # Create a new Hobby object and save it
            new_hobby = Hobby.objects.get_or_create(hobby=hob)[0]
            new_hobby.save()

            # Assign the new hobby to the given user
            user_details.profile.hobbies.add(new_hobby)


# Assign the user a number of languages
def create_languages(user_details, random_city):
    # The list of languages a user can speak
    languages = ['English', 'Spanish', 'Swedish', 'Portuguese', 'Chinese', 'French', 'German', 'Hungarian', 'Latin',
                 'Japanese', 'Thai']

    # Assign user the language native to that city (e.g. Glasgow would be English)
    # The arrays are in the correct order so the city at index 0 will correspond to the language at index 0
    new_language = Language.objects.get_or_create(language=languages[random_city])[0]
    new_language.save()

    # Assign the native language to the user
    user_details.profile.languages.add(new_language)
    user_languages = [languages[random_city]]

    # Assign user a random number of other languages between 0 and 3 (up to a total of four languages)
    for new_language in range(random.randint(0, 3)):

        # Choose a random language in the list
        lang = languages[random.randint(0, len(languages) - 1)]

        # Ensure the language has not already been assigned to the user
        if lang not in user_languages:
            # Create the new language object and save it
            new_language = Language.objects.get_or_create(language=lang)[0]
            new_language.save()

            # Assign the new language to the user
            user_details.profile.languages.add(new_language)
            user_languages.append(lang)


# Create a database of 100 fake users (plus three real) with random names, home cities, hobbies and languages
def create_users():
    # Create the list of City objects to assign to users
    cities = get_cities()

    # Read in first names from file
    names_file = open("static/populationScriptFiles/newNamesMale.txt", 'r')
    male_names = names_file.readlines()

    names_file = open("static/populationScriptFiles/namesFemale.txt", 'r')
    female_names = names_file.readlines()

    # Read in last names from file
    names_file = open("static/populationScriptFiles/namesLast.txt", 'r')
    last_names = names_file.readlines()

    # Read in popular hobbies from file
    hobbies_file = open("static/populationScriptFiles/hobbies.txt", 'r')
    hobby_names = hobbies_file.readlines()

    # Loop through to obtain a database of 100 users
    for new_person in range(0, 100):
        # Assign the user a random city
        random_city = random.randint(0, len(cities) - 1)

        # Create a new User and User profile object with a random name
        user_details = create_user_details(male_names, female_names, last_names, cities[random_city])

        # Assign the user random hobbies and languages
        create_hobbies(user_details, hobby_names)
        create_languages(user_details, random_city)

        # Save the new user
        user_details.profile.save()

    # Create user accounts for the markers to enable them to log in
    user_list = ['leifos', 'laura', 'david']
    created_city = City.objects.get(name="Glasgow")

    # Loop through each of the three users
    for new_person in user_list:
        # Create a User object with their password set as their name
        new_user = User.objects.get_or_create(username=new_person, email=new_person + "@hotmail.com")[0]
        new_user.set_password(new_person)
        new_user.save()

        # Create a new User Profile object with Glasgow as the city
        new_user_profile = UserProfile.objects.get_or_create(user=new_user, city=created_city, )[0]
        new_user_profile.slug = new_person

        # Assign a random profile picture
        profile_picture = "%s/profile_picture" + str(random.randint(0, 4)) + ".jpg"
        new_user_profile.profilepic = profile_picture % 'profile_pictures'

        # Save the new user profile
        new_user_profile.save()


# Each user will leave a random amount of random reviews for other users to populate the rating tables
def leave_reviews():
    # Read in random reviews from file
    reviews_file = open("static/populationScriptFiles/reviews.txt", 'r')
    reviews = reviews_file.readlines()

    # Get the list of all users from the database
    users = UserProfile.objects.all()

    # Loop through the list of all users
    for new_reviewer in users:

        # Put new_reviewer in users_reviewed so they never review themselves
        users_reviewed = [new_reviewer]

        # Each user will review random users between one and five times
        # This ensures that there is variation in the amount of reviews sent and received
        for new_review in range(random.randint(1, 5)):

            # Retrieved a random review (consisting of a comment and a star rating between 1 and 5) from the list
            new_rev = reviews[random.randint(0, len(reviews) - 1)].strip()

            # Split the review into a comment and a star rating (these are separated by a comma)
            new_rev = new_rev.split(', ', 2)
            rev = new_rev[0]
            rating = new_rev[1]

            # Obtain a random user from the list
            reviewee = users[random.randint(0, len(users) - 1)]

            # Ensure the random user has not already been reviewed by this user
            if reviewee not in users_reviewed:
                rev = UserRating.objects.get_or_create(user=reviewee, rating_user=new_reviewer, comment=rev,
                                                       rating=int(rating))[0]

                # Add the reviewed users to the reviewed users list
                users_reviewed.append(reviewee)


if __name__ == '__main__':
    create_users()
    leave_reviews()
