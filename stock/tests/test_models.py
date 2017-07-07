from datetime import datetime, timedelta
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from stock.models import (
    Base,
    Company,
    Product
)
# from hourly.models import Hourly
# from customer_finance.models import Invoice as Customer_Invoice
# from operation_finance.models import Invoice as Operation_Invoice
# from work_order.models import Order


class BaseTest(TestCase):

    def create_base(self):
        return Base.objects.create(category="Usable")

    def test_base_creation(self):
        w = self.create_base()
        self.assertTrue(isinstance(w, Base))
        self.assertEqual(w.__str__(), w.category)


class CompanyTest(TestCase):

    def create_company(self):
        return Company.objects.create(
            company="Lowes",
            address="2333 nowhwere",
            company_phone="223 444 5555", 
            contact_first_name="jerry",
            contact_last_name="tom",
            phone=2145556666, 
            email="twa@gmail.com",
            discontinued=False,
            no_longer_use=False
        )

    def test_company_creation(self):
        w = self.create_company()
        self.assertTrue(isinstance(w, Company))
        self.assertEqual(w.__str__(), w.company)


# class MainTest(TestCase):

#     def setUp(self):
#         self.user = mommy.make(User)
#         self.order = Order.objects.create(
#             client=self.user,
#             description="hardwork",
#         )
#         self.order2 = Order.objects.create(
#             client=self.user,
#             description="hardwork2",
#         )

#     def tearDown(self):
#         del self.user
#         del self.order

#     def create_invoice(self):
#         return Customer_Invoice.objects.create(
#             work_order=self.order, 
#             ledger=mommy.make('finance.Ledger'),
#             pricing=mommy.make('finance.Pricing'),
#             tax=6.00, 
#             give_price_quote=False,
#             paid_in_full=False,
#             over_paid=False,
#             conflict=False,
#             conflict_description="Maybe not ever",
#             note="back to",
#             log="Maybe not ever back to",
#             total_price_quoted=258.09,
#             tax_on_quote=6.01
#         )

#     def create_invoice2(self):
#         return Customer_Invoice.objects.create(
#             work_order=self.order2, 
#             ledger=mommy.make('finance.Ledger'),
#             pricing=mommy.make('finance.Pricing'),
#             tax=7.00, 
#             give_price_quote=False,
#             paid_in_full=False,
#             over_paid=False,
#             conflict=False,
#             conflict_description="Maybe not ever2",
#             note="back to2",
#             log="Maybe not ever back to2",
#             total_price_quoted=365.49,
#             tax_on_quote=7.00
#         )

#     def create_operation_invoice(self):
#         return Operation_Invoice.objects.create(
#             invoice="Homedepot", 
#             plu="23i74u56",
#             ledger=mommy.make('finance.Ledger'), 
#             invoice_amount=59.87,
#             due_by=datetime.now()+timedelta(days=25), 
#             conflict=False, 
#             conflict_description="Oh now",
#             note="today",
#             paid_in_full=False,
#             over_paid=False,
#             log="oh now today"
#         )

#     def create_operation_invoice2(self):
#         return Operation_Invoice.objects.create(
#             invoice="Lowes", 
#             plu="23i7990",
#             ledger=mommy.make('finance.Ledger'), 
#             invoice_amount=659.87,
#             due_by=datetime.now()+timedelta(days=25), 
#             conflict=False, 
#             conflict_description="Oh now2",
#             note="today2",
#             paid_in_full=False,
#             over_paid=False,
#             log="oh now today2"
#         )

#     def create_hourly(self):
#         return Hourly.objects.create(
#             hourly_base=10
#         )

#     def create_user(self):
#         return User.objects.create(
#             username="Jerry",
#             email="jerry@gmail.com"
#         )

#     def create_main(self):
#         return Main.objects.create(main="trial parent ledger")

#     def test_main_creation(self):
#         w = self.create_main()
#         self.create_user()
#         self.create_hourly()
#         self.create_invoice()
#         self.create_invoice2()
#         self.create_operation_invoice()
#         self.create_operation_invoice2()
#         self.assertTrue(isinstance(w, Main))
#         self.assertEqual(w.__str__(), w.main)
#         self.assertEqual(w.get_balance_sheet(), Decimal('-109.17'))


# class LedgerTest(TestCase):

#     def create_ledger(self):
#         return Ledger.objects.create(
#             parent=mommy.make(Main),
#             ledger_name="trial ledger",
#             revenue=False
#         )

#     def test_ledger_creation(self):
#         w = self.create_ledger()
#         self.assertTrue(isinstance(w, Ledger))
#         self.assertEqual(w.__str__(), w.ledger_name)
#         self.assertEqual(w.revenue, False)


# # class InvoiceTest(TestCase):

#     # def create_invoice(self):
#     #     return Invoice.objects.create(
#     #     	invoice="new", 
#     #         plu="12j34u", 
    #         ledger=0, 
    #         invoice_amount=233.09, 
    #         due_by="10-10-1997",
    #         conflict_description="Maybe not ever",
    #         note="back to",
    #         power_ball_number=25
    #     )

    # def create_entry_second(self):
    #     return Entry.objects.create(
    #         first_name="Lisa", 
    #         last_name="Hope", 
    #         first_favorite=5, 
    #         second_favorite=11, 
    #         third_favorite=67,
    #         fourth_favorite=56,
    #         fifth_favorite=3,
    #         power_ball_number=25
    #     )

    # def create_entry_third(self):
    #     return Entry.objects.create(
    #         first_name="Harry", 
    #         last_name="Lumpe", 
    #         first_favorite=5, 
    #         second_favorite=19, 
    #         third_favorite=67,
    #         fourth_favorite=8,
    #         fifth_favorite=33,
    #         power_ball_number=4
    #     )

#     def test_invoice(self):
#         w = self.create_invoice()
        # self.assertTrue(isinstance(w, Entry))
        # self.assertEqual(w.__str__(), "George Lane  2-3-23-45-67, Power ball-25")
        # self.assertEqual(w.all_favorite_balls, {3: 1, 2: 1, 67: 1, 45: 1, 23: 1})
        # self.assertEqual(w.all_powerballs, {25: 1})
        # w.save()
        # another_w = self.create_entry_second()
        # self.assertTrue(isinstance(another_w, Entry))
        # self.assertEqual(another_w.__str__(), "Lisa Hope  3-5-11-56-67, Power ball-25")
        # self.assertEqual(another_w.all_favorite_balls, {67: 2, 3: 2, 5: 1, 23: 1, 56: 1, 2: 1, 11: 1, 45: 1})
        # self.assertEqual(another_w.all_powerballs, {25: 2})
        # another_w.save()
        # yet_another_w = self.create_entry_third()
        # self.assertTrue(isinstance(yet_another_w, Entry))
        # self.assertEqual(yet_another_w.__str__(), "Harry Lumpe  5-8-19-33-67, Power ball-4")
        # self.assertEqual(yet_another_w.all_favorite_balls, {3: 2, 33: 1, 2: 1, 67: 3, 5: 2, 8: 1, 11: 1, 45: 1, 19: 1, 23: 1, 56: 1})
        # self.assertEqual(yet_another_w.all_powerballs, {25: 2, 4: 1})


# class EntryModelFunctionTests(TestCase):

#     def test_most_popular_balls1(self):
#         sorted_dict = most_popular_balls(
#             [
#                 (1, 7), 
#                 (5, 7), 
#                 (2, 5), 
#                 (3, 5), 
#                 (4, 5), 
#                 (7, 4), 
#                 (66, 4), 
#                 (56, 3), 
#                 (6, 2), 
#                 (67, 2), 
#                 (23, 2), 
#                 (68, 2), 
#                 (34, 2), 
#                 (45, 2), 
#                 (55, 2), 
#                 (65, 1), 
#                 (8, 1), 
#                 (12, 1), 
#                 (43, 1), 
#                 (24, 1), 
#                 (33, 1), 
#                 (44, 1), 
#                 (57, 1), 
#                 (58, 1), 
#                 (59, 1)
#             ]
#         )
#         self.assertEqual(sorted_dict, [1, 2, 3, 4, 5])

#     def test_most_popular_balls2(self):
#         sorted_dict = most_popular_balls(
#             [
#                 (1, 7), 
#                 (5, 7), 
#                 (22, 7), 
#                 (3, 7), 
#                 (41, 7), 
#                 (7, 4), 
#                 (66, 4), 
#                 (56, 3), 
#                 (6, 2), 
#                 (67, 2), 
#                 (23, 2), 
#                 (68, 2), 
#                 (34, 2), 
#                 (45, 2), 
#                 (55, 2), 
#                 (65, 1), 
#                 (8, 1), 
#                 (12, 1), 
#                 (43, 1), 
#                 (24, 1), 
#                 (33, 1), 
#                 (44, 1), 
#                 (57, 1), 
#                 (58, 1), 
#                 (59, 1)
#             ]
#         )
#         self.assertEqual(sorted_dict, [1, 3, 5, 22, 41])

#     def test_most_popular_balls3(self):
#         sorted_dict = most_popular_balls(
#             [
#                 (1, 7), 
#                 (5, 7), 
#                 (22, 6), 
#                 (3, 5), 
#                 (41, 4), 
#                 (7, 4), 
#                 (66, 4), 
#                 (56, 4), 
#                 (6, 4), 
#                 (67, 4), 
#                 (23, 2),  
#                 (55, 2), 
#                 (65, 1), 
#                 (8, 1), 
#                 (12, 1) 
#             ]
#         )
#         compared_list = [1, 3, 5, 6, 7, 22, 41, 56, 66, 67]
#         [self.assertTrue(i in compared_list) for i in sorted_dict]
#         self.assertTrue(len(set(sorted_dict)) == 5)

#     def test_most_popular_powerball1(self):
#         sorted_dict = most_popular_powerball(
#             [
#                 (1, 9), 
#                 (5, 7), 
#                 (2, 5), 
#                 (3, 5), 
#                 (4, 5), 
#                 (7, 4), 
#                 (6, 2), 
#                 (23, 2), 
#                 (34, 2),  
#                 (8, 1), 
#                 (12, 1), 
#                 (24, 1)
#             ]
#         )
#         self.assertEqual(sorted_dict, 1)

#     def test_most_popular_powerball2(self):
#         powerball_pick = most_popular_powerball(
#             [
#                 (2, 5), 
#                 (3, 5), 
#                 (4, 5), 
#                 (7, 4), 
#                 (6, 2), 
#                 (23, 2), 
#                 (34, 2),  
#                 (8, 1), 
#                 (12, 1), 
#                 (24, 1)
#             ]
#         )
#         self.assertTrue(powerball_pick in [2, 3, 4])
#         self.assertFalse(powerball_pick in [7, 6, 23, 34, 8, 12, 24])


# class EntryModelFunctionTestsSeparate(TestCase):

#     def test_most_popular_balls4(self):
#         sorted_dict = most_popular_balls(
#             [
#                 (11, 1), 
#                 (14, 1), 
#                 (22, 1), 
#                 (37, 1),  
#                 (46, 1), 
#                 (58, 1), 
#                 (62, 1) 
#             ]
#         )
#         optional_list = [i for i in range(1, 70)]
#         [self.assertTrue(i in optional_list) for i in sorted_dict]
#         self.assertTrue(len(set(sorted_dict)) == 5)

#     def test_most_popular_balls5(self):
#         sorted_dict = most_popular_balls(
#             [
#                 (11, 3), 
#                 (14, 2), 
#                 (22, 1), 
#                 (37, 1),  
#                 (46, 1), 
#                 (58, 1), 
#                 (62, 1) 
#             ]
#         )
#         confirmed_list = [11, 14]
#         optional_list = [i for i in range(1, 70) if i not in confirmed_list]
#         random_only_list = [x for x in sorted_dict if x not in confirmed_list]
        
#         [self.assertTrue(i in sorted_dict) for i in confirmed_list]
#         [self.assertTrue(i in optional_list) for i in random_only_list]
#         self.assertTrue(len(set(sorted_dict)) == 5)

#     def test_most_popular_powerball3(self):
#         powerball_pick = most_popular_powerball(
#             [ 
#                 (8, 1), 
#                 (12, 1), 
#                 (24, 1)
#             ]
#         )
#         self.assertFalse(powerball_pick in [8, 12, 24])
#         self.assertTrue(powerball_pick in range(1, 27))


