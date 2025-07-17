from utils import write

def generate_configs(datapath: str) -> dict[str, str]:
  return {
    "datapath": datapath,
    "service_url": "https://raw.githubusercontent.com/GraphScript-Labs",
    "org_url": "https://github.com/GraphScript-Labs",
    "repos": "\n".join([
      "launcher",
      "editor",
      "desktop-service",
      "runtimes",
    ])
  }

def write_configs(configs: dict[str, str], filepath: str) -> None:
  for config in configs:
    write(
      f"{filepath}/configs/{config}.txt",
      configs[config]
    )

