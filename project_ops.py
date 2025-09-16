import os
import subprocess
from typing import Literal, TypedDict
from file_utils import flip_filename
from json_editor import edit_json_key

# === Constants ===
# API URLs
DEV_SB_API_URL = "https://switchboard-api.dev.webstaurantstore.com"
LOC_SB_API_URL = "https://switchboard-api.loc.clarkinc.biz"
HOME_SB_API_URL = "https://switchboard-api.home.webstaurantstore.com"

# Directline Secrets
DEV_DIRECTLINE_SECRET = "MgZiuFAwJVM.wzgoxkxKlMd7JgAw8iRrECdS93bzPKyRjE4DA4pm2oA"
LOC_DIRECTLINE_SECRET = "1mh32hU8yGo.0Bz5LQVXRH-4c4bbxYas9PdKNpEVkGwVpe9kTYjtv7s"

# Editors
VISUAL_STUDIO = "Visual Studio"
VS_CODE = "VS Code"

# Paths
BASE_PATH = r"C:\NonBackup\Development_Repos"
PATHS = {
    "Chatbot": os.path.join(BASE_PATH, "ChatBot", "ChatBot.sln"),
    "Switchboard": os.path.join(BASE_PATH, "Switchboard-Client", "Switchboard-Client.sln"),
    "SbClient": os.path.join(BASE_PATH, "Switchboard-Client", "Switchboard.Web", "client-app"),
    "SwitchboardApi": os.path.join(BASE_PATH, "SwitchboardAPIDotNetCore", "SwitchboardApi.sln"),
    "Chatstats": os.path.join(BASE_PATH, "ChatStats", "ChatStats.sln"),
}

# JSON Configs
JSON_PATHS = {
    "Switchboard": os.path.join(BASE_PATH, "Switchboard-Client", "Switchboard.Web", "appsettings.json"),
    "Chatbot": os.path.join(BASE_PATH, "ChatBot", "ChatBot", "appsettings.json"),
    "Chatstats": os.path.join(BASE_PATH, "ChatStats", "ChatStats", "appsettings.json"),
}

# Emulator files
BOT_REGISTRATION_FILENAME = "appsettings.bot-registration.json"
CHATBOT_LOCAL_BOT_REGISTRATION = os.path.join(BASE_PATH, "ChatBot", "ChatBot", "LocalAppSettings", BOT_REGISTRATION_FILENAME)
CHATBOT_LOCAL_BOT_REGISTRATION_UNDERSCORE = os.path.join(BASE_PATH, "ChatBot", "ChatBot", "LocalAppSettings", f"_{BOT_REGISTRATION_FILENAME}")

# === Types ===
AllowedProject = Literal["Chatbot", "Switchboard", "SbClient", "SwitchboardApi", "Chatstats"]

class ProjectInfo(TypedDict):
    name: str
    path: str
    editor: Literal["Visual Studio", "VS Code"]

# === Allowed Projects ===
allowed_projects: dict[AllowedProject, ProjectInfo] = {
    "Chatbot": {"name": "Chatbot", "path": PATHS["Chatbot"], "editor": VISUAL_STUDIO},
    "Switchboard": {"name": "Switchboard", "path": PATHS["Switchboard"], "editor": VISUAL_STUDIO},
    "SbClient": {"name": "Switchboard (client)", "path": PATHS["SbClient"], "editor": VS_CODE},
    "SwitchboardApi": {"name": "SwitchboardApi", "path": PATHS["SwitchboardApi"], "editor": VISUAL_STUDIO},
    "Chatstats": {"name": "Chatstats", "path": PATHS["Chatstats"], "editor": VISUAL_STUDIO},
}

# === Helpers ===
def toggle_chatbot_local_bot_registration(using_emulator: bool):
    """Ensure only the correct chatbot registration file exists."""
    try:
        keep = CHATBOT_LOCAL_BOT_REGISTRATION_UNDERSCORE if using_emulator else CHATBOT_LOCAL_BOT_REGISTRATION
        remove = CHATBOT_LOCAL_BOT_REGISTRATION if using_emulator else CHATBOT_LOCAL_BOT_REGISTRATION_UNDERSCORE

        if os.path.exists(remove):
            flip_filename(remove)
        if os.path.exists(keep) and os.path.exists(remove):
            os.remove(remove)
    except Exception as e:
        print(f"Error flipping emulator file: {e}")

# Editor launchers
def _launch_vs(path: str): os.startfile(path)
def _launch_vscode(path: str):
    try:
        subprocess.Popen(["code", path])
    except Exception:
        os.startfile(path)

EDITOR_LAUNCHERS = {
    VISUAL_STUDIO: _launch_vs,
    VS_CODE: _launch_vscode,
}

def open_project(project_name: AllowedProject):
    project = allowed_projects.get(project_name)
    if not project:
        print(f"Project '{project_name}' is not recognized.")
        return

    print(f"Opening '{project['name']}' in {project['editor']} at {project['path']}")
    try:
        EDITOR_LAUNCHERS[project["editor"]](project["path"])
    except Exception as e:
        print(f"Failed to open project: {e}")

# === Reset ===
def reset_projects():
    edit_json_key(JSON_PATHS["Switchboard"], "Api.Persistence.BaseUrl", HOME_SB_API_URL)
    edit_json_key(JSON_PATHS["Switchboard"], "Api.DirectLine.DirectLineSecret", DEV_DIRECTLINE_SECRET)
    edit_json_key(JSON_PATHS["Chatbot"], "Api.SwitchboardApi.BaseUrl", DEV_SB_API_URL)
    edit_json_key(JSON_PATHS["Chatstats"], "SwitchboardApi.BaseUrl", DEV_SB_API_URL)

    toggle_chatbot_local_bot_registration(using_emulator=False)

    print("All projects reset to default (dev) configuration.")

# === Project Runners ===
def run_chatbot(should_run_directline: bool, is_full_project: bool, using_emulator: bool):
    toggle_chatbot_local_bot_registration(using_emulator)
    url = LOC_SB_API_URL if is_full_project else DEV_SB_API_URL
    edit_json_key(JSON_PATHS["Chatbot"], "Api.SwitchboardApi.BaseUrl", url)
    open_project("Chatbot")

def run_switchboard(is_full_project: bool, has_chatbot: bool):
    persistence_url = LOC_SB_API_URL if is_full_project else HOME_SB_API_URL
    directline_secret = LOC_DIRECTLINE_SECRET if has_chatbot else DEV_DIRECTLINE_SECRET
    edit_json_key(JSON_PATHS["Switchboard"], "Api.Persistence.BaseUrl", persistence_url)
    edit_json_key(JSON_PATHS["Switchboard"], "Api.DirectLine.DirectLineSecret", directline_secret)
    open_project("Switchboard")
    open_project("SbClient")

def run_chatstats(is_full_project: bool):
    url = LOC_SB_API_URL if is_full_project else DEV_SB_API_URL
    edit_json_key(JSON_PATHS["Chatstats"], "SwitchboardApi.BaseUrl", url)
    open_project("Chatstats")

def run_switchboard_api():
    open_project("SwitchboardApi")

# === Selection Manager ===
SELECTION_ACTIONS = {
    "Full Project": lambda: (
        run_chatstats(True),
        run_switchboard(True, True),
        run_switchboard_api(),
        run_chatbot(True, True, False)
    ),
    "Chatbot + Switchboard": lambda: (
        run_chatbot(True, False, False),
        run_switchboard(False, True)
    ),
    "Chatbot + Emulator": lambda: run_chatbot(False, False, True),
    "Chatbot": lambda: run_chatbot(False, False, False),
    "Switchboard": lambda: run_switchboard(False, False),
    "Chatstats": lambda: run_chatstats(False),
    "SwitchboardAPI": run_switchboard_api,
    "Reset": reset_projects,
}

def run_selection_manager(selection: str):
    action = SELECTION_ACTIONS.get(selection)
    if action:
        action()
    else:
        print(f"Unknown selection: {selection}")
