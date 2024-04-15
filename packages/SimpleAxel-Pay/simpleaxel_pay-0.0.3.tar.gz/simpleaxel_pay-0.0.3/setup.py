from setuptools import setup  # type: ignore

__project__ = "SimpleAxel-Pay"
__version__ = "0.0.3"
__description__ = (
    "Pay blueprint for SimpleAxel (https://git.tech.eus/EuskadiTech/SimpleAxel-Pay)"
)
__packages__ = ["pay"]
__url__ = "https://git.tech.eus/EuskadiTech/SimpleAxel-Pay"
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
    include_package_data=True,
    package_data={__packages__[0]: ["templates/*"]},
)
