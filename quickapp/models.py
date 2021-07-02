from django.db import models


# Create your models here.
class customer(models.Model):
    customer_name = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.customer_name


class salesperson(models.Model):
    salesperson_name = models.CharField(max_length=100)

    def __str__(self):
        return self.salesperson_name


class orders(models.Model):
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    order_active = models.IntegerField(default=1)
    buyer = models.ForeignKey(customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(salesperson, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

