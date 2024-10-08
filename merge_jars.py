import os
import subprocess
import sys

from util import error

if len(sys.argv) != 2:
    error("Usage: {} <version>".format(sys.argv[0]))

tool_dir = os.path.join(os.path.dirname(__file__), "tools")
os.makedirs(tool_dir, exist_ok=True)

stitch_path = os.path.join(tool_dir, "stitch-0.17.0+local-all.jar")
if not os.path.exists(stitch_path):
    error("stitch not found: get from https://github.com/claiwe/stitch")

version = sys.argv[1]
version_dir = os.path.join("versions", version)
if not os.path.exists(version_dir):
    error("folder {} doesn't exist, have you run the downloader?".format(version_dir))

client_path = os.path.join(version_dir, f"{version}-client.jar")
server_path = os.path.join(version_dir, f"{version}-server.jar")
if not os.path.exists(client_path) or not os.path.exists(server_path):
    error("missing client or server jar, have you run the downloader?")

merged_path = os.path.join(version_dir, f"{version}-merged.jar")
if os.path.exists(merged_path):
    error("{} already exists, quitting".format(merged_path))

process = subprocess.run([
    "java", "-Xmx1G", "-jar",
    os.path.abspath(stitch_path),
    "mergeJar",
    os.path.abspath(client_path),
    os.path.abspath(server_path),
    os.path.abspath(merged_path)
], check=True, capture_output=True, text=True)
print("merged jar saved to {}".format(merged_path))