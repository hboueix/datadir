import os
import shutil
import pytest
import pandas as pd
import pickle as pkl
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

    def test_str(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)

        assert str(data_dir) == TestDataDirectory.basedir

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

    def test_get_text_file_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'not_existing_file'

        with pytest.raises(OSError):
            data_dir.get_text_file(file)

    def test_get_text_file_if_exists_and_empty(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write('')

        text = data_dir.get_text_file(file)

        assert text == []

    def test_get_text_file_if_existsand_not_empty(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write('test\nmultilines')

        text = data_dir.get_text_file(file)

        assert text == ['test', 'multilines']

    def test_save_text_file_if_str_content(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        text = 'test\nmultilines'

        data_dir.save_text_file(file, text)

        with open(os.path.join(TestDataDirectory.basedir, file), 'r') as f:
            assert f.read() == text

    def test_save_text_file_if_list_content(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        text = ['test\n', 'multilines']

        data_dir.save_text_file(file, text)

        with open(os.path.join(TestDataDirectory.basedir, file), 'r') as f:
            assert f.read().splitlines(keepends=True) == text

    def test_save_text_file_if_str_content_and_append_mode(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        text = 'test\nmultilines'
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.write(text)

        data_dir.save_text_file(file, text, mode='a')

        with open(os.path.join(TestDataDirectory.basedir, file), 'r') as f:
            assert f.read() == text + text

    def test_save_text_file_if_list_content_and_append_mode(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        text = ['test\n', 'multilines\n']
        with open(os.path.join(TestDataDirectory.basedir, file), 'w') as f:
            f.writelines(text)

        data_dir.save_text_file(file, text, mode='a')

        with open(os.path.join(TestDataDirectory.basedir, file), 'r') as f:
            assert f.read().splitlines(keepends=True) == text + text

    def test_save_text_file_if_invalid_mode(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        text = 'test\nmultilines'

        with pytest.raises(ValueError):
            data_dir.save_text_file(file, text, mode='invalid_mode')

    def test_get_df_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'not_existing_file'

        with pytest.raises(OSError):
            data_dir.get_df(file)

    def test_get_df_if_csv_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.csv'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df.to_csv(os.path.join(TestDataDirectory.basedir, file), index=False)

        df2 = data_dir.get_df(file)

        assert df.equals(df2)

    def test_get_df_if_txt_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.txt'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df.to_csv(os.path.join(TestDataDirectory.basedir, file), index=False)

        df2 = data_dir.get_df(file)

        assert df.equals(df2)

    def test_get_df_if_excel_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.xlsx'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df.to_excel(os.path.join(TestDataDirectory.basedir, file), index=False)

        df2 = data_dir.get_df(file)

        assert df.equals(df2)

    def test_get_df_if_parquet_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.parquet'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df.to_parquet(os.path.join(TestDataDirectory.basedir, file), index=False)

        df2 = data_dir.get_df(file)

        assert df.equals(df2)

    def test_get_df_if_invalid_path_extension(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.invalid'

        with pytest.raises(ValueError):
            data_dir.get_df(file)

    def test_get_df_if_no_extension_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df.to_csv(os.path.join(TestDataDirectory.basedir, file), index=False)

        df2 = data_dir.get_df(file)

        assert df.equals(df2)

    def test_save_df_if_csv_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.csv'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        data_dir.save_df(file, df, index=False)

        df2 = pd.read_csv(os.path.join(TestDataDirectory.basedir, file))
        assert df.equals(df2)

    def test_save_df_if_txt_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.txt'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        data_dir.save_df(file, df, index=False)

        df2 = pd.read_csv(os.path.join(TestDataDirectory.basedir, file))
        assert df.equals(df2)

    def test_save_df_if_excel_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.xlsx'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        data_dir.save_df(file, df, index=False)

        df2 = pd.read_excel(os.path.join(TestDataDirectory.basedir, file))
        assert df.equals(df2)

    def test_save_df_if_parquet_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.parquet'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        data_dir.save_df(file, df, index=False)

        df2 = pd.read_parquet(os.path.join(TestDataDirectory.basedir, file))
        assert df.equals(df2)

    def test_save_df_if_invalid_path_extension(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.invalid'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        with pytest.raises(ValueError):
            data_dir.save_df(file, df, index=False)

    def test_save_df_if_no_extension_path(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file'
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        data_dir.save_df(file, df, index=False)

        df2 = pd.read_csv(os.path.join(TestDataDirectory.basedir, file+'.csv'))
        assert df.equals(df2)

    def test_get_obj_if_not_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'not_existing_file'

        with pytest.raises(OSError):
            data_dir.get_obj(file)

    def test_get_obj_if_exists(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'file.pkl'
        obj = {'a': 1, 'b': 2}
        with open(os.path.join(TestDataDirectory.basedir, file), 'wb') as f:
            pkl.dump(obj, f)

        obj2 = data_dir.get_obj(file)

        assert obj == obj2

    def test_save_obj_if_invalid_obj(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'invalid_obj.pkl'
        obj = {'a': 1, 'b': 2}.keys()

        with pytest.raises(TypeError):
            data_dir.save_obj(file, obj)

    def test_save_obj_if_valid_obj(self) -> None:
        data_dir = DataDirectory(TestDataDirectory.basedir)
        file = 'valid_obj.pkl'
        obj = {'a': 1, 'b': 2}

        data_dir.save_obj(file, obj)

        with open(os.path.join(TestDataDirectory.basedir, file), 'rb') as f:
            obj2 = pkl.load(f)

        assert obj == obj2
