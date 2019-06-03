import setuptools

setuptools.setup(
    name="smart-detective-api",
    version="0.0.1",
    author="Hitesh Wadekar",
    author_email="hitesh.wadekar@gmail.com",

    description="A microservice for Smart detective witness api",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=[],
    entry_points={
        'console_scripts':
            ['smart-detective-api = detective_api.api.detective_api_rpc:serve']
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
