import sys
import logging
import os
import subprocess
import platform


class Compiler:
    PLATFORM_DICT = {
        ("Linux", "x86_64"): "manylinux1_x86_64",
        ("Linux", "arm64"): "manylinux1_arm64",
        ("Windows", "AMD64"): "win_amd64",
        ("Darwin", "x86_64"): "macosx_11_0_x86_64",
        ("Darwin", "arm64"): "macosx_11_0_arm64",
    }

    @classmethod
    def get_python_tag(cls):
        version, sub_version = sys.version.split(".")[:2]
        return f"cp{version}{sub_version}"

    @classmethod
    def get_platform_name(cls):
        return cls.PLATFORM_DICT.get((platform.uname().system, platform.uname().machine),
                                     (platform.uname().system, platform.uname().machine))

    @classmethod
    def exec_cmd(cls, command: str):
        logging.info(command)
        print(command)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = process.communicate()
        logging.info(stdout)
        print(stdout)
        logging.info(stderr)
        print(stderr)

    @classmethod
    def build_package(cls):
        build_cmd = " ".join(["python3 setup.py bdist_wheel ",
                              f"--python-tag {cls.get_python_tag()}",
                              f"--plat-name {cls.get_platform_name()}",
                              "clean --all"])
        cls.exec_cmd(build_cmd)

    @classmethod
    def compile_package(cls, root_path: str, package_name: str):
        for abs_path, package_path, module_names in os.walk(os.path.join(root_path, package_name)):
            module_path = abs_path[len(os.path.join(root_path, package_name)):]
            for module_name in module_names:
                if module_name == "__init__.py":
                    pass
                elif module_name.endswith(".py"):
                    cls.compile_module(root_path, package_name, module_path, module_name)

    @classmethod
    def compile_module(cls, root_path: str, package_name: str, module_path: str, module_name: str):
        assert(module_name.endswith(".py"))
        compile_cmd = " ".join(["python3 -m nuitka --module --no-pyi-file --disable-ccache",
                                "--remove-output --nofollow-imports",
                                "--output-dir=" + os.path.join(root_path, package_name + module_path),
                                os.path.join(root_path, package_name + module_path, module_name)])
        cls.exec_cmd(compile_cmd)
        clean_cmd = " ".join(["del" if platform.uname().system == "Windows" else "rm",
                              os.path.join(root_path, package_name + module_path, module_name)])
        cls.exec_cmd(clean_cmd)


if __name__ == '__main__':
    print(f"Python Tag: {Compiler.get_python_tag()}")
    print(f"Platform Name: {Compiler.get_platform_name()}")
    print(f"Step: {sys.argv[1]}")
    if sys.argv[1] == "compile":
        print(f"Compiling path:{sys.argv[2]} package:{sys.argv[3]}")
        Compiler.compile_package(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "build":
        print(f"Build package")
        Compiler.build_package()
