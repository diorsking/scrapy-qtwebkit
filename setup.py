from setuptools import setup


setup(
    name='scrapy-qtwebkit',
    version='0.1',
    description='Qt WebKit for Scrapy',
    author='Artur Gaspar',
    author_email='artur.gaspar.00@gmail.com',
    packages=['scrapy_qtwebkit'],
    install_requires=['Twisted>=15', 'Scrapy>=1.1']
)
