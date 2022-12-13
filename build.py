import os
from setuptools.command.install import install


class CustomBuild(install):

    @staticmethod
    def __generate_proto():
        os.system('protoc -I=./proto --python_out=./ ./proto/*')

    def run(self):
        super().run()
        print('Proto files generation started')
        self.__generate_proto()
        print('Proto files generation is done')
