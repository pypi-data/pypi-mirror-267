import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = "dataos-cookiecutter"
package_version = "0.0.5"
description = "Dataos cookiecutter python Package"

setuptools.setup(
    name="dataos-cookiecutter",
    version=package_version,
    author="devendrasr",
    author_email="devendra@tmdc.io",
    description="Dataos Cookiecutter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rubik_/dataos-cookiecutter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'lens2 = lens2.lens2:main'
        ]
    },
    package_data={'lens2': ['lens/resources/*']},
    python_requires='>=3.7',
    install_requires=[
        'requests==2.25.1',
        'python-dotenv==1.0.1',
        'PyYAML==6.0.1',
        'psycopg2-binary==2.9.9',
        'sql_metadata==2.10.0'
    ],
)
