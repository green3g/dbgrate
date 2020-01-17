from setuptools import setup, find_packages

setup(
    name='dbgrate',
    author='roemhildtg',
    version='0.13',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'mako',
        'sqlalchemy'
    ],
    entry_points='''
        [console_scripts]
        dbgrate=dbgrate.main:cli
    '''
)