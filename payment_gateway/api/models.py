import uuid
from django.db import models

class Revenue(models.Model):
    seller_id = models.UUIDField()
    purchase_id = models.UUIDField()
    total_value = models.IntegerField()
    purchase_date = models.DateTimeField()
