import os

from django.shortcuts import render
import httplib2
from django.http import HttpResponseRedirect
from oauth2client.client import flow_from_clientsecrets
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
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)

        # TODO(ankit): Make request here.
        # service = build("plus", "v1", http=http)

        return render(request, "accompani_calendar/index.html")


def auth_return(request):
    # Oauth callback end point.
    credential = FLOW.step2_exchange(request.REQUEST)
    request.session[CREDENTIAL] = credential
    return HttpResponseRedirect(reverse_lazy('index'))