import os

from datadir import DataDirectory


class TestDataDirectory:

    basedir = 'test_basedir'
    not_existing_dir = 'not_existing_dir'

    def setup_method(self, method):
        os.makedirs(TestDataDirectory.basedir, exist_ok=False)

    def teardown_method(self, method):
        os.rmdir(TestDataDirectory.basedir)
        if os.path.exists(TestDataDirectory.not_existing_dir):
            os.rmdir(TestDataDirectory.not_existing_dir)

    def test_create_basedir_if_not_exists(self):
        data_dir = DataDirectory(TestDataDirectory.not_existing_dir)

        assert os.path.isdir(TestDataDirectory.not_existing_dir)

    def test_create_basedir_if_exists(self):
        try:
            data_dir = DataDirectory(TestDataDirectory.basedir)
        except FileExistsError:
            assert False, 'create_basedir() should not raise FileExistsError'

    def test_create_subdir_if_not_exists(self):
        data_dir = DataDirectory(TestDataDirectory.basedir)

        subdir = TestDataDirectory.not_existing_dir
        data_dir.create_subdir(subdir)

        assert os.path.isdir(os.path.join(TestDataDirectory.basedir, subdir))
