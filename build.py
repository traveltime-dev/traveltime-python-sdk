import os

from setuptools.command.install import install
from setuptools.command.sdist import sdist


class CustomBuild(install):
    def run(self):
        super().run()
        print('Proto files generation started')
        generate_proto()
        print('Proto files generation is done')


class CustomSdistCommand(sdist):
    def run(self):
        super().run()
        print('Proto files generation started')
        generate_proto()
        print('Proto files generation is done')


def generate_proto():
    os.system('protoc -I=./proto --python_out=./ ./proto/*')