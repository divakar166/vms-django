from django.urls import path
from .views import *

# Urls
urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
    path('<int:pk>/performance',VendorPerformanceView.as_view(), name='vendor-performance'),
    path('<int:pk>/pos',VendorPosView.as_view(), name='vendor-pos'),
    path('<int:pk>/historical_perf',VendorHistoricalPerfView.as_view(), name='vendor-historical')
]
