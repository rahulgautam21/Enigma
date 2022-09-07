from setuptools import setup, find_packages

setup(
    name='SE Project',
    version='1.0',
    description='Created project for Software Engineering Course',
    author='HomeWork Grp 40(Shreya, Srilekha, Sarika, Chetana, Rahul, Shubham)',
    author_email='cchetan2@ncsu.edu',
    zip_safe=False,
    classifiers=(
        'Development Status :: Development',
        'Intended Audience :: Engineers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ),
    tests_require=['pytest'],
    exclude_package_data={'': ['.gitignore'],
                            'images': ['*.xcf', '*.blend']},
)
