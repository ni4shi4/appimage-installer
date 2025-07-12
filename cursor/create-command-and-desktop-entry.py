import os
import stat
from pathlib import Path
import shutil
import subprocess
import argparse

binary_name = "cursor"
icon_name = "co.anysphere.cursor"

current_dir = Path(__file__).parent
home_dir = Path.home()
download_dir = home_dir / "Downloads"
command_path = home_dir / ".local/bin" / binary_name
desktop_entry_path = home_dir / ".local/share/applications" / f"{binary_name}.desktop"
icon_path = home_dir / ".local/share/icons" / f"{icon_name}.png"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", help="The version of the appimage we want to install", required=True)
    args = parser.parse_args()

    appimage_name = f"Cursor-{args.version}.AppImage"
    appimage_download_path = download_dir / appimage_name
    appimage_working_path = current_dir / appimage_name
    extracted_dir = current_dir / "squashfs-root"

    print(f"Copying appimage to {current_dir}")
    shutil.copy(appimage_download_path, appimage_working_path)

    print(f"Making appimage executable: {appimage_working_path}")
    st = os.stat(appimage_working_path)
    os.chmod(appimage_working_path, st.st_mode | stat.S_IEXEC)

    print(f"extracting appimage")
    subprocess.run([appimage_working_path, "--appimage-extract"], cwd=current_dir)

    print(f"Creating symlink to executable file to {command_path}")
    if os.path.isfile(command_path) or os.path.islink(command_path):
        os.remove(command_path)
    os.symlink(extracted_dir / "usr/bin" / binary_name, command_path)

    print(f"Creating desktop entry to {desktop_entry_path}")
    with open(extracted_dir / f"{binary_name}.desktop", "r") as f:
        desktop_entry = f.read().replace(f"Exec={binary_name} ", f"Exec={binary_name} --no-sandbox ")
    with open(desktop_entry_path, "w") as f:
        f.write(desktop_entry)

    print(f"Copying desktop icon to {desktop_entry_path.parent}")
    shutil.copy(extracted_dir / f"{icon_name}.png", icon_path)

    print(f"cleaning up")
    os.remove(appimage_working_path)

    print(f"Done")

if __name__ == "__main__":
    main()
