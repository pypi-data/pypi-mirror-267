from setuptools import setup, find_packages

setup(
    name='PokemonLibrary',
    version='1.0.3',
    author='Martha Morales',
    author_email='martha_morales@live.com.mx',
    description='Una biblioteca que contiene la clase RandomPokemon',
    packages=find_packages(),
    package_data={'PokemonLibrary': ['pokemon.csv']},
    install_requires=[
        'pandas',  # Asegúrate de agregar cualquier dependencia aquí
    ],
)

