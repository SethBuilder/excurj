# Excurj - Internet Technology 2016

Team project developed by:
* Martin Grant - 2216713G
* Blair Calderwood - 2216586C
* Ihsan Riaz - 2232158R
* Seif Harbi Saleem Elmughrabi - 2219120E

Setup and Install:

Python 2.7 is required with pip to install all dependencies for the application. Requirements.txt has all of the dependencies, which can be installed using "pip install -r requirements.txt".

The application's database is in this repository. You shouldn't have to run any commands to populate the database, however if you do then use the standard "python manage.py makemigrations", "python manage.py migrate" and "python populationscript.py". 

Run the server using "python manage.py runserver" and access it at 127.0.0.1:8000 or else at http://excurj.pythonanywhere.com/

User accounts to login and test the site are:
* Username: leifos, password: leifos
* Username: david, password: david
* Username: laura, password: laura
