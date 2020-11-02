import setuptools
import foxtrot_api

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    dependencies = file.read().split('\n')[:-1]

setuptools.setup(
    name=foxtrot_api.APP_NAME,
    version=foxtrot_api.APP_VERSION,
    author=foxtrot_api.APP_AUTHOR,
    license=foxtrot_api.APP_LICENSE,
    description=foxtrot_api.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=foxtrot_api.APP_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    install_requires=dependencies,
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            '{} = foxtrot_api.__main__:main'.format(foxtrot_api.APP_NAME),
        ]
    }
)
