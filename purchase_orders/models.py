from django.db import models
from vendors.models import Vendor
from django.utils import timezone

# Purchase Order Model
class PurchaseOrder(models.Model):
  po_number = models.CharField(max_length=100, blank=True, default='')
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  order_date = models.DateTimeField()
  delivery_date = models.DateTimeField()
  items = models.JSONField()
  quantity = models.IntegerField()
  status = models.CharField(max_length=20,choices=(
    ('pending','Pending'),
    ('acknowledged','Acknowledged by Vendor'),
    ('completed','Completed'),
    ('cancelled','Cancelled')
  ),default='pending')
  quality_rating = models.FloatField(null=True, blank=True)
  issue_date = models.DateTimeField(auto_now_add=True)
  acknowledgment_date = models.DateTimeField(null=True, blank=True)
  completed_at = models.DateTimeField(blank=True, null=True)

  # On Save method
  def save(self, *args, **kwargs):
    if not self.po_number:
      last_po_number = PurchaseOrder.objects.order_by('-id').first()
      if last_po_number:
        last_po_number = int(last_po_number.po_number.split('-')[1])
      else:
        last_po_number = 0
      self.po_number = f'PO-{str(last_po_number + 1).zfill(3)}'
    super().save(*args, **kwargs)

  def complete_order(self):
    """Method to mark a purchase order as completed and update completed_at."""
    self.status = 'completed'
    self.completed_at = timezone.now()
    self.save()
  
  def cancel_order(self):
    """Method to mark a purchase order as completed and update completed_at."""
    self.status = 'cancelled'
    self.completed_at = timezone.now()
    self.save()

  def __str__(self):
    return f"PurchaseOrder #{self.po_number}"

