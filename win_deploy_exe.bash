#!/bin/bash

# 检测操作系统类型
OS_TYPE=$(uname)
if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Operating System: Linux"
elif [[ "$OS_TYPE" == "MINGW64_NT"* || "$OS_TYPE" == "CYGWIN_NT"* ]]; then
    echo "Operating System: Windows 10"
else
    echo "Operating System: Unknown. Exit!"
    exit 1
fi

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "You are not in a virtual environment."
    echo "Please activate your virtual environment before running this script. Exit!"
    exit 1
else
    echo "You are currently in the virtual environment: $VIRTUAL_ENV"
fi

# 检查是否安装了Node.js并输出其路径
printf "Environment check [1/3]: "
NODE_PATH=$(which node || echo "Node.js is not installed.")
if [ "$NODE_PATH" == "Node.js is not installed. Failed!" ]; then
    echo "$NODE_PATH Please install Node.js and try again. Exit!"
    exit 1
else
    echo "Node.js is installed at: $NODE_PATH"
fi

# 检查是否安装了npm并输出其路径
printf "Environment check [2/3]: "
NPM_PATH=$(which npm || echo "npm is not installed.")
if [ "$NPM_PATH" == "npm is not installed. Failed!" ]; then
    echo "$NPM_PATH Please install npm and try again. Exit!"
    exit 1
else
    echo "npm is installed at: $NPM_PATH"
fi

# 检查虚拟环境中的Python是否安装了PyInstaller并输出其路径
printf "Environment check [3/3]: "
PYINSTALLER_PATH=$(which pyinstaller || echo "PyInstaller is not installed.")
if [ "$PYINSTALLER_PATH" == "PyInstaller is not installed. Failed!" ]; then
    echo "$PYINSTALLER_PATH Please install PyInstaller with 'pip install pyinstaller' and try again. Exit!"
    exit 1
else
    echo "PyInstaller is installed at: $PYINSTALLER_PATH"
fi

# 提示用户确认是否继续
read -p "Do you want to continue with the current virtual environment? (y/N): " confirm
confirm=${confirm,,}  # 将输入转换为小写

if [[ "$confirm" != "y" ]]; then
    echo "Exiting the script."
    exit 1
fi

# 脚本继续执行...
echo "Continuing with the script execution..."


cd chat_gui_server

pyinstaller win_pyinstaller.spec

rm -r build

mv dist ../.app

echo "Build sccess! See app in .app folder."