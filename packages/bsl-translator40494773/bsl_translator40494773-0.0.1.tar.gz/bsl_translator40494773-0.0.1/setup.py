from setuptools import setup, find_packages

setup(
    name="bsl_translator40494773",
    version="0.0.1",
    packages=find_packages(),
    package_dir={},
    description="Open source library to translate BSL signs into text",
    author="Miguel Garcia",
    email="miguelgarher01@gmail.com",
    install_requires=[
        "opencv-python~=4.9.0.80",
        "numpy",
        "mediapipe",
        "tensorflow~=2.15.0.post1",
        "keras~=2.15.0",
        "scikit-learn~=1.4.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
