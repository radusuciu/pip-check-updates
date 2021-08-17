import re

import requests


def get_latest_version(name):
    r = requests.get(f"https://pypi.org/pypi/{name}/json")
    if r.status_code == 200:
        version = r.json()["info"]["version"]
        return version
    return None


def get_current_version(dep):
    name, current_version = [token for token in re.split(r"[><=~!]", dep) if token]
    op = dep[len(name) : -len(current_version)]
    return name, current_version, op


def compare_versions(current_version, latest_version):
    current_versioning = current_version.split(".")
    latest_versioning = latest_version.split(".")

    current_versioning = current_versioning + ["0"] * (3 - len(current_versioning))
    latest_versioning = latest_versioning + ["0"] * (3 - len(latest_versioning))

    if all(
        [
            latest_versioning[:3] == current_versioning[:3],
            len(latest_versioning) == 3,
            len(current_versioning) == 3,
        ]
    ):
        return None

    if latest_versioning[0] != current_versioning[0]:
        return "major"

    if latest_versioning[1] != current_versioning[1]:
        return "minor"

    if latest_versioning[2] != current_versioning[2]:
        return "patch"

    return "other"


def load_dependencies(path="requirements.txt"):
    deps = []
    with open(path) as f:
        for dep in f.read().splitlines():
            dep = dep.strip()
            if dep.startswith("-r"):
                deps.extend(load_dependencies(dep.split()[-1]))
                continue
            try:
                name, current_version, op = get_current_version(dep)
                deps.append([path, name, current_version, op])
            except:
                pass

    return deps