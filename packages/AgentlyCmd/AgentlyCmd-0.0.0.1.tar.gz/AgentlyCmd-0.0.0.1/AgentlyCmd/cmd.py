import sys
import subprocess

class Commands(object):
    @staticmethod
    def create(args:list):
        print(f"\033[91m\033[47m\033[3m\033[1m Agent\033[34mly\033[30m.Tech \033[0m Project Creator")
        project_name = "agently_project"
        if len(args) >= 1:
            project_name = "_".join(args)
        else:
            print("No project name is given. Use 'agently_project' by default.")
        print(f"Creating project '{ project_name }'...")
        subprocess.run(["git", "clone", "https://gitee.com/maplemx/agently-ws.git", project_name])
        print("Done. Happy coding!")
        return

def main():
    command_name = ""
    args = []
    if len(sys.argv) == 1:
        command_name = "create"
    if len(sys.argv) > 2:
        args = sys.argv[2:]
    if hasattr(Commands, command_name):
        getattr(Commands, command_name)(args)
    else:
        print(f"No such command: '{ command_name }'!")

if __name__ == "__main__":
    main()