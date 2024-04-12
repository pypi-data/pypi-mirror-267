from setuptools import setup


setup(
    name='brynq_toolkit_successfactors',
    version='0.1.0',
    description='SuccessFactors wrapper from BrynQ',
    long_description='SuccessFactors wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_toolkit.successfactors"],
    license='BrynQ License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'pandas>=2.2.0,<3.0.0',
    ],
    zip_safe=False,
)