from django.urls import path
from .views import customerView, orderView, orderDetails, salesView,placing_order

urlpatterns = [
    path('customer/',customerView.as_view()), # url to add and get customers
    path('order/',orderView.as_view()), # url to add and get orders
    path('details/<int:id>/', orderDetails.as_view()),
    path('sales/',salesView.as_view()), # url to add and get sales-person
    path('order/delivery/<int:id>/',placing_order.as_view()), # url to palce and confirm orders
    # path('order/new/',placeOrder.as_view()),
]
