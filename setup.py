from setuptools import find_packages, setup

package_name = 'aws-ssm-cli-invoke'

setup(name=package_name,
      version='0.0.1',
      packages=find_packages(),
      install_requires=[],

      entry_points={
            'console_scripts': [
                  'aws-ssm-invoke=ssm.main:main',
            ],
      },

      )
