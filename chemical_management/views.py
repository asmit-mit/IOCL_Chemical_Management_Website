from datetime import datetime as dt

from django.shortcuts import HttpResponse, render
from django.template import loader


# Create your views here.
def entryform(request):
    current = dt.now()
    s = current.strftime("%A, %-m %B %-Y, %I:%M %p")

    context = {
        "date": s,
    }

    return render(request, "chemical_intake_form.html", context)
