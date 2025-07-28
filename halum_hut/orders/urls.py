from django.urls import path
from .views import CreateOrderWithCOD  # 👈 COD view


urlpatterns = [
    path('create-cod/', CreateOrderWithCOD.as_view(), name='create-cod-order'),  # 👈 COD endpoint
]
