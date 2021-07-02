from rest_framework import serializers
from .models import salesperson, orders, customer


class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer
        # fields = ['customer_name','postal_code']
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'


class salespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = salesperson
        fields = '__all__'

