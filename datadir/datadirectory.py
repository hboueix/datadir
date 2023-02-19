import os
import shutil
from typing import Dict, List


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

    def save_text_file(self, file_path: str, content: str | List[str]) -> None:
        file_path = os.path.join(self.basedir_path, file_path)
        with open(file_path, 'w') as f:
            if type(content) is str:
                f.write(content)
            else:
                f.writelines(content)
