import re

import setuptools

with open("src/mockee/__meta__.py", encoding="utf8") as f:
    version = re.search(r'version = ([\'"])(.*?)\1', f.read()).group(2)

setuptools.setup(
    name='mockee',
    version=version
)
