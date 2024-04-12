from setuptools import setup, find_packages

setup(
    name="mucstpy",
    version="1.0.3",
    author="Yu Wang",
    author_email="qq352542417@gmail.com",
    description="The initial package of MuCST",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xkmaxidian/MuCST",
    packages=find_packages(),
    install_requires=[
        "scanpy>=1.9.3",
        "numpy",
        "pandas",
        "anndata",
        "matplotlib",
        "scipy",
        "scikit-learn",
        "psutil",
        "tqdm",
        "leidenalg",
        "torch>=2.0",
        "torchvision"
    ],
    dependency_links=[
        'git+https://github.com/bbchond/torch-toolbox.git#egg=torchtoolbox'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)
