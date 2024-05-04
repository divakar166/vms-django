from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, HistoricalPerformance
from .serializers import VendorSerializer, HistoricalPerformanceSerializer
from purchase_orders.models import PurchaseOrder
from purchase_orders.serializers import PurchaseOrderSerializer

# api/vendors/
class VendorListCreateView(APIView):
  # GET Request to fetch Vendors
  # Headers : Authorization : Token {auth_token}
  # Usage : GET http://localhost:5000/api/vendors/
  def get(self, request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)

  # POST Request to create new Vendor
  # Headers : Authorization : Token {auth_token}
  # Usage : POST http://localhost:5000/api/vendors/ data
  def post(self, request):
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api/vendors/:id
class VendorRetrieveUpdateDestroyView(APIView):
  # Get Object using id
  def get_object(self, pk):
    try:
      return Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
      raise 'Http404'

  # GET Request to fetch Vendor details using ID
  # Headers : Authorization : Token {auth_token}
  # Usage : GET http://localhost:5000/api/vendors/{id}
  def get(self, request, pk):
    try:
      vendor = self.get_object(pk)
      serializer = VendorSerializer(vendor)
      return Response(serializer.data)
    except:
      res = {"message":"Vendor doesn't exist!"}
      return Response(res,status=status.HTTP_400_BAD_REQUEST)

  # PUT Request to update vendor details
  # Headers : Authorization : Token {auth_token}
  # Usage : PUT http://localhost:5000/api/vendors/{id} data-to-update
  def put(self, request, pk):
    try:
      vendor = self.get_object(pk)
      serializer = VendorSerializer(vendor, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
      res = {"message":"Vendor doesn't exist!"}
      return Response(res,status=status.HTTP_400_BAD_REQUEST)

  # DELETE Request to delete vendor
  # Headers : Authorization : Token {auth_token}
  # Usage : DELETE http://localhost:5000/api/vendors/{id}
  def delete(self, request, pk):
    try:
      vendor = self.get_object(pk)
      if vendor:
        vendor.delete()
        res = {"message":"Vendor deleted successfully!"}
        return Response(res,status=status.HTTP_200_OK)
    except:
      res = {"message":"Vendor doesn't exist!"}
      return Response(res,status=status.HTTP_400_BAD_REQUEST)

# api/vendors/:id/performance
class VendorPerformanceView(APIView):
  # GET Request to fetch Vendor's performance metrics
  # Headers : Authorization : Token {auth_token}
  # Usage : GET http://localhost:5000/api/vendors/{id}/performance
  def get(self, request, pk):
    try:
      vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
      raise 'Http404'

    # Check if historical data exists for the vendor
    historical_data = HistoricalPerformance.objects.filter(vendor=vendor)
    if historical_data.exists():
        # Calculate average metrics from historical data
        total_on_time_delivery_rate = 0
        total_quality_rating_avg = 0
        total_average_response_time = 0
        total_fulfillment_rate = 0
        num_data_points = historical_data.count()
        for data_point in historical_data:
            total_on_time_delivery_rate += data_point.on_time_delivery_rate
            total_quality_rating_avg += data_point.quality_rating_avg
            total_average_response_time += data_point.average_response_time
            total_fulfillment_rate += data_point.fulfillment_rate

        # Update vendor's performance metrics
        vendor.on_time_delivery_rate = total_on_time_delivery_rate / num_data_points
        vendor.quality_rating_avg = total_quality_rating_avg / num_data_points
        vendor.average_response_time = total_average_response_time / num_data_points
        vendor.fulfillment_rate = total_fulfillment_rate / num_data_points
        vendor.save()

    # Return vendor's performance metrics
    performance_data = {
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate,
    }
    return Response(performance_data)

# api/vendors/:id/pos
class VendorPosView(APIView):
  # GET Request to fetch all Purchase Order's associated to Vendor
  # Headers : Authorization : Token {auth_token}
  # Usage : GET http://localhost:5000/api/vendors/{id}/pos
  def get(self, request, pk):
    try:
      vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
      return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    pos = PurchaseOrder.objects.filter(vendor=vendor)
    serializer = PurchaseOrderSerializer(pos, many=True)
    res = {"pos":pos.count(),"data":serializer.data}
    return Response(res)
  
# api/vendors/:id/historical_perf
class VendorHistoricalPerfView(APIView):
  # GET Request to fetch Historical Performance of Vendor
  # Headers : Authorization : Token {auth_token}
  # Usage : GET http://localhost:5000/api/vendors/{id}/historical_perf
  def get(self, request, pk):
    try:
      vendor = Vendor.objects.get(pk=pk)
      historicPerformance = HistoricalPerformance.objects.filter(vendor=vendor)
      serializer = HistoricalPerformanceSerializer(historicPerformance, many=True)
      return Response(serializer.data,status=status.HTTP_200_OK)
    except Vendor.DoesNotExist:
      return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
