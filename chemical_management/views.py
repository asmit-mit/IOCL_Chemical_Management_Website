import json

from django.contrib import messages
from django.contrib.auth import logout
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render

from .models import ChemicalMaster, DailyConsumptions


# Create your views here.
def entryform(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    data = ChemicalMaster.objects.all()
    data_json = serialize("json", data)
    data_json = json.dumps(
        list(
            data.values(
                "unit_code",
                "unit_name",
                "chemical_code",
                "chemical_name",
                "unit",
            )
        )
    )

    context = {"data": data, "data_json": data_json}

    if request.POST:
        if (
            request.POST["date"] == ""
            or request.POST["unit"] == ""
            or request.POST["chemical"] == ""
            or request.POST["smc"] == ""
            or request.POST["opening_balance"] == ""
            or request.POST["receive_qty"] == ""
            or request.POST["consumption_qty"] == ""
            or request.POST["sap_balance"] == ""
        ):
            messages.success(request, "Please enter all the required inputs.")
        else:
            date = request.POST["date"]
            unit_code = request.POST["unit"]
            chemical_code = request.POST["chemical"]
            opening_balance = request.POST["opening_balance"]
            reciept = request.POST["receive_qty"]
            consumption = request.POST["consumption_qty"]
            closing_balance = request.POST["closing_balance"]
            sap = request.POST["sap_balance"]

            chemical_instance = get_object_or_404(
                ChemicalMaster,
                unit_code=unit_code,
                chemical_code=chemical_code,
            )

            queryset = DailyConsumptions.objects.filter(
                date=date,
                unit_code=chemical_instance,
                chemical_code=chemical_instance,
            )

            if queryset.exists():
                messages.success(
                    request,
                    "Entry for the entered date, unit and chemical already exists.",
                )
            else:
                entry = DailyConsumptions.objects.create(
                    unit_code=chemical_instance,
                    chemical_code=chemical_instance,
                    date=date,
                    opening_balance=opening_balance,
                    reciept=reciept,
                    consumption=consumption,
                    closing_balance=closing_balance,
                    sap=sap,
                )

                entry.save()

                messages.success(request, "Entry has been added.")

    return render(request, "chemical_intake_form.html", context)


def report(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    data = ChemicalMaster.objects.all()
    data_json = serialize("json", data)
    data_json = json.dumps(
        list(
            data.values(
                "unit_code",
                "unit_name",
                "chemical_code",
                "chemical_name",
                "unit",
            )
        )
    )

    context = {
        "data": data,
        "data_json": data_json,
        "show_table": False,
        "table": [],
    }

    if request.POST:
        if (
            request.POST["start_date"] == ""
            or request.POST["end_date"] == ""
            or request.POST["unit"] == ""
            or request.POST["chemical"] == ""
        ) and "clear" not in request.POST:
            messages.success(request, "Please fill all the required inputs.")
            context["show_table"] = False
        elif "clear" in request.POST:
            context["show_table"] = False
        else:
            unit = request.POST["unit"]
            chemical = request.POST["chemical"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]

            queryset = DailyConsumptions.objects.filter(
                date__range=[start_date, end_date],
                unit_code__unit_code=unit,
                chemical_code__chemical_code=chemical,
            )

            if queryset.exists():
                context["show_table"] = True
                for data in queryset:
                    context["table"].append(
                        {
                            "date": data.date,
                            "opening_balance": data.opening_balance,
                            "reciept": data.reciept,
                            "consumption": data.consumption,
                            "closing_balance": data.closing_balance,
                            "sap": data.sap,
                        }
                    )
            else:
                messages.success(
                    request, "No entry in the database for the entered inputs."
                )

    return render(request, "report_page.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("user_login")
