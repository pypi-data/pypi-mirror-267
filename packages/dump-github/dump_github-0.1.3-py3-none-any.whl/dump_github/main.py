import argparse
import os
from .lib import *

# Config_MaxSize = 1_000

parser = argparse.ArgumentParser(
    prog="dump_github",
    description="Backup users github repo.",
    epilog="https://github.com/Core2002/dump_github",
)

parser.add_argument("username")
parser.add_argument(
    "-d", "--download_zip", action="store_true", help="only download zip file"
)
parser.add_argument("-p", "--print", action="store_true", help="only print urls")
parser.add_argument("-t", "--token", action="store", default="", help="github token")

args = parser.parse_args()


def clone_repo(repo):
    name = repo["name"]
    url = repo["clone_url"]
    size = repo["size"]
    # if int(size) > Config_MaxSize:
    #     print(f"Keep repo [{name}], Becues size is too Big ({int(size)}).")
    #     return
    print("Clone repo: {}".format(name))
    os.system("git clone {}".format(url))


def download_zip(user_name, reop):
    url = f"https://github.com/{user_name}/{reop['name']}/archive/refs/heads/{reop['default_branch']}.zip"
    print("Downloading repo zip: {}".format(reop["name"]))
    os.system("wget {} -O ./{}_{}.zip".format(url, user_name, reop["name"]))


def main():
    # print(args)
    repos = serach_user_repos(args.username, args.token)
    for repo in repos:
        if args.print == True:
            print(repo["clone_url"])
        elif args.download_zip == True:
            download_zip(args.username, repo)
        else:
            clone_repo(repo)


if __name__ == "__main__":
    main()
