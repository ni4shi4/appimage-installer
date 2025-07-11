# 使い方

`create-environment.py`を使って、バイナリをインストールするための環境を準備する

- 例
```bash
uv run create-environment.py -b obsidian -a Obsidian
```

バイナリと同名のディレクトリ配下にインストールスクリプト`create-command-and-desktop-entry.py`が作成される。Appimageごとにディレクトリ構成が異なるので、バイナリへのパス等を編集する

AppImageを`~/Downloads`配下にダウンロードした後に、インストールするためのスクリプトを実行する

- 例
```bash
uv run obsidian/create-command-and-desktop-entry.py -v 1.8.10
```

