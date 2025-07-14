import os
from pathlib import Path

from common.create_command_and_desktop_entry import CreateCommandAndDesktopEntry


class CursorCreateCommandAndDesktopEntry(CreateCommandAndDesktopEntry):
    def __init__(self):
        super().__init__(
            "cursor", "Cursor", "co.anysphere.cursor", Path(__file__).parent
        )

    def create_symlink_to_executable_file(self):
        print(f"Creating symlink to executable file to {self.command_path}")
        if os.path.isfile(self.command_path) or os.path.islink(self.command_path):
            os.remove(self.command_path)
        os.symlink(self.extracted_dir / "usr/bin/cursor", self.command_path)

    def create_desktop_entry(self):
        with open(self.extracted_dir / "cursor.desktop", "r") as f:
            desktop_entry = f.read().replace("Exec=cursor", "Exec=cursor --no-sandbox ")
        with open(self.desktop_entry_path, "w") as f:
            f.write(desktop_entry)


def main():
    executor = CursorCreateCommandAndDesktopEntry()
    executor.main()


if __name__ == "__main__":
    main()
