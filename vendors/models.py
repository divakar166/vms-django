from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Vendor Model
class Vendor(models.Model):
  name = models.CharField(max_length=100)
  mobile_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'\d{10,15}', message='Please enter a valid phone number (10-15 digits)')])
  address = models.TextField()
  vendor_code = models.CharField(max_length=20, unique=True, default='')
  email = models.EmailField(blank=True)
  on_time_delivery_rate = models.FloatField(default=0)
  quality_rating_avg = models.FloatField(default=0)
  average_response_time = models.FloatField(default=0)
  fulfillment_rate = models.FloatField(default=0)

  # On save method
  def save(self, *args, **kwargs):
    # Automatically generate vendor_code if not provided
    if not self.vendor_code:
      self.vendor_code = self.generate_vendor_code()
    super().save(*args, **kwargs)

  # Generate Vendor Code
  def generate_vendor_code(self):
    # Get the count of existing vendors
    count = Vendor.objects.count() + 1
    # Format the vendor code
    return f'VN{count:03d}'

# Historical Performance Model
class HistoricalPerformance(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  date = models.DateTimeField(default=timezone.now)
  on_time_delivery_rate = models.FloatField()
  quality_rating_avg = models.FloatField()
  average_response_time = models.FloatField()
  fulfillment_rate = models.FloatField()
  
  def __str__(self):
    return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"