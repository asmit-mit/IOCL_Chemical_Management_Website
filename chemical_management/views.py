from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render


# Create your views here.
def entryform(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    context = {
        "units": [],
        "chemicals": [],
    }

    return render(request, "chemical_intake_form.html", context)


def report(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    context = {
        "show_table": False,
        "units": [],
        "chemicals": [],
        "table": [],
    }

    if request.GET:
        if "submit" in request.GET:
            context["show_table"] = True
        if (
            request.GET["start_date"] == "" or request.GET["end_date"] == ""
        ) and "clear" not in request.GET:
            messages.success(request, "Please fill all the required inputs.")
            context["show_table"] = False
        if "clear" in request.GET:
            context["show_table"] = False

    return render(request, "report_page.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("user_login")
