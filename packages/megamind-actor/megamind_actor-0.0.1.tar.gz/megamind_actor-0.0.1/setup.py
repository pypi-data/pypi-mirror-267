# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages(".")

package_data = {"": ["*"]}

install_requires = [
    "pydantic",
    "ray",
    "setuptools>=50.0,<51.0",
]

entry_points = {
}

setup_kwargs = {
    "name": "megamind_actor",
    "version": "0.0.1",
    "description": "Megamind Actor",
    "author": "Megamind",
    "author_email": "",
    "maintainer": None,
    "maintainer_email": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.6,<4.0",
}


setup(**setup_kwargs)
