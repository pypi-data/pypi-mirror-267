from setuptools import setup  # type: ignore

__project__ = "SimpleAxel-Auth"
__version__ = "0.0.2"
__description__ = (
    "Auth blueprint for SimpleAxel (https://git.tech.eus/EuskadiTech/Simple-Auth)"
)
__packages__ = ["auth"]
__url__ = "https://git.tech.eus/EuskadiTech/Simple-Auth"
__author__ = "EuskadiTech"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
]
__requires__ = ["requests", "Flask", "stripe", "SimpleSDK"]

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    url=__url__,
    author=__author__,
    classifiers=__classifiers__,
    requires=__requires__,
)
