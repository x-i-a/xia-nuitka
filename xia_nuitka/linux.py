import sys
import logging
import os
import subprocess


class Compiler:
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
    def compile_package(cls, root_path: str, package_name: str, mode: str = "winux"):
        for abs_path, package_path, module_names in os.walk(os.path.join(root_path, package_name)):
            module_path = abs_path[len(os.path.join(root_path, package_name)):]
            for module_name in module_names:
                if module_name == "__init__.py":
                    pass
                elif module_name.endswith(".py"):
                    cls.compile_module(root_path, package_name, module_path, module_name, mode=mode)

    @classmethod
    def compile_module(cls, root_path: str, package_name: str, module_path: str, module_name: str, mode: str = "winux"):
        assert(module_name.endswith(".py"))
        if mode in ["linux", "winux"]:
            linux_compile = " ".join(["python3 -m nuitka --module --no-pyi-file --remove-output --nofollow-imports",
                                      "--output-dir=" + os.path.join(root_path, package_name + module_path),
                                      os.path.join(root_path, package_name + module_path, module_name)])
            cls.exec_cmd(linux_compile)

if __name__ == '__main__':
    compile_mode = "linux"
    print(f"Compiling path:{sys.argv[1]} package:{sys.argv[2]} mode: {compile_mode}")
    Compiler.compile_package(sys.argv[1], sys.argv[2], compile_mode)