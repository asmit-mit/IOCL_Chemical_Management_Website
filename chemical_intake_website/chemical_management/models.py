from django.db import models


# ChemicalMaster Model
class ChemicalMaster(models.Model):
    unit_code = models.CharField(max_length=50)
    unit_name = models.CharField(max_length=50)
    chemical_code = models.CharField(max_length=50)
    chemical_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["unit_code", "chemical_code"],
                name="unique_unit_code_chemical_code",
            )
        ]


# DailyConsumptions Model
class DailyConsumptions(models.Model):
    date = models.DateField()
    unit_code = models.ForeignKey(
        ChemicalMaster,
        on_delete=models.DO_NOTHING,
        related_name="daily_consumptions_unit",
    )
    chemical_code = models.ForeignKey(
        ChemicalMaster,
        on_delete=models.DO_NOTHING,
        related_name="daily_consumptions_chemical",
    )
    opening_balance = models.FloatField()
    reciept = models.FloatField()
    consumption = models.FloatField()
    closing_balance = models.FloatField()
    sap = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "unit_code", "chemical_code"],
                name="unique_date_unit_chemical",
            )
        ]
