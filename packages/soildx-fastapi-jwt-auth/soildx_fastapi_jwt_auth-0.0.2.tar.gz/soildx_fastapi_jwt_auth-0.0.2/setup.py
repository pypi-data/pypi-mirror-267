from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='soildx_fastapi_jwt_auth',
    version="0.0.2",
    author="Akash",
    description="fastapi-jwt-auth simple jwt token authentication",
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.110.1',
        'python-jose[cryptography]',
        'passlib[bcrypt]'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)