from setuptools import setup

setup(
    name="perm_scope",
    version="1.0.0",
    description="Herramienta de análisis y recolección local para sistemas Windows y Linux",
    author="Cyberius Company",
    author_email="contacto@cyberiuscompany.com",
    license="MIT",
    py_modules=["perm_scope"],
    packages=["ventanas", "ventanas.cli", "ventanas.about", "ventanas.home", "modulos"],
    include_package_data=True,
    install_requires=[
        "PyQt5",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "perm_scope=perm_scope:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
