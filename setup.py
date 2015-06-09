"""Setup file for easy installation"""
import os

from setuptools import setup, find_packages

from tests import test_cmd


ROOT = os.path.dirname(__file__)


setup(
    name="django-payzen",
    version="1.0.5",
    description="Django app to manage payments with Payzen ETP",
    license='MIT',
    author="Bertrand Svetchine",
    author_email="bertrand.svetchine@gmail.com",
    url="https://github.com/bsvetchine/django-payzen",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django"],
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
