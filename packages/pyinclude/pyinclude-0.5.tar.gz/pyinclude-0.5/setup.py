from setuptools import setup, find_packages

requirements=[
	"inflect",
	"wxpython"
	]
setup(
	name="pyinclude",
	version="0.5",
	packages=find_packages(),
	install_requires=requirements,
	author="Harry Min Khant",
	author_email="harrymk64@gmail.com",
	description="A collection of python codes to be easy as possible",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/harrymkt/pyinclude",
	classifiers=[
		"Programming Language :: Python :: 3",
		# Add more classifiers as needed
	],
)