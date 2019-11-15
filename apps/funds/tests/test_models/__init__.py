from unittest import skip  # noqa: F401
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

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
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)

        self.assertEqual(fund1.user.id, fund_['user']['id'])
        self.assertEqual(fund1.code, fund_['code'])
        self.assertEqual(fund1.name, fund_['name'])

    def test_update(self):
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)

        fund_ = self.samples['funds'][12]
        fund_.pop('user', None)
        fund2 = fund1.update(**fund_)

        self.assertEqual(fund2, fund1)
        self.assertEqual(fund2.code, fund_['code'])
        self.assertEqual(fund2.name, fund_['name'])

    def test_delete(self):
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)

        fund1.delete()  # Built-in method

        self.assertEqual(fund1.pk, None)

    def test_str_representation(self):
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)

        self.assertEqual(str(fund1), fund_['name'])


class FundModelValidationOnCreateTests(FundModelTests):

    def test_required_errors(self):
        errors = ''
        fund_ = self.samples['funds'][11]
        fund_.pop('user', None)
        fund_.pop('code', None)
        fund_.pop('name', None)

        try:
            Fund.objects.create(**fund_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        fund_ = self.samples['funds'][11]
        fund_['user'] = None
        fund_['code'] = '        '
        fund_['name'] = '        '

        try:
            Fund.objects.create(**fund_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_unique_errors(self):
        errors = ''
        fund_ = self.samples['funds'][11]
        self.create_fund(**fund_)

        try:
            self.create_fund(**fund_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_same_values_to_other_users(self):
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)

        fund_['user']['id'] = 2
        fund2 = self.create_fund(**fund_)

        self.assertNotEqual(fund1.user, fund2.user)
        self.assertEqual(fund1.code, fund2.code)
        self.assertEqual(fund1.name, fund2.name)


class FundModelValidationOnUpdateTests(FundModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)
        fund_['user'] = None
        fund_['code'] = '        '
        fund_['name'] = '        '

        try:
            fund1.update(**fund_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())

    def test_unique_errors(self):
        errors = ''
        fund_ = self.samples['funds'][11]
        self.create_fund(**fund_)
        fund_ = self.samples['funds'][12]
        fund2 = self.create_fund(**fund_)
        fund_ = self.samples['funds'][11]
        fund_.pop('user', None)

        try:
            fund2.update(**fund_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_same_values_to_other_users(self):
        fund_ = self.samples['funds'][11]
        fund1 = self.create_fund(**fund_)
        fund_ = self.samples['funds'][12]
        fund2 = self.create_fund(**fund_)

        fund_['user'] = get_user_model().objects.get(pk=2)
        fund1.update(**fund_)

        self.assertNotEqual(fund1.user, fund2.user)
        self.assertEqual(fund1.code, fund2.code)
        self.assertEqual(fund1.name, fund2.name)
