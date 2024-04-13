from setuptools import setup, find_packages

setup(
    name='doSql',
    version='0.1',
    author='Ramzan Kadyrov',
    author_email='ramzan095@gmail.com',
    description='Подключение к БД',
    long_description='Легко подключайся к БД',
    long_description_content_type='text/markdown',
    url='https://github.com/saiyan05122004',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
