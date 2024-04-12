from setuptools import setup
import re
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with open('statalanjy/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

if not version:
    raise RuntimeError("Version mech mawjoude !")

setup(
    name="statalanjy",
    author="Kristen Kamouh",
    url="https://github.com/kristenkamouh/stats.git",
    version=version,
    packages=[''],
    license='MIT',
    description="Khallik bl Parc (iykyk)",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[],
    python_requires='>=3.5.3',
    include_package_data=True,
    keywords=['parc', 'AK', 'khallik-bl-parc']
)
