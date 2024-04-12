from setuptools import setup, find_packages

setup(
    name="space_avenger",
    version="0.1.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'space_avenger=space_avenger.main:main',
        ],
    },
    package_data={
        'space_avenger': ['assets/*.*'],  # Assuming assets are directly in the assets folder
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
