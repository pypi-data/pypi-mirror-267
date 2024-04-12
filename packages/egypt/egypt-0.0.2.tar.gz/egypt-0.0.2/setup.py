from setuptools import setup, find_packages

setup(
    name='egypt',
    version='0.0.2',
    description='PyTorch Implementation of Multiscale Decomposition and Pyramid Algorithms',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/your_package',
    author='Charles Shan',
    author_email='charles.shht@gmail.com',
    license='MIT',
    # classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    # ],
    keywords='MST Pyramid Pytorch',
    packages=find_packages(),
    install_requires=['torchvision', 'matplotlib', 'torch'],  # List of dependencies
    python_requires='>=3.6',
)
