from flask import make_response, jsonify
from version_utils.cargo_version import get_crate_dependencies
from version_utils.npm_version import get_npm_sub_dependencies
from version_utils.pip_version import get_python_sub_dependencies
from version_utils.yarn_version import get_yarn_sub_dependencies
from authentication import validate_user


def version_to_float(version):
    if version is None:
        return None

    try:
        version_parts = version.split(".")
        major_version = float(version_parts[0])
        minor_version = "".join(version_parts[1:])
        if not minor_version:  # Handle case when there's no minor version part
            return major_version

        decimal_part = float(f".{minor_version}")
        return major_version + decimal_part
    except ValueError:
        print(f"Could not convert '{version}' to float.")
        return None


def get_lang_specific_dependency(lang: str, dependency: str):
    if lang == "rust":
        return get_crate_dependencies(dependency)
    elif lang == "npm":
        return get_npm_sub_dependencies(dependency)
    elif lang == "python3":
        return get_python_sub_dependencies(dependency)
    elif lang == "yarn":
        return get_yarn_sub_dependencies(dependency)
    else:
        raise Exception(
            "Only 4 package managers supported at the time: pip,cargo,yarn, and npm"
        )


def valid_version(version_no, min_version, max_version):
    result = True
    version_no = version_to_float(version_no)
    min_version = version_to_float(min_version)
    max_version = version_to_float(max_version)
    if min_version is not None and version_no < min_version:
        result = False
    if max_version is not None and version_no > max_version:
        result = False
    return result


def get_version_issues(jwt_auth: str, lang: str, used_dependencies: dict):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        dependencies = {}
        results = {}
        for dependency in used_dependencies.keys():
            try:
                dependencies.update(get_lang_specific_dependency(lang, dependency))
            except Exception as err:
                print(repr(err))
                pass
        for dependency in dependencies.keys():
            if dependency in used_dependencies:
                if not valid_version(
                    used_dependencies[dependency],
                    dependencies[dependency][0],
                    dependencies[dependency][1],
                ):
                    results[dependency] = dependencies[dependency]
        message = results
        status_code = 200
    except Exception as err:
        message = {"message": "Could not fetch dependencies", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)
