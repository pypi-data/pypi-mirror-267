import setuptools

# Descripción larga del proyecto
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Configuración del setup
setuptools.setup(
    name = "RumboVeta1",
    version = "1.1",
    author = "Julio Gomez",
    description = "Con esta Biblioteca Calculas el rumbo de veta",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    package_dir= {"":"src"},
    packages = setuptools.find_packages(where="src"),
    # install_requires = ['math'],
    python_requires = ">=3.12.1" 
)