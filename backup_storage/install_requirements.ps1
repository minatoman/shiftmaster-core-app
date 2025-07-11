# install_requirements.ps1
$ErrorActionPreference = "Stop"

# 仮想環境を作成する場所
$venvPath = "H:\Projects\ShiftMaster\env"

# 仮想環境が既に存在しない場合、作成
if (-not (Test-Path $venvPath)) {
    python -m venv $venvPath
}

# 仮想環境をアクティブにする
& "$venvPath\Scripts\Activate"

# 必要なモジュールをインストール
pip install --upgrade pip
pip install -r "H:\Projects\ShiftMaster\backup\config\requirements.txt"
