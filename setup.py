from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements("requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="pysrc",
    author="Andrea Milazzo, Museo dell'Informatica Funzionante",
    author_email="andreamilazzo@mancausoft.org",
    url="https://github.com/MusIF-MIAI/pysrc",
    version="0.0.1",
    description="Utilities to generate the Segnale orario RAI Codificato (SRC)",
    packages=find_packages(),
    install_requires=reqs)
