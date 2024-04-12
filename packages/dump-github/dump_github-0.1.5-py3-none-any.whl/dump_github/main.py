import argparse
import os
from .lib import *

parser = argparse.ArgumentParser(
    prog="dump-github",
    description="Backup users github repo.",
    epilog="https://github.com/Core2002/dump_github",
)

parser.add_argument("username")
parser.add_argument(
    "-d", "--download_zip", action="store_true", help="only download zip file"
)
parser.add_argument("-p", "--print", action="store_true", help="only print urls")
parser.add_argument("--token", action="store", default="", help="github token")
parser.add_argument(
    "--limit_size",
    type=int,
    default=100,
    help="limit size(MB) of download zip file, if 0 then no limit(default:100).",
)

args = parser.parse_args()


def clone_repo(repo):
    name = repo["name"]
    url = repo["clone_url"]
    size = repo["size"]
    print("Clone repo: {}".format(name))
    os.system("git clone {}".format(url))


def download_zip(user_name, reop):
    url = f"https://github.com/{user_name}/{reop['name']}/archive/refs/heads/{reop['default_branch']}.zip"
    max_size = args.limit_size * 1000 * 1000
    cmd = (
        "curl --retry 3 --retry-delay 3 -L --max-filesize {} {} -o ./{}_{}.zip".format(
            max_size, url, user_name, reop["name"]
        )
    )
    print(f"Download {reop['name']} : {url}")
    os.system(cmd)


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
