import setuptools
import os


def read(fname):
    file = open(os.path.join(os.path.dirname(__file__), fname))
    file_data = file.read()
    file.close()

    return file_data

packages = setuptools.find_packages(
    where="src", 
    exclude=['test*','test.*']
)

setuptools.setup(
    name="id_verification_python_requesthelper",
    version="0.0.4",
    author="Sam D Ware",
    author_email="sware@tritelph.com",
    description="A library to interact with the ID Verification Request APIs",
    url="https://github.com/Tritel-ATL/Id.Verification.Python.RequestHelper.git",
    package_dir={"": "src"},
    packages=packages,
    long_description=read('README.md'),
    python_requires='>=3.12',
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Utilities"
    ], install_requires=[ 
        'requests', 
        'logging',
        'multipledispatch',
        'id_verification_python_userhelper'
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=5.0.0"]
    }
)