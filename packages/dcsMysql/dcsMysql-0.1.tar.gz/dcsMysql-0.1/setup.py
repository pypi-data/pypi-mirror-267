from setuptools import setup, find_packages

setup(
    name='dcsMysql',  
    version='0.1',  
    author='azhen',
    author_email='xxiang0803@gmail.co,',
    description='mysql',
    url='https://github.com/xiaoxiangXX/dcsMysql', 
    packages=find_packages(),
    install_requires=['pymysql'],
    entry_points={
        'console_scripts': [
            'dcs_mysql=dcsMysql:job',
        ],
    },
)
