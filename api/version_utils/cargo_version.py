import requests
import semver


def parse_version_spec(version_spec):
    try:
        if version_spec.startswith("="):
            # When version is specified with equality, set min and max version as the specified version
            version = semver.VersionInfo.parse(version_spec[1:])
            return str(version), str(version)
        elif version_spec.startswith("^"):
            # Handle single digit version like ^1
            parts = version_spec[1:].split(".")
            if len(parts) == 1 and parts[0].isdigit():
                min_version = semver.VersionInfo.parse(parts[0] + ".0.0")
                max_version = min_version.bump_major()
                return str(min_version), str(max_version)
            else:
                min_version = semver.VersionInfo.parse(version_spec[1:])
                max_version = min_version.bump_major()
                return str(min_version), str(max_version)
        elif version_spec.startswith("~"):
            min_version = semver.VersionInfo.parse(version_spec[1:])
            max_version = min_version.bump_minor()
            return str(min_version), str(max_version)
        elif version_spec == "*":
            return "0.0.0", None  # No upper bound
        else:
            version = semver.VersionInfo.parse(version_spec)
            return str(version), str(version.bump_patch())
    except ValueError as e:
        print(f"Could not parse version spec: {version_spec}, Error: {e}")
        return None, None


def get_crate_dependencies(crate_name):
    url = f"https://crates.io/api/v1/crates/{crate_name}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch data for {crate_name}")
        return None

    data = response.json()
    versions = data.get("versions", None)

    if not versions:
        print(f"No versions found for {crate_name}")
        return None

    # Sort versions by "created_at" to get the latest version
    latest_version = sorted(versions, key=lambda x: x["created_at"], reverse=True)[0]
    latest_version_num = latest_version["num"]

    dep_url = f"https://crates.io/api/v1/crates/{crate_name}/{latest_version_num}/dependencies"
    dep_response = requests.get(dep_url)

    if dep_response.status_code != 200:
        print(
            f"Failed to fetch dependencies for {crate_name} version {latest_version_num}"
        )
        return None

    dep_data = dep_response.json()

    dependencies = dep_data.get("dependencies", [])

    if not dependencies:
        print(
            f"No dependencies found for {crate_name} version {latest_version_num}. It might be a standalone package."
        )
        return {}

    dependency_dict = {}
    for dep in dependencies:
        version_spec = dep.get("req")
        if version_spec:
            min_version, max_version = parse_version_spec(version_spec)
            if min_version is not None:
                dependency_dict[dep["crate_id"]] = [min_version, max_version]

    return dependency_dict
