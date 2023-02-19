import os
import shutil
import logging
import pandas as pd
from typing import Any, Dict, List, Literal

LOGGER = logging.getLogger(__name__)

class DataDirectory:

    def __init__(self, basedir_path: str, exist_ok: bool = True) -> None:
        self.basedir_path = basedir_path
        self.create_basedir(exist_ok=exist_ok)

    def create_basedir(self, exist_ok: bool = True) -> None:
        os.makedirs(self.basedir_path, exist_ok=exist_ok)

    def create_subdir(self, subdir_path: str, exist_ok: bool = True) -> None:
        subdir_path = os.path.join(self.basedir_path, subdir_path)
        os.makedirs(subdir_path, exist_ok=exist_ok)

    def subdir_exists(self, subdir_path: str) -> bool:
        subdir_path = os.path.join(self.basedir_path, subdir_path)
        return os.path.isdir(subdir_path)

    def file_exists(self, file_path: str) -> bool:
        file_path = os.path.join(self.basedir_path, file_path)
        return os.path.isfile(file_path)

    def get_tree(self) -> Dict[str, str]:
        all_subdirs, all_files = list(), list()
        for root, dirs, files in os.walk(self.basedir_path):
            for name in files:
                all_files.append(os.path.join(root, name))
            for name in dirs:
                all_subdirs.append(os.path.join(root, name))
        return {'subdirs': all_subdirs, 'files': all_files}

    def rm_subdir(self, subdir_path: str, force: bool = False) -> None:
        subdir_path = os.path.join(self.basedir_path, subdir_path)
        if force:
            shutil.rmtree(subdir_path)
        else:
            os.rmdir(subdir_path)

    def rm_file(self, file_path: str) -> None:
        file_path = os.path.join(self.basedir_path, file_path)
        os.remove(file_path)

    def get_text_file(self, file_path: str) -> str:
        file_path = os.path.join(self.basedir_path, file_path)
        with open(file_path, 'r') as f:
            return f.read().splitlines()

    def save_text_file(self, file_path: str, content: str | List[str], mode: Literal['w', 'a'] = 'w') -> None:
        if mode not in ('w', 'a'):
            raise ValueError('Invalid mode, should be either "w" or "a"')

        file_path = os.path.join(self.basedir_path, file_path)
        with open(file_path, mode) as f:
            if type(content) is str:
                f.write(content)
            else:
                f.writelines(content)

    def save_df(self, file_path: str, df: pd.DataFrame, **kwargs: Any) -> None:
        file_path = os.path.join(self.basedir_path, file_path)
        file_ext = os.path.splitext(file_path)[1]
        if file_ext in ('.csv', '.txt'):
            df.to_csv(file_path, **kwargs)
        elif file_ext == '.xlsx':
            df.to_excel(file_path, **kwargs)
        elif file_ext == '.parquet':
            df.to_parquet(file_path, **kwargs)
        elif file_ext == '':
            LOGGER.warning('Empty file extension, saving as csv')
            df.to_csv(file_path + '.csv', **kwargs)
        else:
            raise ValueError(
                f'Unknown file extension: "{file_ext}", should be one of: ".csv", ".txt", ".xlsx", ".parquet"'
            )
