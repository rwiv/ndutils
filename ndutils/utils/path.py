import os.path
from pathlib import Path
from typing import Union


def path_join(*paths: Union[str, int, float, Path, None], delimiter: str = "/") -> str:
    cleaned_paths = []
    for i, rp in enumerate(paths):
        if rp is None:
            continue

        if not isinstance(rp, (str, int, float, Path)):
            raise TypeError(f"Invalid path type: {type(rp)}")

        sp = str(rp)
        if not sp:
            continue
        if isinstance(rp, Path):
            sp = sp.replace(os.path.sep, delimiter)

        if i == 0:
            cleaned_paths.append(sp.rstrip(delimiter))
        elif i == len(paths) - 1:
            cleaned_paths.append(sp.lstrip(delimiter))
        else:
            cleaned_paths.append(sp.strip(delimiter))

    return delimiter.join(cleaned_paths)
