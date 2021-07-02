from django.shortcuts import render
from django.http import JsonResponse
from .serializer import customerSerializer, orderSerializer, salespersonSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import customer, orders, salesperson
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from .tasks import delivery_email

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
class customerView(APIView):
    def get(self, request):
        try:
            buyer = customer.objects.all()
            serializer = customerSerializer(buyer, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = customerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "New Customer!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Message": "Error!"}, status=status.HTTP_400_BAD_REQUEST)


class orderView(APIView):
    def get(self, request):
        try:
            orders_buyer = orders.objects.all()
            serializer = orderSerializer(orders_buyer, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = orderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "New order created!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Message": "Error!"}, status=status.HTTP_400_BAD_REQUEST)


class salesView(APIView):
    def get(self, request):
        try:
            sales = salesperson.objects.all()
            serializer = salespersonSerializer(sales, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            print(request.data)
            serializer = salespersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "New sales-man hired!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


# class customerDetails(APIView):
#     def get(self, request, id=None):
#         try:
#             if cache.get(id):
#                 print("FROM CACHE")
#                 data = cache.get(id)
#                 print(type(data))
#                 return Response(data, status=status.HTTP_200_OK)
#             else:
#                 print("FROM DATABASE")
#                 try:
#                     data = customer.objects.get(id=id)
#                 except customer.DoesNotExist:
#                     data = None
#                 if data!=None:
#                     serializer = customerSerializer(data)
#                     cache.set(id, serializer.data)
#                     return Response(serializer.data, status=status.HTTP_200_OK)
#                 else:
#                     return Response("No record against this id",status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response(e, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id=None):
#         try:
#             key = (cache.keys('*'))
#             for i in key:
#                 if i == str(id):
#                     index = key.index(i)
#                     key = key[index]
#                 else:
#                     key = None
#
#             if (key != None):
#                 try:
#                     c_data = customer.objects.get(id=id)
#                 except customer.DoesNotExist:
#                     c_data = None
#                 if c_data!=None:
#                     serializer = customerSerializer(c_data, data=request.data)
#                     if serializer.is_valid():
#                         serializer.save()
#                         cache.set(key, serializer.data)
#                         return Response(serializer.data, status=status.HTTP_201_CREATED)
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response("No record against this id", status=status.HTTP_404_NOT_FOUND)
#             else:
#                 return Response("No record against this id", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#             return Response(e, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id=None):
#         try:
#             key = cache.keys('*')
#             for i in key:
#                 if i == str(id):
#                     index = key.index(i)
#                     key = key[index]
#                 else:
#                     key = None
#
#             try:
#                 data = customer.objects.get(id=id)
#             except customer.DoesNotExist:
#                 data = None
#             if data!=None:
#                 data.delete()
#                 cache.delete(key)
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             else:
#                 return Response("No record against this id", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response(e)


# class placing view will get the total order detail with the detail of customer and will send email after some
# specified time to receive their order!


class placing_order(APIView):
    def get(self,request, id=None):
        try:
            data = orders.objects.filter(id=id).values('description', 'buyer__customer_name', 'buyer__email',
                                                       'seller__salesperson_name', 'quantity')
            if len(data) !=0:
                if cache.get(id):
                    print("FROM CHACHE")
                    data = cache.get(id)
                else:
                    print("FROM DATABASE")
                    cache.set(id, data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Order Does Not exits", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response("Error!", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):
        try:
            data = orders.objects.filter(id=id).values('description', 'buyer__customer_name', 'buyer__email',
                                                           'seller__salesperson_name', 'quantity')
            if len(data) != 0:
                if cache.get(id):
                    print("FROM CHACHE")
                    data = cache.get(id)
                    email = data[0]['buyer__email']
                    client = data[0]['buyer__customer_name']
                    desc = data[0]['description']
                else:
                    print("FROM DATABASE")
                    email = data[0]['buyer__email']
                    client = data[0]['buyer__customer_name']
                    desc = data[0]['description']
                    cache.set(id, data)

                delivery_email.delay(email, "Delivered",
                                     "Mr." + client + " Your order " + desc + " is placed successfully. Your order will"
                                                                              " at your doorstep in 45 minutes!")
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Order Does Not exits", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response("Error!", status=status.HTTP_400_BAD_REQUEST)


class orderDetails(APIView):
    def get(self, request, id=None):
        try:
            if cache.get(id):
                print("FROM CACHE")
                data = cache.get(id)
                return Response(data, status=status.HTTP_200_OK)
            else:
                print("FROM DATABASE")
                try:
                    data = orders.objects.get(id=id)
                except orders.DoesNotExist:
                    data = None
                if data!=None:
                    serializer = orderSerializer(data)
                    cache.set(id, serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Order Does Not exits", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            try:
                o_data = orders.objects.get(id=id)
            except orders.DoesNotExist:
                o_data = None

            if o_data != None:
                serializer = orderSerializer(o_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    cache.set(id, serializer.data)
                    return Response("order updated successfully!",status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Order Does Not exits in database", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            try:
                o_data = orders.objects.get(id=id)
            except orders.DoesNotExist:
                o_data = None

            if o_data != None:
                o_data.delete()
                cache.delete(id)
                return Response('Order successfully deleted!',status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Order Does Not exits in database", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)