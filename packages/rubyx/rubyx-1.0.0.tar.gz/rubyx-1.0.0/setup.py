import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rubyx",
    version="1.0.0",
    author="@aituglo",
    author_email="contact@aituglo.com",
    description="Rubyx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aituglo/rubyx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['docopt', 'requests'],
    python_requires='>=3.5',
    entry_points = {
        'console_scripts': ['rubyx=src.rubyx:main'],
    }
)
