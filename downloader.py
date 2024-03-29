from os import path, makedirs
from json import load
from shutil import copyfileobj
from urllib3 import PoolManager

c = PoolManager()

version_manifest_v2_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
experimental_versions_url = "https://maven.fabricmc.net/net/minecraft/experimental_versions.json"

with c.request("GET", version_manifest_v2_url, preload_content=False) as res, open("version_manifest_v2.json", "wb") as out_file:
    print("downloading version_manifest_v2.json from mojang")
    copyfileobj(res, out_file)

with c.request("GET", experimental_versions_url, preload_content=False) as res, open("experimental_versions.json", "wb") as out_file:
    print("downloading experimental_versions.json from fabric")
    copyfileobj(res, out_file)

with open("version_manifest_v2.json", "rt") as file:
    manifest_v2 = load(file)

with open("experimental_versions.json", "rt") as file:
    experimental_versions = load(file)

if not path.exists("./versions/"):
    makedirs("./versions")

all_versions = manifest_v2["versions"] + experimental_versions["versions"]

for version in all_versions:
    version_id = version["id"]
    directory = f"./versions/{version_id}"
    filepath = f"{directory}/{version_id}.json"
    url = version["url"]

    if not path.exists(directory):
        makedirs(directory)

    if not path.isfile(filepath):
        with c.request("GET", url, preload_content=False) as res, open(filepath, "wb") as out_file:
            print(f"downloading {version_id}.json")
            copyfileobj(res, out_file)

    with open(filepath, "rt") as file:
        version_meta = load(file)

        if "client_mappings" in version_meta["downloads"]:
            client = version_meta["downloads"]["client"]
            client_mappings = version_meta["downloads"]["client_mappings"]
            client_filename = f"{directory}/{version_id}-client"

            if not path.isfile(client_filename + ".jar"):
                with c.request("GET", client["url"], preload_content=False) as res, open(client_filename + ".jar", "wb") as out_file:
                    print(f"downloading {version_id}-client.jar")
                    copyfileobj(res, out_file)

            if not path.isfile(client_filename + ".txt"):
                with c.request("GET", client_mappings["url"], preload_content=False) as res, open(client_filename + ".txt", "wb") as out_file:
                    print(f"downloading {version_id}-client.txt")
                    copyfileobj(res, out_file)
