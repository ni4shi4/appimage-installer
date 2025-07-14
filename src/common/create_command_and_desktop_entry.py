import argparse
import os
import shutil
import stat
import subprocess
from pathlib import Path


class CreateCommandAndDesktopEntry:
    def __init__(
        self, binary_name: str, appimage_name: str, icon_name: str, current_dir: Path
    ):
        self.binary_name = binary_name
        self.appimage_name = appimage_name
        self.icon_name = icon_name
        self.current_dir = current_dir

        self.define_paths()

    def define_paths(self):
        self.home_dir = Path.home()
        self.download_dir = self.home_dir / "Downloads"
        self.command_path = self.home_dir / ".local/bin" / self.binary_name
        self.desktop_entry_path = (
            self.home_dir / ".local/share/applications" / f"{self.binary_name}.desktop"
        )
        self.icon_path = self.home_dir / ".local/share/icons" / f"{self.icon_name}.png"
        self.extracted_dir = self.current_dir / "squashfs-root"

    def parse_args(self) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--version",
            "-v",
            help="The version of the appimage we want to install",
            required=True,
        )
        args = parser.parse_args()
        return args.version

    def get_appimage_name(self, version: str) -> str:
        return f"{self.appimage_name}-{version}.AppImage"

    def get_appimage_working_path(self, version: str) -> Path:
        return self.current_dir / self.get_appimage_name(version)

    def remove_existing_extracted_directory(self):
        if os.path.exists(self.extracted_dir):
            shutil.rmtree(self.extracted_dir)

    def copy_appimage_to_current_dir(self, version: str):
        print(f"Copying appimage to {self.current_dir}")
        shutil.copy(
            self.download_dir / self.get_appimage_name(version),
            self.get_appimage_working_path(version),
        )

    def make_appimage_executable(self, version: str):
        print(f"Making appimage executable: {self.get_appimage_working_path(version)}")
        st = os.stat(self.get_appimage_working_path(version))
        os.chmod(self.get_appimage_working_path(version), st.st_mode | stat.S_IEXEC)

    def extract_appimage(self, version: str):
        print("extracting appimage")
        subprocess.run(
            [self.get_appimage_working_path(version), "--appimage-extract"],
            cwd=self.current_dir,
        )

    def create_symlink_to_executable_file(self):
        print(f"Creating symlink to executable file to {self.command_path}")
        if os.path.isfile(self.command_path) or os.path.islink(self.command_path):
            os.remove(self.command_path)
        os.symlink(self.extracted_dir / self.binary_name, self.command_path)

    def create_desktop_entry(self):
        print(f"Creating desktop entry to {self.desktop_entry_path}")
        with open(self.extracted_dir / f"{self.binary_name}.desktop", "r") as f:
            desktop_entry = f.read().replace("AppRun", self.binary_name)
        with open(self.desktop_entry_path, "w") as f:
            f.write(desktop_entry)

    def copy_desktop_icon_to_desktop_entry_path(self):
        print(f"Copying desktop icon to {self.desktop_entry_path.parent}")
        shutil.copy(self.extracted_dir / f"{self.icon_name}.png", self.icon_path)

    def clean_up(self, version: str):
        print("cleaning up")
        os.remove(self.get_appimage_working_path(version))

    def main(self):
        version = self.parse_args()
        self.remove_existing_extracted_directory()
        self.copy_appimage_to_current_dir(version)
        self.make_appimage_executable(version)
        self.extract_appimage(version)
        self.create_symlink_to_executable_file()
        self.create_desktop_entry()
        self.copy_desktop_icon_to_desktop_entry_path()
        self.clean_up(version)
        print("Done")
