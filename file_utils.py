import os

def flip_filename(filepath: str, new_name: str = None) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    dir_name, base_name = os.path.split(filepath)
    if new_name:
        new_base = new_name
    else:
        if base_name.startswith("_"):
            new_base = base_name.lstrip("_")
        else:
            new_base = f"_{base_name}"
    new_path = os.path.join(dir_name, new_base)
    os.rename(filepath, new_path)
    return new_path
