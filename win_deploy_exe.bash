#!/bin/bash

# 定义虚拟环境路径变量, 修改为自身Windows系统的虚拟环境的路径
VENV_PATH="/d/PyEnv/openai"

PROJECT_PATH="./chat_gui_server"
WIN_WEBVIEW_PY="webview_pack"
DEST_DIR="./dist/$WIN_WEBVIEW_PY/_internal"

# 虚拟环境激活脚本路径
VENV_ACTIVE_PATH="$VENV_PATH/Scripts/activate"

# 检查虚拟环境激活脚本是否存在
if [ ! -f "$VENV_ACTIVE_PATH" ]; then
  echo "Virtual environment activation script not found: $VENV_ACTIVE_PATH"
  exit 1
fi

# 激活虚拟环境
source "$VENV_ACTIVE_PATH"

# 检查虚拟环境是否已激活
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment activated."
else
    echo "Failed to activate virtual environment."
    exit 1
fi

# 进入到chat_gui_server的目录
cd "$PROJECT_PATH"

# 开始build出spec文件
pyinstaller "$WIN_WEBVIEW_PY.py" -y

# 开始build出exe文件
pyinstaller "$WIN_WEBVIEW_PY.spec" -y

# 定义源文件夹和目标文件夹
SRC_DIR="$VENV_PATH/Lib/site-packages"
# 检查源文件夹是否存在
if [ ! -d "$SRC_DIR" ]; then
  echo "Source directory does not exist: $SRC_DIR"
  exit 1
fi

# 检查目标文件夹是否存在
if [ ! -d "$DEST_DIR" ]; then
  echo "Destination directory does not exist: $DEST_DIR"
  exit 1
fi

# 定义递归复制函数
copy_items() {
  local src="$1"
  local dest="$2"

  for item in "$src"/*; do
    local filename=$(basename "$item")
    local dest_item="$dest/$filename"

    if [ -e "$dest_item" ]; then
      echo "Skipping existing item: $dest_item"
    else
      if [ -d "$item" ]; then
        # 如果是文件夹，创建目标文件夹并递归复制内容
        echo "Copying directory: $item"
        cp -r "$item" "$dest_item"
      else
        # 复制文件
        echo "Copying file: $item"
        cp "$item" "$dest_item"
      fi
    fi
  done
}

# # 开始复制内容
copy_items "$SRC_DIR" "$DEST_DIR"

cp -r "./.dbpath" "$DEST_DIR"
cp -r "./statics" "$DEST_DIR"
cp "./config.json" "$DEST_DIR"

echo "Files copied successfully."