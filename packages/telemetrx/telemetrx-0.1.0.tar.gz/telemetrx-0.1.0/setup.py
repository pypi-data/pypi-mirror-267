from setuptools import setup, find_packages

setup(name='telemetrx',
      version='0.1.0',
      packages=find_packages(),
      install_requires=['aiohttp', 'python-dotenv'],
      python_requires='>=3.7',
      description='A package to send telemetry data asynchronously to TelemetrX platform',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Vivek Singh',
      author_email='vivekksi@cisco.com',
      license='Proprietary',
      include_package_data=True,
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'License :: Other/Proprietary License'])