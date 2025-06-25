import json

from django.contrib import messages
from django.contrib.auth import logout
from django.core.serializers import serialize
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .models import ChemicalMaster, DailyConsumptions


# Create your views here.
def entryform(request):
    if not request.user.is_authenticated:
        messages.success(
            request, "Your session has expired. Please login again."
        )
        return redirect("user_login")

    dropdown_dict = {}
    dropdown_data = ChemicalMaster.objects.all()
    for item in dropdown_data:
        if item.unit_code not in dropdown_dict:
            dropdown_dict[item.unit_code] = {
                "unit_name": item.unit_name,
                "chemicals": [{item.chemical_code: item.chemical_name}],
            }
        else:
            dropdown_dict[item.unit_code]["chemicals"].append(
                {item.chemical_code: item.chemical_name}
            )

    dropdown_json = json.dumps(dropdown_dict)

    context = {"dropdown_json": dropdown_json}

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
        messages.success(
            request, "Your session has expired. Please login again."
        )
        return redirect("user_login")

    return render(request, "report_page.html")


def daily_report(request):
    if not request.user.is_authenticated:
        messages.success(
            request, "Your session has expired. Please login again."
        )
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
        "data_json": data_json,
        "show_table": False,
        "table": [],
    }

    if request.POST:
        if "clear" in request.POST:
            context["show_table"] = False
            return render(request, "daily_report.html", context)

        try:
            if (
                request.POST.get("start_date", "") == ""
                or request.POST.get("end_date", "") == ""
                or request.POST.get("unit", "") == ""
                or request.POST.get("chemical", "") == ""
            ) and "success" in request.POST:
                messages.success(
                    request, "Please fill all the required inputs."
                )
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
                        code = ChemicalMaster.objects.get(
                            chemical_code=data.chemical_code
                        )
                        chemical = code.chemical_name
                        context["table"].append(
                            {
                                "date": data.date,
                                "chemical": chemical,
                                "opening_balance": data.opening_balance,
                                "reciept": data.reciept,
                                "consumption": data.consumption,
                                "closing_balance": data.closing_balance,
                                "sap": data.sap,
                            }
                        )
                else:
                    messages.success(
                        request,
                        "No entry in the database for the entered inputs.",
                    )
        except Exception as e:
            messages.success(request, "Please fill all the required inputs.")

    return render(request, "daily_report.html", context)


def monthly_report(request):
    if not request.user.is_authenticated:
        messages.success(
            request, "Your session has expired. Please login again."
        )
        return redirect("user_login")

    return render(request, "monthly_report.html")


def analytics(request):
    return HttpResponse("Analytics page")


def settings(request):
    return HttpResponse("settings")


def user_logout(request):
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("user_login")
