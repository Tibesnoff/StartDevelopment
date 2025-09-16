import json
from typing import Any

def edit_json_key(file_path: str, dotted_key: str, value: Any) -> bool:
    """
    Updates a nested key in a JSON file by replacing only the line containing
    the final key, preserving original whitespace/formatting.
    """
    try:
        # Verify key exists by walking the parsed JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        keys = dotted_key.split(".")
        d = data
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                print(f"Key path '{dotted_key}' not found.")
                return False
            d = d[k]

        if keys[-1] not in d:
            print(f"Final key '{keys[-1]}' not found in {dotted_key}.")
            return False

        # Replace only the last key in the raw file
        last_key = keys[-1]
        new_value = json.dumps(value)  # ensures proper JSON encoding

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        replaced = False
        for i, line in enumerate(lines):
            if f'"{last_key}"' in line:  # crude but effective for most JSONs
                prefix, _, _ = line.partition(":")
                lines[i] = f'{prefix}: {new_value},\n' if line.strip().endswith(",") else f'{prefix}: {new_value}\n'
                replaced = True
                break

        if not replaced:
            print(f"Line for key '{last_key}' not found in text.")
            return False

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return True

    except Exception as e:
        print(f"Error editing JSON file: {e}")
        return False
