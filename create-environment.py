import argparse
import os
from pathlib import Path

import jinja2

source_template_code = """
from pathlib import Path
from common.create_command_and_desktop_entry import CreateCommandAndDesktopEntry


def main():
    executor = CreateCommandAndDesktopEntry(
        "{{ binary_name }}", "{{ appimage_name }}", "{{ icon_name }}", Path(__file__).parent
    )
    executor.main()


if __name__ == "__main__":
    main()
"""  # noqa: E501


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--binary-name", "-b", help="The name of the binary to create", required=True
    )
    parser.add_argument(
        "--appimage-name",
        "-a",
        help="The name of the appimage we want to install",
        required=True,
    )
    parser.add_argument(
        "--icon-name", "-i", help="The name of the icon we want to install"
    )
    args = parser.parse_args()

    binary_name = args.binary_name
    appimage_name = args.appimage_name
    icon_name = args.icon_name if args.icon_name else binary_name

    print(f"Creating directory for {binary_name}")
    os.makedirs(binary_name, exist_ok=True)
    print(f"Creating script file for {binary_name}")
    template = jinja2.Template(source_template_code)
    script_path = Path(__file__).parent / binary_name / "main.py"
    script_path.write_text(
        template.render(
            binary_name=binary_name, appimage_name=appimage_name, icon_name=icon_name
        )
    )
    print("Done")


if __name__ == "__main__":
    main()
