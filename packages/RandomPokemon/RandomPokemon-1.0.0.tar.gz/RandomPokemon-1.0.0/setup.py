from setuptools import setup, find_packages

setup(
    name='RandomPokemon',
    version='1.0.0',
    author='Martha Morales',
    author_email='tu@email.com',
    description='Una biblioteca que contiene la clase RandomPokemon',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Asegúrate de agregar cualquier dependencia aquí
    ],
)
