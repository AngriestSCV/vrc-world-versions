#!python

import argparse
import json
import subprocess
import os


def update(world: str, blueprint_id: int):
    os.makedirs(f"worlds/{world}", exist_ok=True)

    with open(f"worlds/{world}/data.json", "r") as f:
        try:
            data = json.load(f)
        except:
            data = {}
            pass

    with open(f"worlds/{world}/data.json", "w") as f:
        data["current"] = blueprint_id
        f.truncate()
        json.dump(data, f)

    subprocess.run(["git", "stash", "-u"], check=True)
    subprocess.run(["git", "pull"], check=True)
    subprocess.run(["git", "add", f"worlds/{world}/data.json"], check=True)
    subprocess.run(["git", "commit", "-m", f"Update {world} to use blueprint {blueprint_id}", "--author=script <bot@AngryLabs.com>"], check=True)
    subprocess.run(["git", "push"], check=True)
    subprocess.run(["git", "stash", "pop"], check=True)

if __name__ == "__main__":
    desc = "This is inteneded to update the json for a world in this repo so that the vrchat world can determine if it is out of date"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("world", help="The name of the world to update")
    parser.add_argument("blueprintId", help="The id of the blueprint being uploaded")

    args = parser.parse_args()

    update(args.world, args.blueprintId)
