"""
PM_API
"""

import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name='pm_api',
    packages=['pm_api'],  # this must be the same as the name above
    version='0.1',
    description='Printed Mint API call',
    # long_description_content_type="text/markdown",
    long_description=README,
    author='Korakot Leemakdej',
    author_email='kleemakdej@gmail.com',
    url='https://printedmint.com',
    keywords=['api'],
    install_requires=['pyyaml'],
    license="Commercial",
    package_data={'': ['*.css']},
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        'console_scripts': [
            'pm-api = pm_api:cli'
        ]},
)
