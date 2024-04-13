import sys
import setuptools
import subprocess

with open('./Agently/requirements.txt') as f:
    origin_requirements = f.read().splitlines()

requirements = []
for requirement in origin_requirements:
    if not requirement.startswith("#"):
        requirements.append(requirement)

class CreateCommand(setuptools.Command):
    description = "Create \033[91m\033[47m\033[3m\033[1m Agent\033[34mly\033[30m.Tech \033[0m project dir"
    user_options = [
        ("type=", None, "project type")
    ]

    def initialize_options(self):
        self.type = "ws"

    def finalize_options(self):
        type_options = ["ws"]
        if self.type not in type_options:
            raise ValueError(f"--type options' value must in { type_options }")

    def run(self):
        args = sys.argv[2:]
        project_name = ""
        if len(args) == 0:
            print("Project name is not given, use 'agently_project' as default.")
            project_name = "agently_project"
        else:
            project_name = "_".join(args)

        subprocess.run(["git", "git", "clone", "https://gitee.com/maplemx/agently-ws.git"])
        os.rename("agently-ws", project_name)
        print(f"\033[91m\033[47m\033[3m\033[1m Agent\033[34mly\033[30m.Tech \033[0m Project dir ./{ project_name } is created.")
        return


setuptools.setup(
    name = "Agently",
    version = "3.3.0.0-alpha-0",
    author = "Maplemx",
    author_email = "maplemx@gmail.com",
    description = "Agently, a framework to build applications based on language model powered intelligent agents.",
    long_description = "https://github.com/Maplemx/Agently",
    url = "https://github.com/Maplemx/Agently",
    license='Apache License, Version 2.0',
    packages = ["Agently"],
    #packages = setuptools.find_packages(),
    package_data = {"": ["*.txt", "*.ini"]},
    install_requires= requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass = {
        "create": CreateCommand,
    },
    python_requires=">=3.8",
)
