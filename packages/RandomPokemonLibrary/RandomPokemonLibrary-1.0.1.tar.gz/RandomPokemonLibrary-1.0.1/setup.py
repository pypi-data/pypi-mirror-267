from setuptools import setup, find_packages

setup(
    name='RandomPokemonLibrary',
    version='1.0.1',
    author='Martha Morales',
    author_email='martha_morales@live.com.mx',
    description='Una biblioteca que contiene la clase RandomPokemon',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Asegúrate de agregar cualquier dependencia aquí
    ],
)

