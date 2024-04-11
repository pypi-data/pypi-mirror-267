import setuptools

setuptools.setup(
    name="pyewelink",
    version="0.2",
    author="xwm",
    author_email="xwmdev@163.com",
    description="ewelink client debug tools",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests >= 2.31.0',
        'websocket-client >= 1.7.0',
        'toml >= 0.10.2',
        'pycryptodome >= 3.20.0',
        'pyserial >= 3.5',
        'pytest >= 8.1.1',
        'simplepyble >= 0.7.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    #scripts=['ewelink/ewelink.py'],
    #data_files=[('', ['ewelink/conf.toml'])],
    entry_points = {
        'console_scripts': [
            'ewelink = ewelink.ewelink:main'
        ]
    }
)
