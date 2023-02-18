import os


class DataDirectory:

    def __init__(self, basedir_path: str) -> None:
        self.basedir_path = basedir_path
        self.create_basedir(exist_ok=True)

    def create_basedir(self, exist_ok: bool = False) -> None:
        os.makedirs(self.basedir_path, exist_ok=exist_ok)

    def create_subdir(self, subdir_path: str, exist_ok: bool = True) -> None:
        subdir_path = os.path.join(self.basedir_path, subdir_path)
        os.makedirs(subdir_path, exist_ok=exist_ok)
