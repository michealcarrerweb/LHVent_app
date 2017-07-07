from __future__ import unicode_literals

from datetime import datetime, timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from finance.models import (
    Pricing,
    Main,
    Ledger
)
from hourly.models import Hourly
from customer_finance.models import Invoice as Customer_Invoice
from operation_finance.models import Invoice as Operation_Invoice
from work_order.models import Order




class PricingTest(TestCase):

    def create_pricing(self):
        return Pricing.objects.create(
            pricing="ten",
            percentage=10
        )

    def test_pricing_creation(self):
        w = self.create_pricing()
        self.assertTrue(isinstance(w, Pricing))
        self.assertEqual(w.__str__(), w.pricing)


class MainTest(TestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.order = Order.objects.create(
            client=self.user,
            description="hardwork",
        )
        self.order2 = Order.objects.create(
            client=self.user,
            description="hardwork2",
        )

    def tearDown(self):
        del self.user
        del self.order

    def create_invoice(self):
        return Customer_Invoice.objects.create(
            work_order=self.order, 
            ledger=mommy.make('finance.Ledger'),
            pricing=mommy.make('finance.Pricing'),
            tax=6.00, 
            give_price_quote=False,
            paid_in_full=False,
            over_paid=False,
            conflict=False,
            conflict_description="Maybe not ever",
            note="back to",
            log="Maybe not ever back to",
            total_price_quoted=258.09,
            tax_on_quote=6.01
        )

    def create_invoice2(self):
        return Customer_Invoice.objects.create(
            work_order=self.order2, 
            ledger=mommy.make('finance.Ledger'),
            pricing=mommy.make('finance.Pricing'),
            tax=7.00, 
            give_price_quote=False,
            paid_in_full=False,
            over_paid=False,
            conflict=False,
            conflict_description="Maybe not ever2",
            note="back to2",
            log="Maybe not ever back to2",
            total_price_quoted=365.49,
            tax_on_quote=7.00
        )

    def create_operation_invoice(self):
        return Operation_Invoice.objects.create(
            invoice="Homedepot", 
            plu="23i74u56",
            ledger=mommy.make('finance.Ledger'), 
            invoice_amount=59.87,
            due_by=datetime.now()+timedelta(days=25), 
            conflict=False, 
            conflict_description="Oh now",
            note="today",
            paid_in_full=False,
            over_paid=False,
            log="oh now today"
        )

    def create_operation_invoice2(self):
        return Operation_Invoice.objects.create(
            invoice="Lowes", 
            plu="23i7990",
            ledger=mommy.make('finance.Ledger'), 
            invoice_amount=659.87,
            due_by=datetime.now()+timedelta(days=25), 
            conflict=False, 
            conflict_description="Oh now2",
            note="today2",
            paid_in_full=False,
            over_paid=False,
            log="oh now today2"
        )

    def create_hourly(self):
        return Hourly.objects.create(
            hourly_base=10
        )

    def create_user(self):
        return User.objects.create(
            username="Jerry",
            email="jerry@gmail.com"
        )

    def create_main(self):
        return Main.objects.create(main="trial parent ledger")

    def test_main_creation(self):
        w = self.create_main()
        self.create_user()
        self.create_hourly()
        self.create_invoice()
        self.create_invoice2()
        self.create_operation_invoice()
        self.create_operation_invoice2()
        self.assertTrue(isinstance(w, Main))
        self.assertEqual(w.__str__(), w.main)
        self.assertEqual(w.get_balance_sheet(), Decimal('-109.17'))


class LedgerTest(TestCase):

    def create_ledger(self):
        return Ledger.objects.create(
            parent=mommy.make(Main),
            ledger_name="trial ledger",
            revenue=False
        )

    def test_ledger_creation(self):
        w = self.create_ledger()
        self.assertTrue(isinstance(w, Ledger))
        self.assertEqual(w.__str__(), w.ledger_name)
        self.assertEqual(w.revenue, False)