import setuptools
import foxtrot_api as fa

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name=fa.APP_NAME,
    version=fa.APP_VERSION,
    url=fa.APP_URL,
    author=fa.APP_AUTHOR,
    author_email=fa.APP_AUTHOR_EMAIL,
    license=fa.APP_LICENSE,
    description=fa.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    install_requires=[
        "gunicorn",
        "Flask",
        "Flask-RESTful",
        "Flask-Cors"
    ],
    extra_requires={
        "dev": [
            "twine",
            "pytest",
            "sphinx",
            "check-manifest",
            "sphinx-rtd-theme"
        ]
    },
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            '{} = foxtrot_api.__main__:main'.format(fa.APP_NAME),
        ]
    }
)
