import setuptools

setuptools.setup(
    name = "AgentlyCmd",
    version = "0.0.0.1",
    author = "Maplemx",
    author_email = "maplemx@gmail.com",
    description = "Agently Shell Command.",
    long_description = "Agently Shell Command.",
    url = "https://github.com/Maplemx/Agently",
    license='Apache License, Version 2.0',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'Agently = AgentlyCmd.cmd:main'
        ]
    },
    python_requires=">=3.8",
)
