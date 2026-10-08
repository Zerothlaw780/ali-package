import setuptools

setuptools.setup(
    name="package",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Gamma correction for one or two images",
    url='https://github.com/novavision-ai/package',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        'novavision.package',
        'novavision.package.executors',
        'novavision.package.models',
        'novavision.package.utils',
    ],
    package_dir={'novavision.package': 'src'},
    python_requires=">=3.6"
)