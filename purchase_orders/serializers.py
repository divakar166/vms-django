from rest_framework import serializers
from .models import PurchaseOrder

# Purchase Order Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = PurchaseOrder
    fields = '__all__'