from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.utils import timezone

# api/purchase_orders
class PurchaseOrderListCreateView(APIView):
    # GET Request to fetch all Purchase Orders
    # Headers - Authorization : Token {auth_token}
    # Usage : GET http://localhost:5000/api/purchase_orders
    def get(self, request):
        # Retrieve all purchase orders
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    
    # POST Request to create a new Purchase Order
    # Headers - Authorization : Token {auth_token}
    # Usage : POST http://localhost:5000/api/purchase_orders/
    def post(self, request):
        # Create new purchase order
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {"message":"Created Successfully!","data":serializer.data}
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api/purchase_orders/{id}
class PurchaseOrderRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return None
        
    # GET Request to fetch Purchase Order using ID
    # Headers - Authorization : Token {auth_token}
    # Usage : GET http://localhost:5000/api/purchase_orders/{id}/
    def get(self, request, pk):
        # Fetch purchase order by ID
        purchase_order = self.get_object(pk)
        if purchase_order:
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        else:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT Request to update Purchase Order details
    # Headers - Authorization : Token {auth_token}
    # Usage : PUT http://localhost:5000/api/purchase_orders/{id}/
    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        if purchase_order:
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE Request to delete a Purchase Order
    # Headers - Authorization : Token {auth_token}
    # Usage : DELETE http://localhost:5000/api/purchase_orders/{id}/
    def delete(self, request, pk):
        purchase_order = self.get_object(pk)
        if purchase_order:
            purchase_order.delete()
            return Response({"message": "Purchase order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

# api/purchase_orders/{id}/acknowledge
class PurchaseOrderAcknowledgeView(APIView):
    # Fetch object using ID
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return None
    
    # POST Request to update PO's status to acknowledged
    # Headers - Authorization : Token {auth_token}
    # Usage : POST http://localhost:5000/api/purchase_orders/{id}/acknowledge
    def post(self, request, pk):
        try:
            purchase_order = self.get_object(pk)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
        if purchase_order.acknowledgment_date:
            return Response({'error': 'Purchase order already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.status = 'acknowledged'
        purchase_order.save()
        return Response(PurchaseOrderSerializer(purchase_order).data)

# api/purchase_orders/{id}/complete
class PurchaseOrderCompletionView(APIView):
    # POST Request to update PO's status to completed
    # Headers - Authorization : Token {auth_token}
    # Usage : POST http://localhost:5000/api/purchase_orders/{id}/complete
    def post(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            if purchase_order.acknowledgment_date == None:
                return Response({'message': 'Purchase order is not acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)
            if purchase_order.status == 'completed':
                return Response({'message': 'Purchase order already completed.'}, status=status.HTTP_400_BAD_REQUEST)
            quality_rating = request.data.get('quality_rating')
            if quality_rating is not None:
                # Update purchase order with quality rating
                purchase_order.quality_rating = quality_rating
                purchase_order.save()
            purchase_order.complete_order()  # Call the method from the model
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Purchase order not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error completing purchase order: {e}'}, status=status.HTTP_400_BAD_REQUEST)

# api/purchase_orders/{id}/cancel
class PurchaseOrderCancellationView(APIView):
    # POST Request to update PO's status to cancelled
    # Headers : Authorization : Token {auth_token}
    # Usage : POST http://localhost:5000/api/purchase_orders/{id}/cancel
    def post(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            if purchase_order.acknowledgment_date == None:
                return Response({'message': 'Purchase order is not acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)
            if purchase_order.status == 'completed':
                return Response({'message': 'Purchase order is completed.'}, status=status.HTTP_400_BAD_REQUEST)
            if purchase_order.status == 'cancelled':
                return Response({'message': 'Purchase order already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
            purchase_order.cancel_order()  # Call the method from the model
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Purchase order not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error completing purchase order: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        