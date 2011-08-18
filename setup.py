from setuptools import setup, find_packages

setup(
    name = 'python-sendgrid',
    version = '0.1',
    url = 'http://github.com/tsharju/python-sendgrid',
    license = 'BSD',
    description = 'Library for SendGrid REST API.',
    author = 'Teemu Harju',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'requests'],
)
