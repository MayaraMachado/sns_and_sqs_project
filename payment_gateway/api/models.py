from django.db import models

class Billing(models.Model):
    seller_id = models.PositiveIntegerField()
    purchase_id = models.PositiveIntegerField()
    purchase_date = models.DateTimeField()
    total_received = models.FloatField()