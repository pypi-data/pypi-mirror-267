from setuptools import setup

install_requirements = [
    "scipy",
    "biopython>=1.78",
    "scikit-learn>=0.21.3",
    "pandas>=0.23.3",
    "xgboost==1.2.0",
]

setup(
    name = 'rnamining',
    author = 'Thaís de Almeida Ratis Ramos',
    author_email = 'thaisratis@gmail.com',
    description = 'Package to predict potential coding of RNA sequences provided in fasta format',
    license = 'GPL3',
    include_package_data=True,
    version = '1.0.4',
    packages = ['rnamining'],
    scripts=['bin/rnamining'],
    install_requires=install_requirements
)