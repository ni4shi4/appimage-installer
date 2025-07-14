# 使い方

`create-environment.py`を使って、バイナリをインストールするための環境を準備する

- 例
```bash
uv run create-environment.py -b obsidian -a Obsidian
```

バイナリと同名のディレクトリ配下にインストールスクリプト`main.py`が作成される。Appimageごとにディレクトリ構成等が異なるので、必要に応じてメソッドのオーバーライドする([Cursor向けスクリプト](./cursor/main.py))

AppImageを`~/Downloads`配下にダウンロードした後に、インストールするためのスクリプトを実行する

- 例
```bash
uv run obsidian/main.py -v 1.8.10
```
