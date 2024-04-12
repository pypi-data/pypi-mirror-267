import logging
from pathlib import Path
import subprocess
from typing import Dict, List
from xdg import DesktopEntry
from linkwiz.config import config

APPNAME: str = "LinkWiz"
HTTP_HANDLER: str = "x-scheme-handler/http"

DESKTOP_PATHS = [
    Path("/usr/share/applications/"),
    Path.home() / ".local/share/applications/",
]


def get_browsers() -> Dict[str, Path]:
    """Get the name and exec path of browsers."""
    try:
        installed_browsers = []
        if config.main.get("auto_find_browsers", True):
            output = subprocess.check_output(["gio", "mime", HTTP_HANDLER], text=True)
            installed_browsers = (
                output.split("Recommended applications:")[-1].strip().split("\n")
            )
            installed_browsers = [app.strip() for app in installed_browsers]

            own_desktop = f"{APPNAME.lower()}.desktop"

            if own_desktop in installed_browsers:
                installed_browsers.remove(own_desktop)

        return get_browser_exec(installed_browsers)
    except subprocess.CalledProcessError:
        logging.error("Error getting installed browsers")
        exit(1)


def get_browser_exec(browsers_desktop: List[str]) -> Dict[str, Path]:
    """Get the exec path of installed browsers."""
    installed_browsers: Dict[str, Path] = {}
    for path in DESKTOP_PATHS:
        if not path.exists():
            continue
        for entry in path.glob("*.desktop"):
            if entry.name not in browsers_desktop:
                continue
            desktop_entry = DesktopEntry.DesktopEntry(str(entry))
            name: str = desktop_entry.getName()
            execpath: str = desktop_entry.getExec()
            installed_browsers[name] = Path(execpath)

    installed_browsers.update(config.browsers)

    return installed_browsers
