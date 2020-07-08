"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api.service.product_view import ProductstView
from api.service.purchase_view import PurchasetView
from api.service.user_view import UserView
from api.service.seller_view import SellerView

urlpatterns = [
    path('products/', ProductstView.as_view(), name='products'),
    path('purchase/', PurchasetView.as_view(), name='purchase'),
    path('purchase/history/', PurchasetView.as_view(), name='purchase-history'),
    path('user/', UserView.as_view(), name='user'),
    path('seller/', SellerView.as_view(), name='seller'),
    path('seller/<str:id>', SellerView.as_view(), name='seller-id'),
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh-token/', refresh_jwt_token, name='refresh-token'),
]
