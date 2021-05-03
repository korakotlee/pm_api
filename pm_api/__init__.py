"""
__init__.py
"""

__author__ = 'korakotlee'

# import sys
import os
import argparse
from pathlib import Path
from pm_api import api

__version__ = "0.1.2"

def cli():
    parser = argparse.ArgumentParser(description='Printed Mint API')
    parser.add_argument('directory')
    args = parser.parse_args()

    path = args.directory
    if os.path.isdir(path):
        # api.make_sample_file(path)
        api.run(path)
    else:
        print("\nSorry, the directory does not exist\n")

if __name__ == "__main__":
    cli()
