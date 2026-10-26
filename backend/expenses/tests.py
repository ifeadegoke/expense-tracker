from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Expense


class OwnershipTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='StrongPass123!')
        self.bob = User.objects.create_user(username='bob', password='StrongPass123!')
        self.alice_expense = Expense.objects.create(
            user=self.alice, category='Food',
            description='Alice lunch', amount=Decimal('1500.00'))
        self.bob_expense = Expense.objects.create(
            user=self.bob, category='Data',
            description='Bob airtime', amount=Decimal('500.00'))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_shows_only_own_expenses(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.get(reverse('expense_list'))
        self.assertContains(response, 'Alice lunch')
        self.assertNotContains(response, 'Bob airtime')

    def test_cannot_delete_another_users_expense(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.post(reverse('expense_delete', args=[self.bob_expense.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Expense.objects.filter(id=self.bob_expense.id).exists())

    def test_cannot_edit_another_users_expense(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.get(reverse('expense_edit', args=[self.bob_expense.id]))
        self.assertEqual(response.status_code, 404)

    def test_api_requires_login(self):
        response = self.client.get('/api/expenses/')
        self.assertIn(response.status_code, [401, 403])

    def test_api_lists_only_own_expenses(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, 200)
        descriptions = [item['description'] for item in response.json()]
        self.assertEqual(descriptions, ['Alice lunch'])

    def test_api_create_sets_owner(self):
        self.client.login(username='alice', password='StrongPass123!')
        response = self.client.post('/api/expenses/', {
            'category': 'Food',
            'description': 'Dinner',
            'amount': '2000.00',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.get(description='Dinner').user, self.alice)