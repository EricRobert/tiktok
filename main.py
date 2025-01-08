import json
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from subprocess import run
from time import sleep


def extract_links(dump):
    links = defaultdict(list)

    for item in dump["Activity"]["Favorite Videos"]["FavoriteVideoList"]:
        links["favorites"].append(item["Link"])

    for item in dump["Activity"]["Like List"]["ItemFavoriteList"]:
        links["liked"].append(item["link"])

    for item in dump["Activity"]["Share History"]["ShareHistoryList"]:
        if item["SharedContent"] != "share_video":
            continue
        links["shared"].append(item["Link"])

    return links


def sync(path, args):
    links = extract_links(json.loads(path.read_text()))
    for name, urls in links.items():
        d = Path("mp4", name)
        for url in urls:
            id = url.removesuffix("/").split("/")[-1]
            assert len(id) == 19
            dst = Path(d, f"{id}.mp4")
            if dst.exists():
                continue
            cmd = f"yt-dlp --write-info-json -o '%(id)s.%(ext)s' -P tmp {url}"
            run(cmd, shell=True)
            tmp = Path(args.workspace, f"{id}.mp4")
            if tmp.exists():
                d.mkdir(parents=True, exist_ok=True)
                tmp.with_suffix(".info.json").rename(dst.with_suffix(".info.json"))
                tmp.rename(dst)
            sleep(args.sleep)


def main():
    p = ArgumentParser()
    p.add_argument("files", nargs="*", default=["user_data_tiktok.json"])
    p.add_argument("--sleep", default=5)
    p.add_argument("--workspace", default="./tmp")

    args = p.parse_args()

    for file in args.files:
        sync(Path(file), args)


if __name__ == "__main__":
    main()
