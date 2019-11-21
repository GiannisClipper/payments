from unittest import skip  # noqa: F401
from django.core.exceptions import ValidationError

from funds.models import Fund
from genres.models import Genre

from genres.tests import GenresTests


class GenreModelTests(GenresTests):
    pass


class GenreModelBasicTests(GenreModelTests):

    def test_model_structure(self):
        fields = [x.name for x in Genre._meta.get_fields()]

        self.assertTrue('user' in fields)
        self.assertTrue('code' in fields)
        self.assertTrue('name' in fields)
        self.assertTrue('is_incoming' in fields)
        self.assertTrue('fund' in fields)

    def test_create(self):
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)

        self.assertEqual(genre1.user.id, genre_['user']['id'])
        self.assertEqual(genre1.code, genre_['code'])
        self.assertEqual(genre1.name, genre_['name'])
        self.assertEqual(genre1.fund.id, genre_['fund']['id'])

    def test_update(self):
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)
        genre_ = self.samples['genres'][12]
        genre_.pop('user', None)
        genre_['fund'] = Fund.objects.get(pk=2)
        genre2 = genre1.update(**genre_)

        self.assertEqual(genre2, genre1)
        self.assertEqual(genre2.code, genre_['code'])
        self.assertEqual(genre2.name, genre_['name'])
        self.assertEqual(genre2.fund.id, genre_['fund'].id)

    def test_delete(self):
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)

        genre1.delete()  # Built-in method

        self.assertEqual(genre1.pk, None)

    def test_str_representation(self):
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)

        self.assertEqual(str(genre1), genre_['name'])


class GenreModelValidationOnCreateTests(GenreModelTests):

    def test_required_errors(self):
        errors = ''
        genre_ = self.samples['genres'][11]
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
        genre_ = self.samples['genres'][11]
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
        genre_ = self.samples['genres'][11]
        self.create_genre(**genre_)

        try:
            self.create_genre(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    # def test_invalid_fund_error(self):
    #     errors = ''
    #     genre_ = self.samples['genres'][11]
    #     genre_['fund']['id'] = self.samples['funds'][21]['id']

    #     try:
    #         self.create_genre(**genre_)
    #     except ValidationError as err:
    #         errors = dict(err)

    #     self.assertIn('fund', errors)

    def test_same_values_to_other_users(self):
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)

        genre_ = self.samples['genres'][21]
        genre_['code'] = genre1.code
        genre_['name'] = genre1.name
        genre2 = self.create_genre(**genre_)

        self.assertNotEqual(genre1.user, genre2.user)
        self.assertEqual(genre1.code, genre2.code)
        self.assertEqual(genre1.name, genre2.name)


class GenreModelValidationOnUpdateTests(GenreModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        genre_ = self.samples['genres'][11]
        genre1 = self.create_genre(**genre_)
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
        genre_ = self.samples['genres'][11]
        self.create_genre(**genre_)
        genre_ = self.samples['genres'][12]
        genre2 = self.create_genre(**genre_)
        genre_ = self.samples['genres'][11]
        genre_.pop('user', None)
        genre_.pop('fund', None)

        try:
            genre2.update(**genre_)
        except ValidationError as err:
            errors = dict(err)

        self.assertIn('__all__', errors)
        self.assertEqual(2, len(errors['__all__']))

    # def test_invalid_fund_error(self):
    #     errors = ''
    #     genre_ = self.samples['genres'][11]
    #     genre1 = self.create_genre(**genre_)
    #     genre_ = self.samples['genres'][21]
    #     genre2 = self.create_genre(**genre_)
    #     genre_.pop('user', None)
    #     genre_['fund'] = genre1.fund

    #     try:
    #         genre2.update(**genre_)
    #     except ValidationError as err:
    #         errors = dict(err)

    #     self.assertIn('fund', errors)
