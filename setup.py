from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in testcrew/__init__.py
from testcrew import __version__ as version

setup(
	name="testcrew",
	version=version,
	description="testcrew",
	author="rehan",
	author_email="rehan@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
