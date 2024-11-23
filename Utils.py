import subprocess
from typing import Pattern

from Server import Server


# 実行しているユーザーから別のユーザーにファイルをコピーする
def copy_file(src, dest, dest_server: Server):
    try:
        subprocess.run(
            ["scp", src, f"{dest_server.user}@{dest_server.host}:{dest}"],
            check=True,
            input=f"{dest_server.password}\n",
        )
        return True
    except subprocess.CalledProcessError as e:
        print("Error: ", e)
        return False

def remove_files(pattern: Pattern, dest_server: Server):
    try:
        # files = subprocess.run(
        #     ["expect", "-c", f"""
        #     spawn ssh {dest_server.user}@{dest_server.host} "ls {dest_server.path}"
        #     expect \\\"password:\\\"
        #     send \\\"{dest_server.password}\\n\\\"
        #     interact
        #     """],
        #     stdout=subprocess.PIPE,
        #     text=True
        # ).stdout.split("\n")
        #
        # removable_files = [f for f in files if pattern.match(f)]
        # subprocess.run(
        #     ["expect", "-c", f"""
        #     spawn ssh {dest_server.user}@{dest_server.host} "rm {' '.join(removable_files)}"
        #     expect \\\"password:\\\"
        #     send \\\"{dest_server.password}\\n\\\"
        #     interact
        #     """],
        # )

        files = subprocess.run(
            ["ssh", f"{dest_server.user}@{dest_server.host}", f"ls {dest_server.path}"],
            stdout=subprocess.PIPE,
            text=True,
            input=f"{dest_server.password}\n",
            check=True
        ).stdout.split("\n")

        removable_files = [f for f in files if pattern.match(f)]

        subprocess.run(
            ["ssh", f"{dest_server.user}@{dest_server.host}", f"rm {' '.join(removable_files)}"],
            input=f"{dest_server.password}\n",
            text=True,
            check=True
        )


        return True
    except subprocess.CalledProcessError as e:
        print("Error: ", e)
        return False