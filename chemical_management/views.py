from django.shortcuts import render


# Create your views here.
def entryform(request):
    context = {}

    return render(request, "chemical_intake_form.html", context)
