from typing import Any
from datetime import datetime
from plistlib import dumps

from os import mkdir, chmod, rename, makedirs
from os.path import exists

from shutil import rmtree, copytree, move

from subprocess import run

from utils import read, write

def build_mac(temp_path: str, datapath: str) -> None:
  runtime_path: str = f"{temp_path}/runtimes"
  d_service_path: str = f"{temp_path}/desktop-service"
  version: str = read(f"{d_service_path}/version") or "v0"

  timestamp: float = float(version.strip("v"))
  tdt: datetime = datetime.fromtimestamp(timestamp)
  version: str = tdt.strftime("%Y.%m.%d.%H%M%S")
  short_version: str = tdt.strftime("%Y.%m.%d")

  build_path: str = f"{datapath}/build"
  assets_path: str = f"{d_service_path}/assets"

  runtime_name: str = "py313-mac"
  runtime_path = f"{runtime_path}/{runtime_name}"

  if exists(build_path):
    rmtree(build_path)
  
  if exists(f"{datapath}/GraphScript.app"):
    rmtree(f"{datapath}/GraphScript.app")

  makedirs(build_path)

  copytree(d_service_path, f"{build_path}/desktop-service")
  copytree(runtime_path, f"{build_path}/runtime")
  copytree(assets_path, f"{build_path}/Resources")

  info: dict[str, Any] = {
    "CFBundleName": "GraphScript",
    "CFBundleDisplayName": "GraphScript",
    "CFBundleIdentifier": "dev.graphscript.dservice",
    "CFBundleVersion": version,
    "CFBundleShortVersionString": short_version,
    "CFBundlePackageType": "APPL",
    "CFBundleIconFile": "GraphScript.icns",
    "CFBundleExecutable": "launcher",
    "CFBundleURLTypes": [
      {
        "CFBundleURLName": "GraphScript URL",
        "CFBundleURLSchemes": ["graphscript"]
      }
    ]
  }

  write(
    f"{build_path}/Info.plist",
    dumps(info).decode('utf-8')
  )

  launcher_code: list[str] = [
    """#!/bin/bash""",
    """DIR="$(cd "$(dirname "$0")" && pwd)\"""",
    """RUNTIME_DIR="$DIR/../runtime\"""",
    """SOURCE_DIR="$DIR/../desktop-service/src\"""",
    """export PYTHONPATH="$RUNTIME_DIR/packages\"""",
    """$RUNTIME_DIR/bin/python3 "$SOURCE_DIR/main.py\" "$@\"""",
  ]

  write(
    f"{build_path}/MacOS/launcher",
    "\n".join(launcher_code)
  )

  write(f"{build_path}/PkgInfo", "APPL????")

  chmod(f"{build_path}/MacOS/launcher", 0o755)
  chmod(f"{build_path}/runtime/bin/python3", 0o755)

  mkdir(f"{datapath}/GraphScript.app")
  rename(build_path, f"{datapath}/GraphScript.app/Contents")

  if exists("/Applications/GraphScript.app"):
    try:
      rmtree("/Applications/GraphScript.app")
    except PermissionError:
      run([
        "sudo", "rm", "-rf", "/Applications/GraphScript.app"
      ])
  
  try:
    move(
      f"{datapath}/GraphScript.app",
      "/Applications/GraphScript.app"
    )
  except PermissionError:
    run([
      "sudo", "mv", f"{datapath}/GraphScript.app",
      "/Applications/GraphScript.app"
    ])

