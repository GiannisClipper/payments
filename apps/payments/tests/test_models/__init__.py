from unittest import skip  # noqa: F401
from django.core.exceptions import ValidationError
import datetime

from django.contrib.auth import get_user_model

from funds.models import Fund
from genres.models import Genre
from payments.models import Payment

from payments.tests import PaymentsTests


class PaymentModelTests(PaymentsTests):
    pass


class PaymentModelBasicTests(PaymentModelTests):

    def test_model_structure(self):
        fields = [x.name for x in Payment._meta.get_fields()]

        self.assertTrue('user' in fields)
        self.assertTrue('date' in fields)
        self.assertTrue('genre' in fields)
        self.assertTrue('incoming' in fields)
        self.assertTrue('outgoing' in fields)
        self.assertTrue('fund' in fields)
        self.assertTrue('remarks' in fields)

    def test_create(self):
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)

        self.assertEqual(payment1.user.id, payment_['user']['id'])
        self.assertEqual(payment1.date,
            datetime.datetime.strptime(payment_['date'], "%Y-%m-%d").date())
        self.assertEqual(payment1.genre.id, payment_['genre']['id'])
        payment_['incoming'] = payment_['incoming'] if payment_['incoming'] else 0
        payment_['outgoing'] = payment_['outgoing'] if payment_['outgoing'] else 0
        self.assertEqual(payment1.incoming, payment_['incoming'])
        self.assertEqual(payment1.outgoing, payment_['outgoing'])
        self.assertEqual(payment1.fund.id, payment_['fund']['id'])
        payment_['remarks'] = payment_['remarks'] if payment_['remarks'] else ''
        self.assertEqual(payment1.remarks, payment_['remarks'])

    def test_update(self):
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)
        payment_ = self.samples['payments'][12]
        payment_.pop('user', None)
        payment_['fund'] = Fund.objects.get(pk=payment_['fund']['id'])
        payment_['genre'] = Genre.objects.get(pk=payment_['genre']['id'])
        payment2 = payment1.update(**payment_)

        self.assertEqual(payment2, payment1)
        self.assertEqual(payment2.date,
            datetime.datetime.strptime(payment_['date'], "%Y-%m-%d").date())
        self.assertEqual(payment2.genre, payment_['genre'])
        payment_['incoming'] = payment_['incoming'] if payment_['incoming'] else 0
        payment_['outgoing'] = payment_['outgoing'] if payment_['outgoing'] else 0
        self.assertEqual(payment2.incoming, payment_['incoming'])
        self.assertEqual(payment2.outgoing, payment_['outgoing'])
        self.assertEqual(payment2.fund, payment_['fund'])
        payment_['remarks'] = payment_['remarks'] if payment_['remarks'] else ''
        self.assertEqual(payment2.remarks, payment_['remarks'])

    def test_delete(self):
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)

        payment1.delete()  # Built-in method

        self.assertEqual(payment1.pk, None)

    def test_str_representation(self):
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)
        amount = payment1.incoming if payment1.genre.is_incoming else payment1.outgoing

        self.assertEqual(str(payment1),
            f'{payment1.genre.name} {payment1.date} {amount} {payment1.remarks}')


class PaymentModelValidationOnCreateTests(PaymentModelTests):

    def test_required_errors(self):
        errors = ''
        payment_ = self.samples['payments'][11]
        payment_.pop('user', None)
        payment_.pop('date', None)
        payment_.pop('genre', None)
        payment_.pop('incoming', None)
        payment_.pop('outgoing', None)
        payment_.pop('fund', None)

        try:
            Payment.objects.create(**payment_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('date', errors.keys())
        self.assertIn('genre', errors.keys())
        self.assertNotIn('incoming', errors.keys())
        self.assertNotIn('outgoing', errors.keys())
        self.assertIn('fund', errors.keys())
        self.assertNotIn('remarks', errors.keys())

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        payment_ = self.samples['payments'][11]
        payment_['user'] = None
        payment_['date'] = '        '
        payment_['genre'] = None
        payment_['incoming'] = 0
        payment_['outgoing'] = 0
        payment_['fund'] = None
        payment_['remarks'] = '        '

        try:
            Payment.objects.create(**payment_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('date', errors.keys())
        self.assertIn('genre', errors.keys())
        self.assertNotIn('incoming', errors.keys())
        self.assertNotIn('outgoing', errors.keys())
        self.assertIn('fund', errors.keys())
        self.assertNotIn('remarks', errors.keys())

    def test_unique_errors(self):
        errors = ''
        payment_ = self.samples['payments'][11]
        payment_['remarks'] = None
        self.create_payment(**payment_)

        try:
            self.create_payment(**payment_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(1, len(errors['__all__']))


class PaymentModelValidationOnUpdateTests(PaymentModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)
        payment_['user'] = None
        payment_['date'] = '        '
        payment_['genre'] = None
        payment_['incoming'] = 0
        payment_['outgoing'] = 0
        payment_['fund'] = None
        payment_['remarks'] = '        '

        try:
            payment1.update(**payment_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('date', errors.keys())
        self.assertIn('genre', errors.keys())
        self.assertNotIn('incoming', errors.keys())
        self.assertNotIn('outgoing', errors.keys())
        self.assertIn('fund', errors.keys())
        self.assertNotIn('remarks', errors.keys())

    def test_unique_errors(self):
        errors = ''
        payment_ = self.samples['payments'][11]
        payment1 = self.create_payment(**payment_)
        payment_ = self.samples['payments'][12]
        payment2 = self.create_payment(**payment_)
        payment_ = self.samples['payments'][11]
        payment_.pop('user', None)
        payment_['genre'] = payment1.genre
        payment_['fund'] = payment1.fund

        try:
            payment2.update(**payment_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(1, len(errors['__all__']))
