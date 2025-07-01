import base64
import calendar
import csv
import json
import random
import tkinter as tk
from datetime import date, datetime, timedelta
from functools import wraps
from io import BytesIO
from tkinter import filedialog

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.core.cache import cache
from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from sklearn.linear_model import LinearRegression

from .models import ChemicalMaster, DailyConsumptions

matplotlib.use("Agg")


# util functions
def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("user_login")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def handle_user_submission(request, required_fields):
    missing_fields = [
        field
        for field in required_fields
        if not request.POST.get(field, "").strip()
    ]
    if missing_fields:
        return (
            False,
            f"Please fill all the required inputs: {', '.join(missing_fields)}",
        )
    return True, "All inputs received."


def get_file_form_filemanager():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("CSV files", "*.csv"),),
    )

    root.destroy()

    return file_path


def handle_consumption_data_import():
    file_path = get_file_form_filemanager()

    DailyConsumptions.objects.all().delete()

    try:
        with open(file_path) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:

                try:
                    chemical_instance = get_object_or_404(
                        ChemicalMaster,
                        unit_code=row[1],
                        chemical_code=row[3],
                    )
                except Exception as e:
                    return (
                        False,
                        f"We got an error: {e}",
                    )

                entry = DailyConsumptions.objects.create(
                    date=row[0],
                    unit_code=chemical_instance,
                    chemical_code=chemical_instance,
                    opening_balance=row[5],
                    reciept=row[6],
                    consumption=row[7],
                    closing_balance=row[8],
                    sap=row[9],
                    remarks=row[10],
                )

                entry.save()

    except Exception as e:
        invalidate_cache()
        DailyConsumptions.objects.all().delete()
        return (
            False,
            f"We got an error: {e}",
        )

    invalidate_cache()
    return True, "CSV file successfully imported."


def handle_chemical_data_import():
    file_path = get_file_form_filemanager()

    ChemicalMaster.objects.all().delete()

    try:
        with open(file_path) as f:
            reader = csv.reader(f)

            next(reader)
            for row in reader:

                entry = ChemicalMaster.objects.create(
                    unit_code=row[0],
                    unit_name=row[1],
                    chemical_code=row[2],
                    chemical_name=row[3],
                    unit=row[4],
                )

                entry.save()

    except Exception as e:
        ChemicalMaster.objects.all().delete()
        return (
            False,
            f"We got an error: {e}",
        )

    invalidate_cache()
    return True, "CSV file successfully imported."


def handle_data_download(columns, value_list, model, download_file_name):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{download_file_name}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(columns)

    records = model.objects.all().values_list(*value_list)

    for rec in records:
        writer.writerow(rec)

    return response


def get_month_name(month_number):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number"


def get_and_cache_dropdown_data():
    if cache.get("dropdown_json") is not None:
        return cache.get("dropdown_json")

    data_dict = {}
    dropdown_data = ChemicalMaster.objects.all()

    for item in dropdown_data:
        consumption_data = DailyConsumptions.objects.filter(
            chemical_code=item, unit_code=item, consumption__gt=0
        ).order_by("-date")[:7]

        if consumption_data.exists():
            sap_stock = consumption_data[0].sap
        else:
            sap_stock = 0

        sap_material_code = "".join(random.choices("0123456789", k=4))
        avg_consume = 0

        consumption_values = [
            record.consumption for record in consumption_data
        ]

        consumption_data_list = [
            [record.date.strftime("%Y-%m-%d"), record.consumption]
            for record in consumption_data
        ]

        if consumption_values:
            avg_consume = sum(consumption_values) / len(consumption_values)
        else:
            avg_consume = 0

        avg_consume = round(avg_consume, 2)

        if item.unit_code not in data_dict:
            data_dict[item.unit_code] = {
                "unit_name": item.unit_name,
                "chemicals": [
                    {
                        item.chemical_code: item.chemical_name,
                        "avg_consume": avg_consume,
                        "uom": item.unit,
                        "smc": sap_material_code,
                        "sap_stock": sap_stock,
                        "consumption_data": consumption_data_list,
                    }
                ],
            }
        else:
            data_dict[item.unit_code]["chemicals"].append(
                {
                    item.chemical_code: item.chemical_name,
                    "avg_consume": avg_consume,
                    "uom": item.unit,
                    "smc": sap_material_code,
                    "sap_stock": sap_stock,
                    "consumption_data": consumption_data_list,
                }
            )

    data_json = json.dumps(data_dict)

    cache.set("dropdown_json", data_json)
    cache.touch("dropdown_json", 60 * 60 * 2)

    return data_json


def get_analytics(
    id,
    unit_code,
    chemical_code,
    unit_name,
    chemical_name,
    day,
    month,
    year,
    n_months,
):
    chemical_instance = get_object_or_404(
        ChemicalMaster,
        unit_code=id[0],
        chemical_code=id[1],
    )

    latest = (
        DailyConsumptions.objects.filter(
            unit_code=unit_code, chemical_code=chemical_code
        )
        .order_by("-date")
        .first()
    )

    last_7_entries = DailyConsumptions.objects.filter(
        unit_code=unit_code,
        chemical_code=chemical_code,
        consumption__gt=0,
    ).order_by("-date")[:7]

    avg_consumption = round(
        last_7_entries.aggregate(Avg("consumption"))["consumption__avg"],
        2,
    )
    total_stock = round(latest.closing_balance + latest.sap, 2)
    coverage = (
        round(total_stock / (avg_consumption * 31), 2)
        if avg_consumption
        else 0
    )

    today = datetime.now()
    start_date = (today - relativedelta(months=n_months)).replace(day=1)
    end_date = today.replace(day=1)

    monthly_consumptions = (
        DailyConsumptions.objects.filter(
            unit_code=unit_code,
            chemical_code=chemical_code,
            date__gte=start_date,
            date__lt=end_date,
        )
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total_consumption=Sum("consumption"))
        .order_by("month")
    )

    consumption_data = [
        (entry["month"], entry["total_consumption"])
        for entry in monthly_consumptions
        if entry["total_consumption"] is not None
    ]

    months = [entry[0] for entry in consumption_data]
    consumptions = [entry[1] for entry in consumption_data]

    if len(months) > 1:
        X = np.array(range(len(consumptions))).reshape(-1, 1)
        y = np.array(consumptions)

        model = LinearRegression()
        model.fit(X, y)

        future_indices = np.array(
            range(len(consumptions), len(consumptions) + 4)
        ).reshape(-1, 1)
        future_consumptions = model.predict(future_indices).tolist()
        future_consumptions = [round(val, 2) for val in future_consumptions]

        current_month_start = today.replace(day=1)
        future_months = [
            current_month_start + relativedelta(months=i) for i in range(4)
        ]
    else:
        future_consumptions = [0.0, 0.0, 0.0, 0.0]
        future_months = []

    all_months = months

    all_consumptions = consumptions

    X_all = np.array(range(len(all_consumptions))).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X_all, all_consumptions)

    y_pred = model.predict(X_all)

    max_value = max(all_consumptions)
    y_ticks = np.arange(0, max_value + 200, 100)

    fig_pred, ax_pred = plt.subplots(figsize=(12, 6))

    ax_pred.scatter(
        all_months,
        all_consumptions,
        color="red",
        edgecolor="black",
        label="Actual & Predicted Data",
    )

    ax_pred.plot(
        all_months,
        y_pred,
        color="blue",
        label="Linear Regression Line",
        alpha=0.8,
    )

    ax_pred.set_title(
        f"Predicted Consumption for {chemical_name} ({unit_name})",
        fontsize=16,
    )
    ax_pred.set_xlabel("Months", fontsize=12)
    ax_pred.set_ylabel("Consumption", fontsize=12)
    ax_pred.legend(fontsize=10)
    ax_pred.set_yticks(y_ticks)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer_pred = BytesIO()
    plt.savefig(buffer_pred, format="png")
    buffer_pred.seek(0)
    plt.close(fig_pred)

    pred_chart = base64.b64encode(buffer_pred.getvalue()).decode("utf-8")

    monthly_data = DailyConsumptions.objects.filter(
        unit_code=unit_code,
        chemical_code=chemical_code,
        date__year=year,
        date__month=month - 1,
    ).order_by("date")

    dates = list(monthly_data.values_list("date", flat=True))
    consumptions_daily = list(
        monthly_data.values_list("consumption", flat=True)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        dates,
        consumptions_daily,
        label=chemical_name,
        alpha=0.7,
    )

    ax.set_title(
        f"{chemical_name}({unit_name}) Consumption Pattern", fontsize=16
    )
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Consumption", fontsize=12)
    ax.legend(fontsize=10)
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)

    analytics_chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return (
        {
            "id": id[0],
            "unit_name": unit_name,
            "chemical_name": chemical_name,
            "avg_consumption": avg_consumption,
            "latest_closing_balance": latest.closing_balance,
            "latest_sap": latest.sap,
            "total_stock": total_stock,
            "coverage": coverage,
            "measure_unit": chemical_instance.unit,
            "predictions": future_consumptions,
        },
        {"id": id, "analytics_chart": analytics_chart},
        {"id": id, "pred_chart": pred_chart},
    )


def get_or_cache_analytics():
    if cache.get("analytics_data") is None:

        analytics_data = []
        analytics_chart_list = []
        pred_chart_list = []
        today = datetime.today()
        current_month = today.month
        current_year = today.year

        pairs = DailyConsumptions.objects.values(
            "unit_code",
            "unit_code__unit_code",
            "unit_code__unit_name",
            "chemical_code",
            "chemical_code__chemical_code",
            "chemical_code__chemical_name",
        ).distinct()

        for pair in pairs:
            unit_code = pair["unit_code"]
            chemical_code = pair["chemical_code"]
            unit_name = pair["unit_code__unit_name"]
            chemical_name = pair["chemical_code__chemical_name"]

            id = [
                pair["unit_code__unit_code"],
                pair["chemical_code__chemical_code"],
            ]

            data, analytics_chart, pred_chart = get_analytics(
                id,
                unit_code,
                chemical_code,
                unit_name,
                chemical_name,
                today,
                current_month,
                current_year,
                n_months=9,
            )

            analytics_data.append(data)
            analytics_chart_list.append(analytics_chart)
            pred_chart_list.append(pred_chart)

        cache_data = {
            "analytics_data": analytics_data,
            "analytics_charts": analytics_chart_list,
            "pred_charts": pred_chart_list,
        }

        cache.set("analytics_data", cache_data)
        cache.touch("analytics_data", 60 * 60 * 2)

    else:
        cache_data = cache.get("analytics_data")

    return (
        cache_data["analytics_data"],
        cache_data["analytics_charts"],
        cache_data["pred_charts"],
    )


def invalidate_cache():
    cache.delete("analytics_data")
    cache.delete("dropdown_json")


# Create your views here.
@custom_login_required
def entryform(request):
    context = {"data_json": get_and_cache_dropdown_data()}

    requied_inputs = [
        "date",
        "unit",
        "chemical",
        "receive_qty",
        "consumption_qty",
        "sap_balance",
    ]

    if request.POST:
        success, message = handle_user_submission(request, requied_inputs)

        if not success:
            messages.success(request, message)
            return render(request, "chemical_intake_form.html", context)

        date = request.POST["date"]
        opening_balance = request.POST["opening_balance"]
        reciept = request.POST["receive_qty"]
        consumption = request.POST["consumption_qty"]
        closing_balance = request.POST["closing_balance"]
        sap = request.POST["sap_balance"]
        remarks = request.POST["remarks"]

        if remarks == "":
            remarks = "No Remarks"

        chemical_instance = get_object_or_404(
            ChemicalMaster,
            unit_code=request.POST.get("unit"),
            chemical_code=request.POST.get("chemical"),
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
                remarks=remarks,
            )

            entry.save()

            invalidate_cache()
            messages.success(request, "Entry has been added.")

    return render(request, "chemical_intake_form.html", context)


@custom_login_required
def report(request):
    return render(request, "report_page.html")


@custom_login_required
def daily_report(request):

    context = {
        "show_table": False,
        "table": [],
    }

    context["data_json"] = get_and_cache_dropdown_data()

    required_inputs = ["start_date", "end_date", "unit", "chemical"]

    if request.POST:
        success, message = handle_user_submission(request, required_inputs)

        if not success:
            messages.success(request, message)
            context["show_table"] = False
            return render(request, "daily_report.html", context)

        unit = request.POST["unit"]
        chemical = request.POST["chemical"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        unit_context = ChemicalMaster.objects.filter(unit_code=unit)
        if chemical != "all":
            chemical_context = ChemicalMaster.objects.filter(
                unit_code=unit, chemical_code=chemical
            )
            context["chem"] = chemical_context[0].chemical_name
        else:
            context["chem"] = "All Chemicals"

        context["unit"] = unit_context[0].unit_name
        context["start_date"] = start_date
        context["end_date"] = end_date

        if chemical == "all":
            queryset = DailyConsumptions.objects.filter(
                date__range=[start_date, end_date],
                unit_code__unit_code=unit,
            )

        else:
            queryset = DailyConsumptions.objects.filter(
                date__range=[start_date, end_date],
                unit_code__unit_code=unit,
                chemical_code__chemical_code=chemical,
            )

        if queryset.exists():
            for data in queryset:
                context["table"].append(
                    {
                        "date": data.date,
                        "chemical": data.chemical_code.chemical_name,
                        "reciept": data.reciept,
                        "consumption": data.consumption,
                        "closing_balance": data.closing_balance,
                        "sap": data.sap,
                        "remarks": data.remarks,
                    }
                )
            context["show_table"] = True
        else:
            messages.success(
                request,
                "No entry in the database for the entered inputs.",
            )
            context["show_table"] = False

    return render(request, "daily_report.html", context)


@custom_login_required
def monthly_report(request):
    context = {
        "show_table": False,
    }

    context["data_json"] = get_and_cache_dropdown_data()

    required_inputs = ["select-month", "unit", "chemical"]

    if request.POST:
        success, message = handle_user_submission(request, required_inputs)

        if not success:
            messages.success(request, message)
            context["show_table"] = False

            return render(request, "monthly_report.html", context)

        unit = request.POST["unit"]
        chemical = request.POST["chemical"]
        month = int(request.POST["select-month"])

        unit_context = ChemicalMaster.objects.filter(unit_code=unit)

        print(chemical)

        if chemical != "all":
            chemical_context = ChemicalMaster.objects.filter(
                unit_code=unit, chemical_code=chemical
            )
            context["chem_context"] = chemical_context[0].chemical_name
        else:
            context["chem_context"] = "All Chemicals"

        context["unit_context"] = unit_context[0].unit_name

        context["month_context"] = get_month_name(month)

        data_dict = json.loads(context["data_json"])
        chemicals_in_record = data_dict[unit]["chemicals"]

        current_year = datetime.now().year
        _, total_days = calendar.monthrange(current_year, month)

        if chemical != "all":
            context["chem"] = "All"
            for chem_dict in chemicals_in_record:
                for key, value in chem_dict.items():
                    if key == chemical:
                        chemicals_in_record = [{key: value}]
                        break
        else:
            new_chemicals_in_record = []
            for chem_dict in chemicals_in_record:
                key, value = next(iter(chem_dict.items()))
                new_chemicals_in_record.append({key: value})

            chemicals_in_record = new_chemicals_in_record

        closing_balance_record = []

        for record in chemicals_in_record:
            chemical_code, chemical_name = next(iter(record.items()))

            last_record = (
                DailyConsumptions.objects.filter(
                    date__year=current_year,
                    date__month=month,
                    unit_code__unit_code=unit,
                    chemical_code__chemical_code=chemical_code,
                )
                .order_by("-date")
                .first()
            )

            if last_record:
                closing_balance_record.append(last_record.closing_balance)
            else:
                closing_balance_record.append(0.0)

        records_with_dates = []

        for day in range(1, total_days + 1):
            current_date = date(current_year, month, day)
            current_date_str = current_date.strftime("%Y-%m-%d")
            day_records = []

            for record in chemicals_in_record:
                for chemical_code, chemical_name in record.items():
                    daily_consumption = DailyConsumptions.objects.filter(
                        date=current_date,
                        unit_code__unit_code=unit,
                        chemical_code__chemical_code=chemical_code,
                    ).first()

                    if daily_consumption:
                        day_records.append(
                            {
                                "chemical_name": chemical_name,
                                "reciept": daily_consumption.reciept,
                                "consumption": daily_consumption.consumption,
                            }
                        )
                    else:
                        day_records.append(
                            {
                                "chemical_name": chemical_name,
                                "reciept": 0.0,
                                "consumption": 0.0,
                            }
                        )

            records_with_dates.append(
                {"date": current_date_str, "records": day_records}
            )

        context["records_with_dates"] = records_with_dates
        context["closing_balance_record"] = closing_balance_record
        context["show_table"] = True

    return render(request, "monthly_report.html", context)


@custom_login_required
def analytics(request):
    context = {}

    units = list(
        ChemicalMaster.objects.values("unit_code", "unit_name").distinct()
    )

    (
        context["analytics_data"],
        context["analytics_charts"],
        context["pred_charts"],
    ) = get_or_cache_analytics()

    context["units"] = units

    return render(request, "analytics.html", context)


@custom_login_required
def settings(request):
    if request.POST:
        if "color" in request.POST:
            color = request.POST.get("color")
            request.session["background_color"] = color
        elif "clear_consumption_data" in request.POST:
            messages.success(
                request, "Cleared all data in DailyConsumptions Database."
            )
            DailyConsumptions.objects.all().delete()
            invalidate_cache()
            return render(request, "settings_page.html")
        elif "download_consumption_data" in request.POST:
            columns = [
                "Date",
                "Unit Code",
                "Unit Name",
                "Chemical Code",
                "Chemical Name",
                "Opening Balance",
                "Reciept",
                "Consumption",
                "Closing Balance",
                "Sap Stock",
                "Remarks",
            ]

            value_list = [
                "date",
                "unit_code__unit_code",
                "unit_code__unit_name",
                "chemical_code__chemical_code",
                "chemical_code__chemical_name",
                "opening_balance",
                "reciept",
                "consumption",
                "closing_balance",
                "sap",
                "remarks",
            ]

            return handle_data_download(
                columns, value_list, DailyConsumptions, "Consumption_Data"
            )

        elif "import_consumption_csv" in request.POST:
            success, message = handle_consumption_data_import()
            messages.success(request, message)
            return render(request, "settings_page.html")

        elif "clear_chemical_data" in request.POST:
            messages.success(
                request,
                "Cleared all data in ChemicalMaster and DailyConsumptions.",
            )
            DailyConsumptions.objects.all().delete()
            ChemicalMaster.objects.all().delete()
            return render(request, "settings_page.html")

        elif "download_chemical_data" in request.POST:
            columns = [
                "Unit Code",
                "Unit Name",
                "Chemical Code",
                "Chemical Name",
                "Unit of Measurement",
            ]

            value_list = [
                "unit_code",
                "unit_name",
                "chemical_code",
                "chemical_name",
                "unit",
            ]

            return handle_data_download(
                columns, value_list, ChemicalMaster, "ChemicalMaster_Database"
            )

        elif "import_chemical_csv" in request.POST:
            success, message = handle_chemical_data_import()
            messages.success(request, message)
            return render(request, "settings_page.html")

    return render(request, "settings_page.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("user_login")
