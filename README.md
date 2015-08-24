Accompani-Calendar is a 'lean' app which displays your primary Google calendar in the FullCalendar UI.

This app talks to Google Calendar v3 apis; therefore, you would need to generate a client_secret.json and place it in the child of accompany folder. For instructions on how to generate this file, please see: https://developers.google.com/google-apps/calendar/auth. A placeholder file with the name 'client_secret_placeholder.json' has been placed.


Depedencies:
1. Linux + Python 2.7
2. Django 1.7.5
3. google-api-python-client python library
4. oauth2client python library for handing oauth requests.

Both (3) and (4) can be installed using pip


To run:
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver
4. In your browser, go to http://localhost:8000/accompani/calendar/index/
