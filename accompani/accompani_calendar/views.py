
import json
from datetime import datetime
import os

from django.shortcuts import render
import httplib2
from django.http import HttpResponseRedirect, HttpResponse
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from django.core.urlresolvers import reverse_lazy

from apiclient.discovery import build

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

# TODO(ankit): Move this to a constants file.
CREDENTIAL = 'credential'

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    # Request read/write access to calendar scopes since I *might* work on implementing
    # create calendar event functionality.
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/accompani/calendar/oauthcallback/')


def index(request):
    # Main page of the calendar app.
    if CREDENTIAL in request.session:
        credential = request.session[CREDENTIAL]
    else:
        credential = None

    if credential is None or credential.invalid:
        return do_auth()
    else:
        try:
            # Make sure that when the page is loaded, the session doesn't contain
            # expired access token.
            http = httplib2.Http()
            http = credential.authorize(http)

        except AccessTokenRefreshError:
            return do_auth()
        return render(request, "accompani_calendar/index.html")


# Fetches a list of calendar events for a given month and year.
# Why is this API necessary? We show the 'month view' of the calendar; we just want to show all the events
# which occur in the given month.
# This function either returns a list of events in a json or sends a message to the frontend to 'refresh' the page; this
# is required since we might have an access token which needs to be refreshed.
def fetch_list(request):
    start_date = request.GET.get('start', '2015-01-01')
    try:
        credential = request.session[CREDENTIAL]
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("calendar", "v3", http=http)
        # TODO(ankit): Worry about timezone issues later on?
        timeMin = datetime.strptime(start_date, '%Y-%m-%d').isoformat() + 'Z'
        eventResults = service.events().list(calendarId='primary', singleEvents=True, timeMin=timeMin, orderBy='startTime').execute()

        events = eventResults.get('items', [])

        response_data = {}
        response_data['should_refresh'] = False
        response_data['data'] = events

    except AccessTokenRefreshError:
        response_data = {};
        response_data['should_refresh'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def do_auth():
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)

def auth_return(request):
    # Oauth callback end point.
    credential = FLOW.step2_exchange(request.REQUEST)
    request.session[CREDENTIAL] = credential
    return HttpResponseRedirect(reverse_lazy('index'))