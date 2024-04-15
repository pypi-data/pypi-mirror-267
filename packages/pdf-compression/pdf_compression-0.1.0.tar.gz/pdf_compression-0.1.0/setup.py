from setuptools import find_packages, setup

setup(
    name='pdf_compression',
    package_dir = {"": "pdf_compression"},
    packages=find_packages(where="pdf_compression"),
    version='0.1.0',
    description='A PDF compression library',
    long_description="A PDF compression library built upon PyMuPDF and Pillow. Quick, free of cost and open source.",
    author='Nishtha',
    author_email = 'nishthachitalia0309@gmail.com',
    license='MIT',
    install_requires=['pillow', 'pymupdf'],
    keywords=['python', 'pdf', 'compression', 'pdf_compression'],
    tests_require=['pytest'],
    test_suite='tests',
)