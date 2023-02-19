import os
import shutil
import pytest
from typing import Any, Dict

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
        _ = DataDirectory(TestDataDirectory.not_existing_dir)

        assert os.path.isdir(TestDataDirectory.not_existing_dir)

    def test_create_basedir_if_exists(self) -> None:
        _ = DataDirectory(TestDataDirectory.basedir)

    def test_create_subdir_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)

        subdir = TestDataDirectory.not_existing_dir
        data_dir.create_subdir(subdir)

        assert os.path.isdir(os.path.join(TestDataDirectory.basedir, subdir))

    def test_create_subdir_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'existing_subdir'

        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))

        data_dir.create_subdir(subdir)

    def test_subdir_exists_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = TestDataDirectory.not_existing_dir

        assert data_dir.subdir_exists(subdir) is False

    def test_subdir_exists_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'existing_subdir'

        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))

        assert data_dir.subdir_exists(subdir) is True

    def test_file_exists_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'not_existing_file'

        assert data_dir.file_exists(file) is False

    def test_file_exists_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'existing_file'

        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write('')

        assert data_dir.file_exists(file) is True

    def test_get_tree_if_empty_basedir(self) -> Dict[str, str]:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        
        tree = data_dir.get_tree()
        
        assert tree == {'subdirs': [], 'files': []}

    def test_get_tree_if_not_empty_basedir(self) -> Dict[str, str]:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'subdir'
        file = 'file'

        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write('')
        with open(os.path.join(TestDataDirectory.basedir, subdir, file), 'w') as f:
            f.write('')

        tree = data_dir.get_tree()
        
        assert tree == {
            'subdirs': ['test_basedir\\subdir'], 
            'files': ['test_basedir\\file', 'test_basedir\\subdir\\file']
        }

    def test_rm_subdir_if_empty(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'subdir'
        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))

        data_dir.rm_subdir(subdir)

        assert os.path.isdir(os.path.join(TestDataDirectory.basedir, subdir)) is False

    def test_rm_subdir_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = TestDataDirectory.not_existing_dir

        with pytest.raises(OSError):
            data_dir.rm_subdir(subdir)

    def test_rm_subdir_if_not_empty(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'subdir'
        file = 'file'
        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))
        with open(os.path.join(TestDataDirectory.basedir, subdir, file), 'w') as f:
            f.write('')

        with pytest.raises(OSError):
            data_dir.rm_subdir(subdir)

    def test_rm_subdir_if_not_empty_and_force(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        subdir = 'subdir'
        file = 'file'
        os.makedirs(os.path.join(TestDataDirectory.basedir, subdir))
        with open(os.path.join(TestDataDirectory.basedir, subdir, file), 'w') as f:
            f.write('')

        data_dir.rm_subdir(subdir, force=True)

        assert os.path.isdir(os.path.join(TestDataDirectory.basedir, subdir)) is False

    def test_rm_file_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'not_existing_file'

        with pytest.raises(OSError):
            data_dir.rm_file(file)

    def test_rm_file_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write('')

        data_dir.rm_file(file)

        assert os.path.isfile(os.path.join(TestDataDirectory.basedir, file)) is False
