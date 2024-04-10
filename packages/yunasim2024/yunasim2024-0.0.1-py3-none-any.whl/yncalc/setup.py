import setuptools

setuptools.setup(
    include_package_data = True,
    name = 'yunasim2024',
    version='0.0.1',
    description = 'nice calculator',
    author = 'simrok',
    autho_email = 'ynna3784@gmail.com',
    url = 'https://github.com/simrok/calc0001',
    download_url = 'https://github.com/simrok/calc0001',
    install_requires=['pytest'],
    long_description = 'oss-dev calculator python module',
    long_description_content_type = 'text/markdown',
    packages = ['yncalc'],
    classifiers = [
     'Programming Language :: Python :: 3',
     'Programming Language :: Python :: 3.10',
     # 기타 등등...
]
)
