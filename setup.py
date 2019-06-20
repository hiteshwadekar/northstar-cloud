import setuptools

setuptools.setup(
    setup_requires=['pbr>=2.0.0'],
    pbr=True)

'''
setuptools.setup(
    name="northstar_cloud",
    version="0.0.1",
    author="Hitesh Wadekar",
    author_email="hitesh.wadekar@ibm.com",

    description="A microservice for northstar_cloud services.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=[],
    entry_points={
        'console_scripts':
            ['northstar-cloud = northstar_cloud.cli.northstar_cloud_start:serve']
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
'''
