from django.core.exceptions import ValidationError

from unittest import skip  # noqa: F401

from funds.models import Fund
from funds.tests import FundsTests


class FundModelTests(FundsTests):
    pass


class FundModelBasicTests(FundModelTests):

    def test_model_structure(self):
        fields = [x.name for x in Fund._meta.get_fields()]

        self.assertTrue('user' in fields)
        self.assertTrue('code' in fields)
        self.assertTrue('name' in fields)

    def test_create(self):
        fund = Fund.objects.create(**self.samples[0])

        self.assertEqual(fund.user.id, self.samples[0]['user'].id)
        self.assertEqual(fund.code, self.samples[0]['code'])
        self.assertEqual(fund.name, self.samples[0]['name'])

    def test_update(self):
        fund1 = Fund.objects.create(**self.samples[0])
        fund2 = fund1.update(**self.samples[1])

        self.assertEqual(fund1, fund2)

    def test_delete(self):
        fund = Fund.objects.create(**self.samples[0])
        fund.delete()  # Built-in method

        self.assertEqual(fund.pk, None)

    def test_str_representation(self):
        fund = Fund.objects.create(**self.samples[0])

        self.assertEqual(str(fund), self.samples[0]['name'])


class FundModelValidationOnCreateTests(FundModelTests):

    def test_required_errors(self):
        errors = ''
        del self.samples[0]['user']
        del self.samples[0]['code']
        del self.samples[0]['name']

        try:
            Fund.objects.create(**self.samples[0])
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        self.samples[0]['user'] = None
        self.samples[0]['code'] = '        '
        self.samples[0]['name'] = '        '

        try:
            Fund.objects.create(**self.samples[0])
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_unique_errors(self):
        errors = ''
        Fund.objects.create(**self.samples[0])

        try:
            Fund.objects.create(**self.samples[0])
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_valid_same_fields_for_different_users(self):
        self.samples[0]['user'] = self.user1
        fund1 = Fund.objects.create(**self.samples[0])
        self.samples[0]['user'] = self.user2
        fund2 = Fund.objects.create(**self.samples[0])

        self.assertNotEqual(fund1.user, fund2.user)
        self.assertEqual(fund1.code, fund2.code)
        self.assertEqual(fund1.name, fund2.name)


class FundModelValidationOnUpdateTests(FundModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        fund = Fund.objects.create(**self.samples[0])
        self.samples[0]['user'] = None
        self.samples[0]['code'] = '        '
        self.samples[0]['name'] = '        '

        try:
            fund.update(**self.samples[0])
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_unique_errors(self):
        errors = ''
        Fund.objects.create(**self.samples[0])
        fund = Fund.objects.create(**self.samples[1])

        try:
            fund.update(**self.samples[0])
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_valid_same_fields_for_different_users(self):
        self.samples[0]['user'] = self.user1
        fund1 = Fund.objects.create(**self.samples[0])
        fund2 = Fund.objects.create(**self.samples[1])
        self.samples[0]['user'] = self.user2
        fund2.update(**self.samples[0])

        self.assertNotEqual(fund1.user, fund2.user)
        self.assertEqual(fund1.code, fund2.code)
        self.assertEqual(fund1.name, fund2.name)
