from os import rename, remove
from zipfile import ZipFile

from ssl import create_default_context
from certifi import where as certifi_where

from urllib.request import (
  urlretrieve,
  build_opener,
  install_opener,
  HTTPSHandler
)

context = create_default_context(cafile=certifi_where())
opener = build_opener(HTTPSHandler(context=context))
install_opener(opener)

def pull_source(repo: str, filepath: str) -> None:
  url: str = "https://github.com/GraphScript-Labs/"
  branch: str = "latest-release"
  full_url: str = f"{url}/{repo}/archive/refs/heads/{branch}.zip"

  update_zip = urlretrieve(
    full_url,
    f"{filepath}/{repo}.zip"
  )

  with ZipFile(update_zip[0], 'r') as zip_ref:
    zip_ref.extractall(filepath)
    rename(
      f"{filepath}/{repo}-{branch}",
      f"{filepath}/{repo}"
    )

    remove(f"{filepath}/{repo}.zip")

