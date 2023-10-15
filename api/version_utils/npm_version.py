import requests
import semver


def get_npm_sub_dependencies(package_name):
    url = f"https://registry.npmjs.org/{package_name}/latest"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch data for {package_name}")
        return None

    data = response.json()
    dependencies = data.get("dependencies", None)

    if dependencies is None:
        print(f"No dependencies found for {package_name}")
        return None

    dependency_dict = {}
    for dep, version_spec in dependencies.items():
        # Handle the version specification using semver
        min_version = None
        max_version = None

        if version_spec.startswith("^"):
            min_version = semver.VersionInfo.parse(version_spec[1:])
            max_version = min_version.bump_major()
        elif version_spec.startswith("~"):
            min_version = semver.VersionInfo.parse(version_spec[1:])
            max_version = min_version.bump_minor()
        elif version_spec == "*":
            min_version = "0.0.0"
            max_version = None  # No upper bound
        else:
            try:
                min_version = semver.VersionInfo.parse(version_spec)
                max_version = min_version.bump_patch()
            except ValueError:
                print(f"Could not parse version spec: {version_spec}")

        dependency_dict[dep] = [
            str(min_version) if min_version else None,
            str(max_version) if max_version else None,
        ]

    return dependency_dict
