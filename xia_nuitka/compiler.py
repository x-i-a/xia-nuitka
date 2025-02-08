import sys
import logging
import os
import subprocess
import platform


class Compiler:
    @classmethod
    def get_python_tag(cls):
        return f"{sys.version}"

    @classmethod
    def exec_cmd(cls, command: str):
        logging.info(command)
        print(command)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = process.communicate()
        process.wait()
        logging.info(stdout)
        print(stdout)
        logging.info(stderr)
        print(stderr)

    @classmethod
    def build_package(cls, root_path: str, package_name: str):
        python_tag = "cp310"
        plat_name = "macosx_11_0_x86_64"
        with os.chdir(package_name):
            build_cmd = " ".join(["python3 setup.py bdist_wheel ",
                                  f"--python-tag {python_tag}",
                                  f"--plat-name {plat_name}",
                                  "clean --all"])
            print(build_cmd)

    @classmethod
    def compile_package(cls, root_path: str, package_name: str, mode: str):
        for abs_path, package_path, module_names in os.walk(os.path.join(root_path, package_name)):
            module_path = abs_path[len(os.path.join(root_path, package_name)):]
            for module_name in module_names:
                if module_name == "__init__.py":
                    pass
                elif module_name.endswith(".py"):
                    cls.compile_module(root_path, package_name, module_path, module_name, mode=mode)

    @classmethod
    def compile_module(cls, root_path: str, package_name: str, module_path: str, module_name: str, mode: str):
        assert(module_name.endswith(".py"))
        compile_cmd = " ".join(["python3 -m nuitka --module --no-pyi-file --remove-output --nofollow-imports",
                                "--output-dir=" + os.path.join(root_path, package_name + module_path),
                                os.path.join(root_path, package_name + module_path, module_name)])
        cls.exec_cmd(compile_cmd)
        clean_cmd = " ".join(["del" if mode.startswith("win") else "rm",
                              os.path.join(root_path, package_name + module_path, module_name)])
        cls.exec_cmd(clean_cmd)


if __name__ == '__main__':
    os_info = platform.uname()
    print(f"System: {os_info.system}")
    print(f"Node Name: {os_info.node}")
    print(f"Release: {os_info.release}")
    print(f"Version: {os_info.version}")
    print(f"Machine: {os_info.machine}")
    print(f"Processor: {os_info.processor}")
    print(f"Python Version: {sys.version}")
    print(f"Compiling path:{sys.argv[1]} package:{sys.argv[2]} mode: {sys.argv[3]}")
    Compiler.compile_package(sys.argv[1], sys.argv[2], sys.argv[3])
    Compiler.build_package(sys.argv[1], sys.argv[2])
