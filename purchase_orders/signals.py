from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.db.models import F, Avg
from vendors.models import HistoricalPerformance
import datetime

# Signal to update Vendor's performance metrics

# Main function
@receiver(post_save, sender=PurchaseOrder)
def handle_purchase_order_save(sender, instance, created, **kwargs):
  update_vendor_metrics(instance.vendor) # Update vendor metrics
  if created and instance.status=="acknowledged":  # Process newly created purchase orders (acknowledgments)
    update_response_time(instance)  # Update average response time
  else:  # Process updated purchase orders (potentially completed)
    if instance.status == 'completed':
      update_on_time_delivery_rate(instance)  # Update on-time delivery rate
      update_historical_performance(instance.vendor) # Update Historical performance of vendor
      if instance.quality_rating is not None:  # Update quality rating if completed with rating
        update_vendor_quality_rating(instance.vendor)
    if instance.status == 'cancelled':
      update_on_time_delivery_rate(instance)

# Update avg response time
def update_response_time(purchase_order):
  vendor = purchase_order.vendor
  # Calculate and update average response time (same logic as before)
  vendor_pos = PurchaseOrder.objects.filter(vendor=vendor)
  response_times = []
  for po in vendor_pos:
    if po.acknowledgment_date:
      issue_date = po.issue_date
      ack_date = po.acknowledgment_date
      response_time = ack_date - issue_date
      response_times.append(response_time.total_seconds() / 60)

  if response_times:
    average_response_time = sum(response_times) / len(response_times)
    vendor.average_response_time = average_response_time
    vendor.save()

# Update on time delivery rate
def update_on_time_delivery_rate(purchase_order):
  vendor = purchase_order.vendor
  total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
  on_time_deliveries = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__gte=F('completed_at')).count()

  on_time_delivery_rate = on_time_deliveries / total_completed_orders if total_completed_orders > 0 else 0.0

  vendor.on_time_delivery_rate = on_time_delivery_rate
  vendor.save()

# Update avg quality rating
def update_vendor_quality_rating(vendor):
  completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
  average_rating = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']

  if average_rating is not None:  # Handle cases where no completed orders with rating exist
    vendor.quality_rating_avg = average_rating
    vendor.save()

# Update Vendor Metrics & Fulfillment rate
def update_vendor_metrics(vendor):
  total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
  completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
  fulfillment_rate = completed_pos / total_pos if total_pos > 0 else 0.0

  vendor.fulfillment_rate = fulfillment_rate
  vendor.save()
  
def update_historical_performance(vendor):
  performance_record = HistoricalPerformance(
    vendor=vendor,
    on_time_delivery_rate=vendor.on_time_delivery_rate,
    quality_rating_avg=vendor.quality_rating_avg,
    average_response_time=vendor.average_response_time,
    fulfillment_rate=vendor.fulfillment_rate
  )
  performance_record.save()