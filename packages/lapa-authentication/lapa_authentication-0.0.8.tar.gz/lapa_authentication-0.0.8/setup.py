from setuptools import find_packages, setup

package_name = "lapa_authentication"

setup(
    name=package_name,
    version="0.0.8",
    packages=find_packages(),
    package_data={
        package_name: ["data/*"],
    },
    install_requires=[
        "uvicorn>=0.24.0.post1",
        "fastapi>=0.104.1",
        "square_logger~=1.0",
        "pydantic>=2.5.3",
        "lapa_commons>=0.0.1",
        "bcrypt>=4.1.2",
        "pyjwt>=2.8.0"
    ],
    extras_require={},
    author="Lav Sharma, thePmSquare",
    author_email="lavsharma2016@gmail.com, thepmsquare@gmail.com",
    description="authentication service for my personal server.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/lavvsharma/{package_name}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
