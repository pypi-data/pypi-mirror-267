"imports"
import setuptools
# Each Python project should have pyproject.toml or setup.py
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including the current pre-release)
# as we have moved away from needing to generate a setup.py file to enable editable installs
# - We might be able to delete this file soon
setuptools.setup(
    name='person-local',
    version='0.0.50',  # https://pypi.org/project/person-local/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles person Local Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles-zone/person-local-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
    install_requires=["shapely>=2.0.2",
                      "language-remote>=0.0.17",]
)
