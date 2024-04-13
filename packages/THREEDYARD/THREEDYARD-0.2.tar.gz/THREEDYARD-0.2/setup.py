from setuptools import setup, find_packages

setup(
    name='THREEDYARD',
    version='0.2',
    packages=find_packages(),
    description='A 3D modeling mini library',
    author='Muhammad Ammar Jamshed',
    author_email='ammar.jamshed@aidatayard.com',
    url="https://github.com/AmmarJamshed",
    install_requires=[
        'numpy','pandas','matplotlib'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)