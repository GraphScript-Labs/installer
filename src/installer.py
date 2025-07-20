from shutil import rmtree

from os import makedirs
from os.path import abspath, expanduser, exists

from subprocess import run

from fetcher import pull_source
from configs import generate_configs, write_configs
from buildtools import build_mac

def install(installConfigs: dict[str, str]) -> None:
  internal_dir: str = "__gsds_app_data__"
  config_datapath: str = f"{installConfigs['datapath']}/{internal_dir}"

  datapath: str = abspath(expanduser(config_datapath))
  build_path: str = f"{datapath}/installer"

  if exists(build_path):
    rmtree(build_path)
  
  makedirs(build_path, exist_ok=True)

  pull_source("desktop-service", build_path)
  pull_source("runtimes", build_path)
  configs = generate_configs(datapath)
  
  makedirs(f"{build_path}/desktop-service/configs", exist_ok=True)
  write_configs(configs, f"{build_path}/desktop-service")

  build_mac(build_path, datapath)

  makedirs(f"{datapath}/data", exist_ok=True)
  makedirs(f"{datapath}/temp", exist_ok=True)
  
  run([
    "/Applications/GraphScript.app/Contents/MacOS/launcher",
    "--setup",
  ])

  rmtree(build_path)
  run([
    "open", "/Applications/GraphScript.app",
  ])
