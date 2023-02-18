import os
import shutil
from typing import Any

from datadir import DataDirectory


class TestDataDirectory:

    basedir = 'test_basedir'
    not_existing_dir = 'not_existing_dir'

    def setup_method(self, method: Any) -> None:
        os.makedirs(TestDataDirectory.basedir, exist_ok=False)

    def teardown_method(self, method: Any) -> None:
        shutil.rmtree(TestDataDirectory.basedir)
        if os.path.exists(TestDataDirectory.not_existing_dir):
            shutil.rmtree(TestDataDirectory.not_existing_dir)

    def test_create_basedir_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.not_existing_dir)

        assert os.path.isdir(TestDataDirectory.not_existing_dir)

    def test_create_basedir_if_exists(self) -> None:
        try:
            data_dir = DataDirectory(TestDataDirectory.basedir)
        except FileExistsError:
            assert False, 'create_basedir() should not raise FileExistsError'

    def test_create_subdir_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)

        subdir = TestDataDirectory.not_existing_dir
        data_dir.create_subdir(subdir)

        assert os.path.isdir(os.path.join(TestDataDirectory.basedir, subdir))

    def test_create_subdir_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'existing_subdir'

        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))

        try:
            data_dir.create_subdir(subdir)
        except FileExistsError:
            assert False, 'create_subdir() should not raise FileExistsError'

    def test_subdir_exists_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = TestDataDirectory.not_existing_dir

        assert data_dir.subdir_exists(subdir) is False

    def test_subdir_exists_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'existing_subdir'

        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))

        assert data_dir.subdir_exists(subdir) is True
