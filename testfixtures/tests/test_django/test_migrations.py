from testfixtures.django import MigrationTestCase


class TestMigrationsTests(MigrationTestCase):

    migrate_from = [('test_django', '0001_initial')]
    migrate_to = [('test_django', '0002_add_foreign_key')]

    def test_simple(self):
        SampleModel = self.old_apps.get_model('test_django', 'SampleModel')
        SampleModel.create(value='foo')

        self.migrate_to_dest()

        SampleModel = self.new_apps.get_model('test_django', 'SampleModel')
        SampleModel.create(value='foo')
