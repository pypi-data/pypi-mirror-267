from setuptools import setup
from batch_integrated_gradients import BatchIntegratedGradients

setup(
    name='batch_integrated_gradients',
    version=BatchIntegratedGradients.__version__,
    description='Batch Integrated Gradients is a simple method for explaining temporal data predictions.',
    long_description='The Batch Integrated Gradients method is provides a simple method for explaining temporal data predictions. This provides details on both the gradients and integrated gradients that can be visualised.',
    url='https://github.com/jamie-duell/batch_integrated_gradients',
    author='Jamie Duell',
    author_email='853435@swansea.ac.uk',
    packages=['batch_integrated_gradients'],
    install_requires=['numpy', 'scipy', 'torch', 'matplotlib'],
)