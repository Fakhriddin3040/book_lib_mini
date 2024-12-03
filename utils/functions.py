import os


# Util-functions for working with FileSystem


def mkdirs(path: str, is_file: bool = False):
    if is_file:
        path = os.path.dirname(path)
    os.makedirs(path, exist_ok=True)


def get_filename(file_path: str) -> str:
    return os.path.basename(file_path)
