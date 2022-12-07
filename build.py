import pathlib
import os
from subprocess import check_call
from setuptools.command.install import install


class CustomInstall(install):

    @staticmethod
    def __generate_proto_code():
        print("helo")
        proto_interface_dir = "./proto"
        generated_src_dir = "./traveltimepy/dto/proto/"
        out_folder = "traveltimepy"
        if not os.path.exists(generated_src_dir):
            os.mkdir(generated_src_dir)
        proto_it = pathlib.Path().glob(proto_interface_dir + "/**/*")
        proto_path = "generated=" + proto_interface_dir
        protos = [str(proto) for proto in proto_it if proto.is_file()]
        check_call(["protoc"] + protos + ["--python_out", out_folder, "--proto_path", proto_path])

    def run(self):
        print("Custom install start")
        super().run()
        self.__generate_proto_code()
        print("Custom install done")

