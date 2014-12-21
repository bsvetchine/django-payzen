"""Setup file for easy installation"""
import os
import re

from setuptools import setup, find_packages

from tests import test_cmd


ROOT = os.path.dirname(__file__)
PIP_REQUIRES = os.path.join(ROOT, "requirements.txt")


def parse_requirements(*filenames):
    requirements = []
    for f in filenames:
        for line in open(f, 'r').read().split('\n'):
            # Comment lines. Skip.
            if re.match(r'(\s*#)|(\s*$)', line):
                continue
            # Editable matches. Put the egg name into our reqs list.
            if re.match(r'\s*-e\s+', line):
                pkg = re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line)
                requirements.append("%s" % pkg)
            # File-based installs not supported/needed. Skip.
            elif re.match(r'\s*-f\s+', line):
                pass
            else:
                requirements.append(line)
    return requirements


setup(
    name="django-payzen",
    version="1.0",
    description="Django app to manage payments with Payzen ETP",
    license='MIT',
    author="Bertrand Svetchine",
    author_email="bertrand.svetchine@gmail.com",
    url="https://github.com/bsvetchine/django-payzen",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements(PIP_REQUIRES),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Framework :: Django",
        "Topic :: Software Development"],
    cmdclass={'test': test_cmd.TestCommand}
)
