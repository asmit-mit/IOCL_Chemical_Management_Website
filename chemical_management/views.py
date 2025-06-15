from django.contrib import messages
from django.shortcuts import render


# Create your views here.
def entryform(request):
    context = {
        "units": [
            {"value": "kg", "text": "Kilogram"},
            {"value": "lb", "text": "Pound"},
            {"value": "oz", "text": "Ounce"},
            {"value": "g", "text": "Gram"},
        ],
        "chemicals": [
            {"value": "dummy", "text": "Dummy"},
        ],
    }

    return render(request, "chemical_intake_form.html", context)


def report(request):
    context = {
        "show_table": False,
        "units": [
            {"value": "kg", "text": "Kilogram"},
            {"value": "lb", "text": "Pound"},
            {"value": "oz", "text": "Ounce"},
            {"value": "g", "text": "Gram"},
        ],
        "chemicals": [
            {"value": "dummy", "text": "Dummy"},
        ],
        "table": [
            {
                "date": "2025-06-01",
                "opening_balance": 1000,
                "reciept": 200,
                "consumption": 150,
                "closing_balance": 1050,
                "sap": "SAP001",
                "days_left": 10,
            },
            {
                "date": "2025-06-02",
                "opening_balance": 1050,
                "reciept": 300,
                "consumption": 200,
                "closing_balance": 1150,
                "sap": "SAP002",
                "days_left": 12,
            },
            {
                "date": "2025-06-03",
                "opening_balance": 1150,
                "reciept": 100,
                "consumption": 250,
                "closing_balance": 1000,
                "sap": "SAP003",
                "days_left": 8,
            },
        ],
    }

    if request.GET:
        if "submit" in request.GET:
            context["show_table"] = True
        if (
            request.GET["start_date"] == "" or request.GET["end_date"] == ""
        ) and "clear" not in request.GET:
            messages.success(request, "Please fill all the inputs.")
            context["show_table"] = False
        if "clear" in request.GET:
            context["show_table"] = False

    print(request.GET)

    return render(request, "report_page.html", context)
