import os
import shutil
import requests
from tkinter import Tk, filedialog

def patch_studio():
    print("Please select RobloxStudioBeta.exe.")

    app_data_folder = os.environ['LOCALAPPDATA']
    versions_folder = os.path.join(app_data_folder, "Roblox", "Versions")
    versions_dirs = [d for d in os.listdir(versions_folder) if os.path.isdir(os.path.join(versions_folder, d))]
    
    target_dir = None
    for version_dir in versions_dirs:
        if os.path.isfile(os.path.join(versions_folder, version_dir, "RobloxStudioBeta.exe")):
            target_dir = os.path.join(versions_folder, version_dir)
            break

    if not target_dir:
        print("RobloxStudioBeta.exe not found.")
        return

    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=target_dir, title="Select RobloxStudioBeta.exe", filetypes=[("Roblox Studio", "RobloxStudioBeta.exe")])
    if not file_path:
        print("No file selected. Exiting patching.")
        return

    input("Loaded .exe, Press Enter to continue!")
    
    with open(file_path, 'rb') as f:
        file_data = f.read()

    print("Looking for bytes..")
    patch_done = False
    for i in range(len(file_data) - 3):
        if file_data[i:i+4] == b':/Pl':
            file_data = file_data[:i] + b'./Pl' + file_data[i+4:]
            print("Found byte & Patching")
            patch_done = True

    patched_file_path = os.path.join(target_dir, "RobloxStudioPatched.exe")
    with open(patched_file_path, 'wb') as f:
        f.write(file_data)

    if not patch_done:
        print("No bytes to patch found.")
        return

    print("Found Bytes and Patched RobloxStudioBeta")

    target_dir = os.path.dirname(file_path)
    platform_path = os.path.join(target_dir, "Platform")
    base_path = os.path.join(platform_path, "Base", "QtUI", "themes")
    base_path = os.path.normpath(base_path)
    print(base_path)
    os.makedirs(platform_path, exist_ok=True)
    os.makedirs(base_path, exist_ok=True)
    
    dark_theme_url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/QtResources/Platform/Base/QtUI/themes/DarkTheme.json"
    light_theme_url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/QtResources/Platform/Base/QtUI/themes/LightTheme.json"
    foundation_dark_theme_url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/QtResources/Platform/Base/QtUI/themes/FoundationDarkTheme.json"
    foundation_light_theme_url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/QtResources/Platform/Base/QtUI/themes/FoundationLightTheme.json"

    dark_theme_path = os.path.join(base_path, "DarkTheme.json")
    light_theme_path = os.path.join(base_path, "LightTheme.json")
    foundation_dark_theme_path = os.path.join(base_path, "FoundationDarkTheme.json")
    foundation_light_theme_path = os.path.join(base_path, "FoundationLightTheme.json")

    print("Downloading theme files...")
    try:
        download_file(dark_theme_url, dark_theme_path)
        download_file(light_theme_url, light_theme_path)
        download_file(foundation_dark_theme_url, foundation_dark_theme_path)
        download_file(foundation_light_theme_url, foundation_light_theme_path)
        print("Theme files downloaded successfully.")
    except Exception as e:
        print(f"Failed to download theme files: {e}")
        return

    os.startfile(os.path.dirname(patched_file_path))

def download_file(url, file_path):
    """
    Download the file from the provided URL and save it to the specified file path.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    patch_studio()
