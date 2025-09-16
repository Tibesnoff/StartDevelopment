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
    try:
        keep = CHATBOT_LOCAL_BOT_REGISTRATION_UNDERSCORE if using_emulator else CHATBOT_LOCAL_BOT_REGISTRATION
        remove = CHATBOT_LOCAL_BOT_REGISTRATION if using_emulator else CHATBOT_LOCAL_BOT_REGISTRATION_UNDERSCORE

        if os.path.exists(remove):
            flip_filename(remove)
        if os.path.exists(keep) and os.path.exists(remove):
            os.remove(remove)
    except Exception as e:
        print(f"Error flipping emulator file: {e}")

def _launch_vs(path: str): 
    os.startfile(path)

def run_vs_task_in_terminal(project_path: str, task_name: str):
    try:
        # For Chatbot, the package.json is in ChatBot/ChatBot/ subdirectory
        if "ChatBot" in project_path:
            # Extract the base path and go to ChatBot/ChatBot/ subdirectory
            base_dir = os.path.dirname(project_path)  # Gets to ChatBot folder
            package_dir = os.path.join(base_dir, "ChatBot")  # Goes to ChatBot/ChatBot/
        else:
            package_dir = os.path.dirname(project_path)
        
        print(f"Starting '{task_name}' in terminal window...")
        print(f"Looking for package.json in: {package_dir}")
        
        # Create a batch command that runs the npm script
        batch_content = f"""@echo off
title {task_name}
cd /d "{package_dir}"
echo Starting {task_name}...
echo Working directory: {package_dir}
echo Press Ctrl+C to stop
echo.

REM Check if package.json exists
if not exist package.json (
    echo ERROR: package.json not found in {package_dir}
    echo Please check the path and try again.
    pause
    exit /b 1
)

npm run {task_name}
echo.
echo Task completed. Press any key to close.
pause >nul
"""
        
        # Write batch file to temp location
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
            f.write(batch_content)
            batch_file = f.name
        
        # Run the batch file in a new terminal window
        subprocess.Popen(['cmd', '/c', 'start', batch_file], shell=True)
        print(f"Task '{task_name}' started in terminal window")
        return True
        
    except Exception as e:
        print(f"Error starting task '{task_name}': {e}")
        return False

def _launch_vscode(path: str):    
    if not os.path.exists(path):
        print(f"ERROR: Path does not exist: {path}")
        return
    
    vscode_commands = [
        ["code", path],
        ["code.cmd", path],
        ["C:\\Program Files\\Microsoft VS Code\\Code.exe", path],
        ["C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe", path]
    ]
    
    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        vscode_commands.append([os.path.join(user_profile, "AppData", "Local", "Programs", "Microsoft VS Code", "Code.exe"), path])
    
    for cmd in vscode_commands:
        try:
            subprocess.run(cmd, check=True, shell=True)
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
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

    print(f"Opening '{project['name']}' in {project['editor']}")
    try:
        EDITOR_LAUNCHERS[project["editor"]](project["path"])
    except Exception as e:
        print(f"Failed to open project: {e}")

def reset_projects():
    print("Resetting all project configurations...")
    edit_json_key(JSON_PATHS["Switchboard"], "Api.Persistence.BaseUrl", HOME_SB_API_URL)
    edit_json_key(JSON_PATHS["Switchboard"], "Api.DirectLine.DirectLineSecret", DEV_DIRECTLINE_SECRET)
    edit_json_key(JSON_PATHS["Chatbot"], "Api.SwitchboardApi.BaseUrl", DEV_SB_API_URL)
    edit_json_key(JSON_PATHS["Chatstats"], "SwitchboardApi.BaseUrl", DEV_SB_API_URL)
    toggle_chatbot_local_bot_registration(using_emulator=False)
    print("All projects reset to default (dev) configuration.")

def run_chatbot(should_run_directline: bool, is_full_project: bool, using_emulator: bool):
    toggle_chatbot_local_bot_registration(using_emulator)
    url = LOC_SB_API_URL if is_full_project else DEV_SB_API_URL
    edit_json_key(JSON_PATHS["Chatbot"], "Api.SwitchboardApi.BaseUrl", url)
    
    if should_run_directline:
        run_vs_task_in_terminal(PATHS["Chatbot"], "start-static-ngrok-tunnel")
    
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
    "F": lambda: (
        run_chatstats(True),
        run_switchboard(True, True),
        run_switchboard_api(),
        run_chatbot(True, True, False)
    ),
    "CS": lambda: (
        run_chatbot(True, False, False),
        run_switchboard(False, True)
    ),
    "CE": lambda: run_chatbot(False, False, True),
    "C": lambda: run_chatbot(False, False, False),
    "S": lambda: run_switchboard(False, False),
    "ST": lambda: run_chatstats(False),
    "API": run_switchboard_api,
    "R": reset_projects,
}

def run_selection_manager(selection: str):
    action = SELECTION_ACTIONS.get(selection)
    if action:
        print(f"\nLaunching {selection} configuration...")
        action()
        print("Configuration complete!")
    else:
        print(f"Unknown selection: {selection}")
