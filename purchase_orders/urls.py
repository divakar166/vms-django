from django.urls import path, include
from .views import *

urlpatterns = [
  path('', PurchaseOrderListCreateView.as_view(), name='pos-list-create'),
  path('<int:pk>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='pos-retrieve-update-destroy'),
  path('<int:pk>/acknowledge/',PurchaseOrderAcknowledgeView.as_view(), name='pos-acknowledge'),
  path('<int:pk>/complete/',PurchaseOrderCompletionView.as_view(), name='pos-completion'),
  path('<int:pk>/cancel/',PurchaseOrderCancellationView.as_view(), name='pos-cancellation'),
]