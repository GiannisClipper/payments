from unittest import skip  # noqa: F401

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from funds.tests import FundsTests
from genres.tests import GenresTests

from genres.models import Genre


class GenreModelTests(GenresTests):
    pass


class GenreModelBasicTests(GenreModelTests):

    def test_model_structure(self):
        fields = [x.name for x in Genre._meta.get_fields()]

        self.assertTrue('user' in fields)
        self.assertTrue('code' in fields)
        self.assertTrue('name' in fields)
        self.assertTrue('is_income' in fields)
        self.assertTrue('fund' in fields)

    def test_create(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        fund_ = self.samples['funds'][0][0]
        fund1 = FundsTests.create_fund(user1, fund_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_, fund1)

        self.assertEqual(genre1.user.id, genre_['user'].id)
        self.assertEqual(genre1.code, genre_['code'])
        self.assertEqual(genre1.name, genre_['name'])
        self.assertEqual(genre1.fund.id, genre_['fund'].id)

    def test_update(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_)

        genre_ = self.samples['genres'][0][1]
        genre_['user'] = user1
        fund_ = self.samples['funds'][0][0]
        fund1 = FundsTests.create_fund(user1, fund_)
        genre_['fund'] = fund1

        genre2 = genre1.update(**genre_)

        self.assertEqual(genre1, genre2)

    def test_delete(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_)

        genre1.delete()  # Built-in method

        self.assertEqual(genre1.pk, None)

    def test_str_representation(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_)

        self.assertEqual(str(genre1), genre_['name'])


class GenreModelValidationOnCreateTests(GenreModelTests):

    def test_required_errors(self):
        errors = ''
        genre_ = self.samples['genres'][0][0]
        genre_.pop('user', None)
        genre_.pop('code', None)
        genre_.pop('name', None)
        genre_.pop('fund', None)

        try:
            Genre.objects.create(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())
        self.assertNotIn('fund', errors.keys())

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        genre_ = self.samples['genres'][0][0]
        genre_['user'] = None
        genre_['code'] = '        '
        genre_['name'] = '        '
        genre_['fund'] = None

        try:
            Genre.objects.create(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())
        self.assertNotIn('fund', errors.keys())

    def test_unique_errors(self):
        errors = ''
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        fund_ = self.samples['funds'][0][0]
        fund1 = FundsTests.create_fund(user1, fund_)
        genre_ = self.samples['genres'][0][0]
        self.create_genre(user1, genre_, fund1)

        try:
            self.create_genre(user1, genre_, fund1)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_same_values_to_other_users(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_)

        user_ = self.samples['users'][1]
        user2 = get_user_model().objects.create_user(**user_)
        genre2 = self.create_genre(user2, genre_)

        self.assertNotEqual(genre1.user, genre2.user)
        self.assertEqual(genre1.code, genre2.code)
        self.assertEqual(genre1.name, genre2.name)


class GenreModelValidationOnUpdateTests(GenreModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        fund_ = self.samples['funds'][0][0]
        fund1 = FundsTests.create_fund(user1, fund_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_, fund1)
        genre_['user'] = None
        genre_['code'] = '        '
        genre_['name'] = '        '
        genre_['fund'] = None

        try:
            genre1.update(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('user', errors.keys())
        self.assertIn('code', errors.keys())
        self.assertIn('name', errors.keys())
        self.assertNotIn('fund', errors.keys())

    def test_unique_errors(self):
        errors = ''
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        fund_ = self.samples['funds'][0][0]
        fund1 = FundsTests.create_fund(user1, fund_)
        genre_ = self.samples['genres'][0][0]
        self.create_genre(user1, genre_, fund1)
        genre_ = self.samples['genres'][0][1]
        genre2 = self.create_genre(user1, genre_, fund1)
        genre_ = self.samples['genres'][0][0]

        try:
            genre2.update(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    def test_same_values_to_other_users(self):
        user_ = self.samples['users'][0]
        user1 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][0]
        genre1 = self.create_genre(user1, genre_)
        user_ = self.samples['users'][1]
        user2 = get_user_model().objects.create_user(**user_)
        genre_ = self.samples['genres'][0][1]
        genre2 = self.create_genre(user2, genre_)
        genre_.pop('user', None)

        genre1.update(**genre_)

        self.assertNotEqual(genre1.user, genre2.user)
        self.assertEqual(genre1.code, genre2.code)
        self.assertEqual(genre1.name, genre2.name)
