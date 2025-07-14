from pathlib import Path

from common.create_command_and_desktop_entry import CreateCommandAndDesktopEntry


def main():
    executor = CreateCommandAndDesktopEntry(
        "obsidian", "Obsidian", "obsidian", Path(__file__).parent
    )
    executor.main()


if __name__ == "__main__":
    main()
