import os
import sys
import subprocess

class Commands(object):
    @staticmethod
    def help(args:list):
        subprocess.run(["echo", "\033[91m\033[47m\033[3m\033[1m Agent\033[34mly\033[30m.Tech \033[0m"])
        subprocess.run(["echo", "📘 Command List:"])
        subprocess.run(["echo", "--------------"])
        subprocess.run(["echo", "create\t<project_name>\t--type <type_name>\tCreate new Agently project into dir './<project_name>'."])

    @staticmethod
    def create(args:list):
        print(f"\033[91m\033[47m\033[3m\033[1m Agent\033[34mly\033[30m.Tech \033[0m")
        project_name = "agently_project"
        if len(args) >= 1:
            project_name = "_".join(args)
        else:
            print("🟡 No project name is given. Use 'agently_project' by default.")
        print(f"🟢 Creating project '{ project_name }'...")
        if os.path.exists(f"./{ project_name }"):
            print(f"🚫 The directory '{ project_name }' has already exist. Please check or use another project name.")
        else:
            subprocess.run(["git", "clone", "https://gitee.com/maplemx/agently-ws.git", project_name])
            print(f"✅ Project directory '{ project_name }' created. Happy coding!")
        return

def main():
    command_name = ""
    args = []
    if len(sys.argv) == 1:
        command_name = "help"
    else:
        command_name = sys.argv[1]
    if len(sys.argv) > 2:
        args = sys.argv[2:]
    if hasattr(Commands, command_name):
        getattr(Commands, command_name)(args)
    else:
        print(f"No such command: '{ command_name }'!")

if __name__ == "__main__":
    main()