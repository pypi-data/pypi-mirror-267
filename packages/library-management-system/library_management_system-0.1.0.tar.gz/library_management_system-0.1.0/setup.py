from setuptools import setup, find_packages

setup(
    name='library_management_system',
    version='0.1.0',
    author='Alexandra Oliveira',
    author_email='m.alexandra.ro@gmail.com',
    description='A simple library management system',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Any dependencies you need, for example:
        # 'requests',
    ],
)
