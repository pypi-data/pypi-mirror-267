from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="starlight_toolkit",
    version="0.1.0",
    description="A set of tools to manage the Starlight spectral synthesis code.",
    # long_description=long_description,
    url="https://github.com/arielwrl/starlight_toolkit",
    author="Ariel Werle",
    author_email="ariel.werle@inaf.it",
    package_dir={"": "starlight_toolkit"},
    packages=find_packages(where="starlight_toolkit"),
    python_requires=">=3, <4",
    install_requires=[], 
    include_package_data=True
)