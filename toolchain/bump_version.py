#!/usr/bin/env python

import os
import re

version_file = init_file = semver_pattern = None


def set_app(app):
    global version_file, init_file, semver_pattern
    # File where the version is stored
    version_file = r'../VERSION'
    init_file = rf'../{app}/__init__.py'

    # Semantic versioning regex pattern (major.minor.patch)
    semver_pattern = r'^(\d+)\.(\d+)\.(\d+)$'

def run_cmd(cmd):
    print(">>> " + cmd)
    os.system(cmd)

def should_increment_minor(commit_message):
    """Checks if 'feat: ' is at the beginning of any line in the commit message."""
    return any(line.startswith("feat: ") for line in commit_message.splitlines())

def increment_version(version, increment_minor=False):
    """Increments the minor or patch part of the semantic version."""
    match = re.match(semver_pattern, version)
    if match:
        major, minor, patch = match.groups()
        if increment_minor:
            # Increment the minor version and reset the patch version
            new_version = f"{major}.{int(minor) + 1}.0"
        else:
            # Increment the patch version
            new_version = f"{major}.{minor}.{int(patch) + 1}"
        return new_version
    else:
        raise ValueError(f"Invalid semantic version: {version}")

def read_version_file():
    """Reads the current version from the VERSION file."""
    if not os.path.exists(version_file):
        raise FileNotFoundError(f"{version_file} file not found.")

    with open(version_file, 'r') as f:
        version = f.read().strip()
        rest = []
        for line in f:
            rest.append(line)

    return version, rest

def write_version_file(new_version, rest):
    """Writes the new version to the VERSION file."""
    with open(version_file, 'w') as f:
        f.write(new_version + '\n')
        for line in rest:
            f.write(line)

def write_version_to_init(new_version, init_file):
    with open(init_file, 'r') as f:
        lines = f.readlines()
        new_version_line = f'__version__ = "{new_version}"\n'
        if lines:
            lines[0] = new_version_line
        else:
            lines.append(new_version_line)
    with open(init_file, 'w') as f:
        f.writelines(lines)

def bump_version():
    current_version, rest_of_file = read_version_file()
    new_version = increment_version(current_version, increment_minor=False)
    write_version_file(new_version, rest_of_file)
    write_version_to_init(new_version, init_file)

    run_cmd(f"git add {version_file}")
    run_cmd(f"git add {init_file}")

    print(f"Version updated to {new_version} in {version_file}")

if __name__ == '__main__':
    try:
        bump_version()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
