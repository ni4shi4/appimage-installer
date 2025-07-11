import jinja2
from pathlib import Path
import os
import argparse


def main():
    template_path = Path(__file__).parent / "create-command-and-desktop-entry.py.jinja"
    template = jinja2.Template(template_path.read_text())

    parser = argparse.ArgumentParser()
    parser.add_argument("--binary-name", "-b", help="The name of the binary to create", required=True)
    parser.add_argument("--appimage-name", "-a", help="The name of the appimage we want to install", required=True)
    parser.add_argument("--icon-name", "-i", help="The name of the icon we want to install")
    args = parser.parse_args()

    binary_name = args.binary_name
    appimage_name = args.appimage_name
    icon_name = args.icon_name if args.icon_name else binary_name

    print(f"Creating directory for {binary_name}")
    os.makedirs(binary_name, exist_ok=True)
    print(f"Creating script file for {binary_name}")
    script_path = Path(__file__).parent / binary_name / "create-command-and-desktop-entry.py"
    script_path.write_text(template.render(binary_name=binary_name, appimage_name=appimage_name, icon_name=icon_name))
    print("Done")

if __name__ == "__main__":
    main()
