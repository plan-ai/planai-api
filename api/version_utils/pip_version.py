import requests
from packaging.requirements import Requirement
from packaging.version import parse as parse_version


def get_sub_dependencies(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch data for {package_name}")
        return None

    data = response.json()
    dependencies = data["info"]["requires_dist"]

    if dependencies is None:
        print(f"No dependencies found for {package_name}")
        return None

    dependency_dict = {}
    for dep in dependencies:
        if "extra" not in dep:  # Ignoring extra requirements
            requirement = Requirement(dep)
            specifier = requirement.specifier

            if specifier:
                # Calculate min and max version from specifier
                min_version = None
                max_version = None

                for spec in specifier:
                    op, ver = spec.operator, spec.version
                    if op in [">=", ">"]:
                        current_min_version = parse_version(ver)
                        if min_version is None or current_min_version > min_version:
                            min_version = current_min_version
                    elif op in ["<=", "<"]:
                        current_max_version = parse_version(ver)
                        if max_version is None or current_max_version < max_version:
                            max_version = current_max_version

                min_version = str(min_version) if min_version is not None else None
                max_version = str(max_version) if max_version is not None else None
                dependency_dict[requirement.name] = [min_version, max_version]

    return dependency_dict
