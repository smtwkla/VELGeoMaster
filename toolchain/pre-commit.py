#!/usr/bin/env python

import os
import re


# File where the version is stored
version_file = 'VERSION'

# Semantic versioning regex pattern (major.minor.patch)
semver_pattern = r'^(\d+)\.(\d+)\.(\d+)$'

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

def read_version():
    """Reads the current version from the VERSION file."""
    if not os.path.exists(version_file):
        raise FileNotFoundError(f"{version_file} file not found.")
    
    with open(version_file, 'r') as f:
        version = f.read().strip()
    
    return version

def write_version(new_version):
    """Writes the new version to the VERSION file."""
    with open(version_file, 'w') as f:
        f.write(new_version + '\n')

def main():
    # Read the current version
    current_version = read_version()
    print(f"Current version: {current_version}")

    # Increment the version (minor or patch based on commit message)
    new_version = increment_version(current_version, increment_minor=False)
    
    print(f"New version: {new_version}")

    # Write the new version back to the VERSION file
    write_version(new_version)
    os.system("git add VERSION")
    print(f"Version updated to {new_version} in {version_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)