#!python

import argparse
import json
import subprocess
import os

def shell_out(args, check):
    print("Running: " + ' '.join(args))
    subprocess.run(args, check=check)

    print("-------------")
    print()

def update(world: str, blueprint_id: int):
    data_path = f"worlds/{world}/data.json"

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except:
        data = {}


    shell_out(["git", "stash", "-u"], True)
    try:
        shell_out(["git", "reset", "--hard"], True)
        shell_out(["git", "pull"], True)

        os.makedirs(f"worlds/{world}", exist_ok=True)
        if data.get("current", None) == blueprint_id:
            print("Nothing to do")
            return

        with open(f"worlds/{world}/data.json", "w+") as ff:
            data["current"] = blueprint_id
            ff.truncate()
            json.dump(data, ff)
            print("Saved new data")

        shell_out(["git", "add", data_path], True)
        shell_out(["git", "commit", "-m", f"Update {world} to use blueprint {blueprint_id}", "--author=script <bot@AngryLabs.com>"], True)
        shell_out(["git", "push"], True)
    except Exception as ex:
        print("Error updating", ex)
        pass
    shell_out(["git", "reset", "--hard"], False)
    shell_out(["git", "stash", "pop"], False)

if __name__ == "__main__":
    desc = "This is inteneded to update the json for a world in this repo so that the vrchat world can determine if it is out of date"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("world", help="The name of the world to update")
    parser.add_argument("blueprintId", help="The id of the blueprint being uploaded")

    args = parser.parse_args()

    update(args.world, args.blueprintId)
