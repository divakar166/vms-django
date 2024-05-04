from django.test import TestCase
from .models import Vendor, HistoricalPerformance
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from purchase_orders.models import PurchaseOrder
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime

# Model Test Cases
# Vendor Model Test Cases
class VendorModelTestCase(TestCase):
  def test_vendor_code_generation(self):
    vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address', email='test@example.com')
    self.assertEqual(vendor.vendor_code, 'VN001')

  def test_vendor_creation(self):
    vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address', email='test@example.com')
    self.assertEqual(vendor.name, 'Test Vendor')
    self.assertEqual(vendor.mobile_number, '1234567890')
    self.assertEqual(vendor.address, 'Test Address')
    self.assertEqual(vendor.email, 'test@example.com')

# Historical Performance Model Test Cases
class HistoricalPerformanceModelTestCase(TestCase):
  def setUp(self):
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address', email='test@example.com')
    
  def test_historical_performance_creation(self):
    performance = HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=0.9, quality_rating_avg=4.5, average_response_time=2.5, fulfillment_rate=0.95)
    self.assertEqual(performance.vendor, self.vendor)
    self.assertAlmostEqual(performance.on_time_delivery_rate, 0.9)
    self.assertAlmostEqual(performance.quality_rating_avg, 4.5)
    self.assertAlmostEqual(performance.average_response_time, 2.5)
    self.assertAlmostEqual(performance.fulfillment_rate, 0.95)

# Views Test Cases
# Vendor get & create views test cases
class VendorListCreateViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

  def test_create_vendor(self):
    url = reverse('vendor-list-create')
    data = {
      'name': 'Test Vendor',
      'mobile_number': '1234567890',
      'address': 'Test Address',
      'email': 'test@example.com'
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Vendor.objects.count(), 1)
    self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

  def test_get_vendors(self):
      Vendor.objects.create(name='Vendor 1', mobile_number='1234567890', address='Address 1')
      Vendor.objects.create(name='Vendor 2', mobile_number='9876543210', address='Address 2')

      url = reverse('vendor-list-create')
      response = self.client.get(url)

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 2)

# Vendor update views test cases
class VendorRetrieveUpdateDestroyViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')

    def test_get_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        data = {'name': 'Updated Vendor'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=self.vendor.pk).name, 'Updated Vendor')

    def test_delete_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Vendor.objects.filter(pk=self.vendor.pk).exists())

# Vendor performance view test cases
class VendorPerformanceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
        HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=0.9, quality_rating_avg=4.5, average_response_time=2.5, fulfillment_rate=0.95)

    def test_get_vendor_performance(self):
        url = reverse('vendor-performance', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 0.9)
        self.assertEqual(response.data['quality_rating_avg'], 4.5)
        self.assertEqual(response.data['average_response_time'], 2.5)
        self.assertEqual(response.data['fulfillment_rate'], 0.95)

# Vendor Po's view test cases
class VendorPosViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    order_date = datetime.datetime(2024, 5, 3, 12, 0, 0, tzinfo=datetime.timezone.utc)
    delivery_date = datetime.datetime(2024, 5, 5, 12, 0, 0, tzinfo=datetime.timezone.utc)
    self.purchase_order = PurchaseOrder.objects.create(vendor=self.vendor, order_date=order_date,  delivery_date=delivery_date, items={"item1":1}, quantity=1, status='completed')

  def test_get_vendor_pos(self):
    url = reverse('vendor-pos', kwargs={'pk': self.vendor.pk})
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['pos'], 1)
    self.assertEqual(len(response.data['data']), 1)
    self.assertEqual(response.data['data'][0]['po_number'], 'PO-001')
    self.assertEqual(response.data['data'][0]['status'], 'completed')
