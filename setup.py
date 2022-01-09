import setuptools

setuptools.setup(
    name="c-elegans-wiring",
    version="0.0.1",
    url="https://github.com/adrameshiu/c_elegans_wiring",
    author="Aditya Ramesh",
    author_email="adramesh@iu.edu",
    description="tools to analyze and filter the worm wiring diagram of C Elegans",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'openpyxl', 'matplotlib', 'networkx', 'pydot'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={'': ['data/*.csv', 'data/*.xlsx']}
)
