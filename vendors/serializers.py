from rest_framework import serializers
from .models import Vendor, HistoricalPerformance

# Vendor Serializer
class VendorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vendor
    fields = '__all__'

# Historical Performance Serializer
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = HistoricalPerformance
    fields = '__all__'
