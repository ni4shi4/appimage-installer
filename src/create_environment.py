import argparse
import json
import os
from pathlib import Path

import jinja2
import tomlkit

ROOT_DIR = Path(__file__).resolve().parents[1]
APPS_DIR = ROOT_DIR / "src" / "app"

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


def _normalize_function_name(binary_name: str) -> str:
    return binary_name.replace("-", "_")


def _add_project_script(pyproject_path: Path, script_name: str, module_name: str):
    content = pyproject_path.read_text()
    doc = tomlkit.parse(content)
    if "project" not in doc or not isinstance(doc["project"], dict):
        doc["project"] = tomlkit.table()
    project = doc["project"]
    if "scripts" not in project or not isinstance(project["scripts"], dict):
        project["scripts"] = tomlkit.table()
    scripts = project["scripts"]
    script_value = f"app.{module_name}.main:main"
    if script_name in scripts and scripts[script_name] == script_value:
        return
    scripts[script_name] = script_value
    pyproject_path.write_text(tomlkit.dumps(doc))


def add_entrypoint(script_name: str, binary_name: str):
    module_name = _normalize_function_name(binary_name)
    pyproject_path = ROOT_DIR / "pyproject.toml"
    _add_project_script(pyproject_path, script_name, module_name)


def _load_config(config_path: Path) -> list[dict]:
    content = json.loads(config_path.read_text())
    if isinstance(content, dict) and "items" in content:
        items = content["items"]
    else:
        items = content
    if not isinstance(items, list):
        raise ValueError('config must be a JSON array or {"items": [...]}')
    return items


def create_environment(
    binary_name: str,
    appimage_name: str,
    icon_name: str | None = None,
    add_entrypoint_flag: bool = False,
    entrypoint_name: str | None = None,
):
    icon_name = icon_name if icon_name else binary_name
    module_name = _normalize_function_name(binary_name)

    print(f"Creating directory for {binary_name}")
    os.makedirs(APPS_DIR / module_name, exist_ok=True)
    print(f"Creating script file for {binary_name}")
    template = jinja2.Template(source_template_code)
    script_path = APPS_DIR / module_name / "main.py"
    script_path.write_text(
        template.render(
            binary_name=binary_name, appimage_name=appimage_name, icon_name=icon_name
        )
    )
    if add_entrypoint_flag:
        entrypoint_name = (
            entrypoint_name if entrypoint_name else f"install-{binary_name}"
        )
        add_entrypoint(entrypoint_name, binary_name)


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
    parser.add_argument(
        "--config",
        help='JSON file with multiple app definitions (array or {"items": [...]})',
    )
    parser.add_argument(
        "--add-entrypoint",
        action="store_true",
        help="Add a project script entry point for installation",
    )
    parser.add_argument(
        "--entrypoint-name",
        help="Entry point name in [project.scripts] (default: install-<binary>)",
    )
    args = parser.parse_args()

    if args.config:
        config_path = Path(args.config).expanduser().resolve()
        for item in _load_config(config_path):
            create_environment(
                item["binary_name"],
                item["appimage_name"],
                item.get("icon_name"),
                item.get("add_entrypoint", args.add_entrypoint),
                item.get("entrypoint_name"),
            )
    else:
        create_environment(
            args.binary_name,
            args.appimage_name,
            args.icon_name,
            args.add_entrypoint,
            args.entrypoint_name,
        )
    print("Done")


if __name__ == "__main__":
    main()
