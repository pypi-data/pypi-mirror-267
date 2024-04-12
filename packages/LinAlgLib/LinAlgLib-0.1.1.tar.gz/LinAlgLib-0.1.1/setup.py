from setuptools import setup, find_packages

setup(
    name='LinAlgLib',
    version='0.1.1',
    author='David_Wasilewski',
    packages=find_packages(),
    py_modules=['functions'],
    install_requires=[
        'numpy',
        'sympy'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DWasilewski3/LinAlgLib',
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)