from setuptools import setup, find_packages

setup(
    name                = 'all_utils',
    version             = '0.1',
    description         = 'util function for experiments',
    author              = 'Jaesik Yoon',
    author_email        = 'jaesik.yoon.kr@gmail.com',
    url                 = 'https://github.com/jsikyoon/my_ubuntu_settings',
    install_requires    =  [],
    packages            = find_packages(exclude = []),
    keywords            = ['utilization'],
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
)
