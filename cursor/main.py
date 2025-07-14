from pathlib import Path

from common.create_command_and_desktop_entry import CreateCommandAndDesktopEntry


class CursorCreateCommandAndDesktopEntry(CreateCommandAndDesktopEntry):
    def __init__(self):
        super().__init__(
            "cursor", "Cursor", "co.anysphere.cursor", Path(__file__).parent
        )

    def create_desktop_entry(self):
        with open(self.extracted_dir / f"{self.binary_name}.desktop", "r") as f:
            desktop_entry = f.read().replace(
                f"Exec={self.binary_name} ", f"Exec={self.binary_name} --no-sandbox "
            )
        with open(self.desktop_entry_path, "w") as f:
            f.write(desktop_entry)


def main():
    executor = CursorCreateCommandAndDesktopEntry()
    executor.main()


if __name__ == "__main__":
    main()
