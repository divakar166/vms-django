from django.test import TestCase
from django.utils import timezone
from .models import PurchaseOrder
from vendors.models import Vendor
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import PurchaseOrder
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PurchaseOrderModelTestCase(TestCase):
  def setUp(self):
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    self.purchase_order = PurchaseOrder.objects.create(
        vendor=self.vendor,
        order_date=timezone.now(),
        delivery_date=timezone.now(),
        items={"item1": 1},
        quantity=1
    )

  def test_purchase_order_creation(self):
    """Test creation of a PurchaseOrder instance."""
    self.assertIsInstance(self.purchase_order, PurchaseOrder)

  def test_po_number_generation(self):
    """Test automatic generation of PO number."""
    self.assertTrue(self.purchase_order.po_number.startswith('PO-'))

  def test_complete_order(self):
    """Test marking a purchase order as completed."""
    self.purchase_order.complete_order()
    self.assertEqual(self.purchase_order.status, 'completed')
    self.assertIsNotNone(self.purchase_order.completed_at)

  def test_str_representation(self):
    """Test string representation of a PurchaseOrder instance."""
    expected_string = f"PurchaseOrder #{self.purchase_order.po_number}"
    self.assertEqual(str(self.purchase_order), expected_string)

class PurchaseOrderListCreateViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    self.user = User.objects.create(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
    
  def test_create_purchase_order(self):
    url = reverse('pos-list-create')
    data = {
      'vendor': self.vendor.pk,
      'order_date': timezone.now(),
      'delivery_date': timezone.now() + timedelta(days=7),
      'items': {'item1': 1},
      'quantity': 1
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_get_purchase_orders(self):
    PurchaseOrder.objects.create(
      vendor=self.vendor,
      order_date=timezone.now(),
      delivery_date=timezone.now() + timedelta(days=7),
      items={'item1': 1},
      quantity=1,
      status='pending'
    )
    url = reverse('pos-list-create')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

class PurchaseOrderRetrieveUpdateDestroyViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    self.purchase_order = PurchaseOrder.objects.create(
      vendor=self.vendor,
      order_date=timezone.now(),
      delivery_date=timezone.now() + timedelta(days=7),
      items={'item1': 1},
      quantity=1,
      status='pending'
    )
    self.user = User.objects.create(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
    

  def test_retrieve_purchase_order(self):
    url = reverse('pos-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_update_purchase_order(self):
    url = reverse('pos-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
    data = {
      'status': 'completed'
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['status'], 'completed')

  def test_delete_purchase_order(self):
    url = reverse('pos-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PurchaseOrderAcknowledgeViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    self.purchase_order = PurchaseOrder.objects.create(
      vendor=self.vendor,
      order_date=timezone.now(),
      delivery_date=timezone.now() + timedelta(days=7),
      items={'item1': 1},
      quantity=1,
      status='pending'
    )
    self.user = User.objects.create(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
    

  def test_acknowledge_purchase_order(self):
    url = reverse('pos-acknowledge', kwargs={'pk': self.purchase_order.pk})
    response = self.client.post(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIsNotNone(PurchaseOrder.objects.get(pk=self.purchase_order.pk).acknowledgment_date)

class PurchaseOrderCompletionViewTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.vendor = Vendor.objects.create(name='Test Vendor', mobile_number='1234567890', address='Test Address')
    self.purchase_order = PurchaseOrder.objects.create(
      vendor=self.vendor,
      order_date=timezone.now(),
      delivery_date=timezone.now() + timedelta(days=7),
      items={'item1': 1},
      quantity=1,
      status='acknowledged',
      acknowledgment_date=timezone.now()
    )
    self.user = User.objects.create(username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
    


  def test_complete_purchase_order(self):
    url = reverse('pos-completion', kwargs={'pk': self.purchase_order.pk})
    response = self.client.post(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(PurchaseOrder.objects.get(pk=self.purchase_order.pk).status, 'completed')