from django.shortcuts import render
from django.http import HttpResponse

# Index page of the accompani calendar app.


def index(request):

    return render(request, "accompani_calendar/index.html")
