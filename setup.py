# noinspection Mypy
from typing import Any

from setuptools import setup, find_packages
from os import path, getcwd

# from https://packaging.python.org/tutorials/packaging-projects/

# noinspection SpellCheckingInspection
package_name = "helix_fhir_profiles"

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open(path.join(getcwd(), "VERSION")) as version_file:
        version = version_file.read().strip()
except IOError:
    raise


def fix_setuptools() -> None:
    """Work around bugs in setuptools.

    Some versions of setuptools are broken and raise SandboxViolation for normal
    operations in a virtualenv. We therefore disable the sandbox to avoid these
    issues.
    """
    try:
        from setuptools.sandbox import DirectorySandbox

        # noinspection PyUnusedLocal
        def violation(operation: Any, *args: Any, **_: Any) -> None:
            print("SandboxViolation: %s" % (args,))

        DirectorySandbox._violation = violation
    except ImportError:
        pass


# Fix bugs in setuptools.
fix_setuptools()


# classifiers list is here: https://pypi.org/classifiers/

# create the package setup
setup(
    name=package_name,
    version=version,
    author="Abbey",
    author_email="abbey.mcculloch@icanbwell.com",
    description="helix_fhir_profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/icanbwell/helix.fhir.profiles.git",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
    package_data={"helix_fhir_profiles": ["py.typed"]},
)
