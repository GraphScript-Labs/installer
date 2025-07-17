from typing import Self, Callable, TypeAlias
from webhost import host
from os.path import exists, isdir
from utils import APP_DIR
from webview import (
  create_window,
  Window,
  start,
  FOLDER_DIALOG,
)

InstallFn: TypeAlias = Callable[[
  dict[str, str]
], None]

class InstallerWindow:
  window: Window
  installFn: InstallFn

  def __init__(
    self: Self,
    installFn: InstallFn,
    url: str,
    title: str = 'GraphScript',
    dims: tuple[int, int] = (600, 400),
    acryllic: bool = True,
    frameless: bool = True,
    fulldrag: bool = False,
    resizable: bool = True,
  ) -> None:
    self.installFn = installFn
    self.window = create_window(
      title=title,
      url=url,
      js_api=self,
      width=dims[0],
      height=dims[1],
      transparent=acryllic,
      vibrancy=acryllic,
      frameless=frameless,
      easy_drag=fulldrag,
      resizable=resizable,
    )

  def close(self: Self) -> None:
    self.window.destroy()
    exit(0)

  def check_path(self: Self, path: str) -> bool:
    return exists(path) and isdir(path)

  def select_folder(self: Self) -> str:
    return (self.window.create_file_dialog(
      FOLDER_DIALOG,
      allow_multiple=False,
    ) or [""])[0]

  def install(self: Self, configs: dict[str, str]) -> None:
    self.installFn(configs)
    self.close()

def launch_window(installFn: InstallFn) -> None:
  port, _ = host(f"{APP_DIR}/frontend")
  InstallerWindow(installFn, f"http://localhost:{port}/")
  start()

