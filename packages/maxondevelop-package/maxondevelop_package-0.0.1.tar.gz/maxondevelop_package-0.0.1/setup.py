import pathlib

import setuptools

setuptools.setup(
	name="maxondevelop-package",
	version="0.0.1",
	description="Bref description",
	long_description=pathlib.Path("README.md").read_text(),
	long_description_content_type="text/markdown",
	url="http://maxondevelop-package.com",
	author="Maxondevelop",
	author_email="timetotime828@gmail.com",
	license="MIT",
	project_urls={
		"Documentation": "http://docs.com",
		"Source": "http://github.com",
	},
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"Topic :: Utilities",
	],
	python_requires=">=3.10,<=3.12",
	install_requires=["requests", "pandas>=2.0"],
	extras_require={
		"excel": ["openpyxl"],
	},
	packages=setuptools.find_packages(),
	include_package_data=True,
	entry_points={"console_script": ["maxondevelop_package = maxondevelop_package.cli:main"]},
)