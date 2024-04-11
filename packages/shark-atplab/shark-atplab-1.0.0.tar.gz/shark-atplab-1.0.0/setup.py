import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def extract_requirements(req_file_path: str) -> list[str]:
    """
    Read requirements file and return list of requirements
    """
    req_lst: list[str] = []

    with open(req_file_path, "rt") as req_file:
        for line in req_file:
            req = re.sub(r"\s+", "", line, flags=re.UNICODE)
            req = req.split("#")[0]  # skip comment

            if len(req):  # skip empty line
                req_lst.append(req)
    return req_lst


with open(os.path.join(here, 'shark_atplab/VERSION')) as fv:
    version = fv.read().strip()

setup(
    name="shark-atplab",
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=extract_requirements('requirements.txt'),
    version=version,
    author="Willis Chow <chow@mpi-cbg.de>, Soumyadeep Ghosh <soumyadeep11194@gmail.com>, "
           "Agnes Toth-Petroczy <tothpet@mpi-cbg.de>, Maxim Scheremetjew <schereme@mpi-cbg.de>",
    author_email="chow@mpi-cbg.de",
    description="SHARK-Dive (Similarity/Homology Assessment by Relating K-mers)",
    url="https://www.biorxiv.org/content/10.1101/2023.06.26.546490v1",
    download_url="https://git.mpi-cbg.de/tothpetroczylab/shark",
    keywords=["Homology Detection", "Disordered Proteins", "Condensates"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    package_data={'shark_atplab': ['VERSION', '../data/*', '../requirements.txt']},
)
