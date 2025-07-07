import sys
from importlib.metadata import version
from typing import Any

import pandas as pd


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_package_version(package_name: str) -> str:
    return version(package_name)


def flatten_json(json_info, prefix = ''):
    """
    Recursively flattens an arbitrary structured JSON object.
    Returns a list of flat dicts, each suitable as a row in DataFrame.
    :param prefix:
    :type prefix:
    :type json_info: a JSON structure of unknown schema.
    """
    out = []

    if isinstance(json_info, dict):
        # Dict: flatten each value
        res = [{}]
        for k, v in json_info.items():
            sub = flatten_json(v, prefix + k + '.')
            new_res = []
            for item in res:
                for sub_item in sub:
                    merged = {**item, **sub_item}
                    new_res.append(merged)
            res = new_res
        out.extend(res)

    elif isinstance(json_info, list):
        # List: repeat for each element
        res = []
        for i, item in enumerate(json_info):
            sub = flatten_json(item, prefix)
            res.extend(sub)
        out.extend(res)

    else:
        # Leaf value
        out.append({prefix[:-1]: json_info})

    return out


def main():
    data = {
        "user": {"name": "Alice", "email": "alice@example.com"},
        "orders": [
            {"id": 101, "amount": 99.99},
            {"id": 102, "amount": 45.50}
        ]
    }

    flattened_data = flatten_json(data)
    df = pd.DataFrame(flattened_data)
    print(df)

    export_index = True
    if export_index:
        df.index.name = 'Sequence'

    # NOTE: by default, to_csv and to_excel overwrite any preexisting file with the same name
    df.to_csv("customer-orders.csv", index = export_index)
    df.to_excel("customer-orders.xlsx", index = export_index)


def get_required_package_names() -> list[str]:
    packages: list[str] = []
    with open('requirements.txt') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # skip blank lines and comments
            package = line.split('~')[0].strip()  # works for ~=, >=, ==, etc.
            packages.append(package)

    packages.sort()
    return packages


if __name__ == '__main__':
    print(f"Python version: {get_python_version()}")
    
    package_names = get_required_package_names()
    
    for pkg in package_names:
        package_name = f'{pkg}'.ljust(12)
        print(f'{package_name}{get_package_version(pkg)}')

    main()
