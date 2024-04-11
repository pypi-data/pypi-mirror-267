from setuptools import setup, find_packages

#Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="ezirion_api",
	version="0.1.2",
	packages=find_packages(),
	install_requires=[],
	author="Adrián García",
	description="Biblioteca de mis cursos (Prueba para mi primera api)",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://miurlinventada.com"
)
