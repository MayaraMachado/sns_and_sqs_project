from django.db import models
from django.contrib.auth.models import User
import uuid

class Seller(models.Model):
    seller_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price =  models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CreditCard(models.Model):
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    card_number = models.CharField(max_length=19)
    cvv = models.IntegerField()
    card_holder_name = models.CharField(max_length=255)
    exp_date = models.CharField(max_length=5) 

class Purchase(models.Model):
    purchase_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total_price = models.IntegerField()
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + str(self.total_price)
