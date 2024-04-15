from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

with open(os.path.join(root_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

for dirpath, dirnames, filenames in os.walk(os.path.join('src', 'karray')):
    # Ignore dirnames that start with '.'
    if "__init__.py" in filenames:
        pkg = dirpath.replace(os.path.sep, ".")
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, ".")
        packages.append(pkg)

setup(
    name="karray",
    version="2024.3.5",
    python_requires=">=3.8",
    packages=packages,
    author="Carlos Gaete-Morales",
    author_email="cdgaete@gmail.com",
    install_requires=[
        "numpy"
    ],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Lightweight labelled multidimensional arrays with NumPy arrays under the hood.",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
    ],
)
