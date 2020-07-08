import pytest
import json
from django.urls import reverse

def test_view_get_page_not_found(client):
   response = client.get('/')
   assert response.status_code == 404

def test_purchase_without_authentication(client, db):
   url = reverse('purchase')
   body = {
            "products" : [
               {
                  "product_id": "aa44ac86-3705-4954-8a1d-aa4733623870"
               },
               {
                  "product_id": "66efcb62-7b50-41b9-a3ca-7a6382eba6e8"
               }
            ],
            "credit_card":{
               "card_number":"1234123412341234"
            }
         }
   response = client.post(url, data=body)
   assert response.status_code == 401

def test_purchase_history_without_authentication(client, db):
   url = reverse('purchase-history')
   response = client.post(url)
   assert response.status_code == 401

def test_view_get_list_products_without_authentication(client, db):
   url = reverse('products')
   response = client.get(url)
   assert response.status_code == 200

def test_purchase_with_authentication_and_field_errors(client, django_user_model):
   url = reverse('purchase')
   username="user1"
   password="password"
   data = {'products' : [],'credit_card':{'card_number':'1234123412341234','cvv':789,'exp_date':'12/24'}}
   django_user_model.objects.create_user(username=username, password=password)
   client.login(username=username, password=password)
   response = client.post(url, data=json.loads(json.dumps(data)))
   r = response.json()
   assert response.status_code == 400

def test_purchase_history_with_authentication(client, django_user_model):
   url = reverse('purchase-history')
   username="user1"
   password="password"
   django_user_model.objects.create_user(username=username, password=password)
   client.login(username=username, password=password)
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_view_create_product_and_seller(client, db):
    url_seller = reverse('seller')
    url_product = reverse('products')
    data_seller = {"name":"seller"}
    response_seller = client.post(url_seller, data_seller)
    seller_id = response_seller.json().get('seller_id')
    assert response_seller.status_code == 201

    response_get_seller = client.get(url_seller+seller_id)
    assert response_get_seller.status_code == 200

    data_product = {"title":"Notebook LeVelho","price":100000,"seller_id":seller_id}
    response_product = client.post(url_product, data_product)   
    assert response_product.status_code == 201
