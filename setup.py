from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='traveltimepy',
      version='1.0.0',
      description='Python Interface to Travel Time',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/traveltime-dev/traveltime-python-sdk',
      author='TravelTime',
      license='MIT',
      packages=['traveltimepy'],
      keywords=['traveltime', 'api', 'maps'],
      install_requires=[
          'requests', 'certifi >= 2021.5.30'
      ]
    )
