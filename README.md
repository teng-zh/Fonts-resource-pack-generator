# Minecraft-generate-fonts-resource-pack

## Introduction
This is a powerful tool designed to generate custom font resource packs for Minecraft, allowing you to use unique fonts in your Minecraft game. Whether you're a map creator, a server administrator, or just a regular player looking to add a personal touch to your game, this tool provides an easy - to - use solution.

### Features
- **Lightning - fast Generation**: The tool can generate font resource packs in just 1 millisecond, significantly reducing waiting time and increasing efficiency.
- **Font Format Compatibility**: It supports both True Type Font (TTF) and Open Type Font (OTF), giving you a wide range of font options to choose from.
- **Extensive Version Support**: This tool can generate resource packs for all supported Minecraft versions from 1.13 to 1.21, ensuring compatibility with different game versions.
- **Customizable Parameters**: You can adjust the left shift, bottom shift, font size, and resolution according to your needs, enabling you to create highly customized font effects.
- **User - friendly Interface**: The graphical user interface (GUI) is intuitive and easy to use, even for beginners.

## Supported Versions
This tool supports Minecraft versions ranging from 1.13 to 1.21. It's important to select the correct version when generating the resource pack to ensure compatibility with your game.

## How to Use

### Prerequisites
- **Python Installation**: Python is required to run this tool. If Python is not installed on your system, the `main.bat` script will automatically download and install Python 3.9.13 for you.

### Steps
1. **Run the Batch Script**:
    - Navigate to the project directory in the command prompt.
    - Execute the `main.bat` script. This script will first check if Python is installed. If not, it will download and install Python 3.9.13 silently. After that, it will start the Python script for generating the font resource pack.
2. **Open the Font Generator Interface**:
    - Once the Python script starts, a GUI window will appear.
3. **Configure the Font Resource Pack**:
    - **Select Font File**: Click the "Select Font File" button and choose a TTF or OTF font file from your local storage.
    - **Set Icon (Optional)**: Click the "Select Icon File" button and choose a PNG image as the icon for your resource pack. If you don't select an icon, a default icon will be used.
    - **Enter Description**: In the "Enter Description" field, write a brief description of your font resource pack. This description will be displayed in the Minecraft resource pack list.
    - **Choose Output Folder**: Click the "Select Output Folder" button and select a directory on your computer to save the generated resource pack.
    - **Set Zip Package Name**: In the "Enter Zip Package Name" field, enter a name for the generated resource pack. If you choose the ZIP output format, this will be the name of the ZIP file.
    - **Select Output Format**: You can choose between "Folder" and "ZIP" as the output format. Selecting "Folder" will generate a folder containing the resource pack files, while "ZIP" will generate a compressed ZIP file.
    - **Select Game Version**: Use the dropdown menu to select the Minecraft version for which you want to generate the resource pack.
    - **Adjust Font Parameters**:
        - **Left Shift**: Enter the number of pixels to shift the font horizontally.
        - **Bottom Shift**: Enter the number of pixels to shift the font vertically.
        - **Font Size**: Set the size of the font.
        - **Resolution**: Adjust the resolution of the font for better clarity.
4. **Generate the Resource Pack**:
    - After completing all the above configurations, click the "Create Resource Pack" button. The tool will start generating the resource pack, and a progress bar will show the generation progress.
    - Once the progress reaches 100%, a message box will pop up indicating that the resource pack has been generated successfully, along with the path where it is saved.
5. **Use the Resource Pack in Minecraft**:
    - Open Minecraft and go to the main menu.
    - Click "Options" and then select "Resource Packs".
    - Click "Open Resource Pack Folder" and copy the generated resource pack (either the folder or the ZIP file) into this folder.
    - Back in the resource pack selection screen, move the newly added resource pack from the left - hand list to the right - hand list to activate it.

## Installation
### Automatic Installation (Recommended)
1. Make sure your computer is connected to the Internet.
2. Download the project files from the GitHub repository and extract them to a local directory.
3. Double - click the `main.bat` file. This script will handle the Python installation if necessary and start the font resource pack generation tool.

### Manual Installation
1. **Install Python 3.9.13**:
    - Visit the official Python website (https://www.python.org/downloads/release/python - 3913/) and download the Python 3.9.13 installer for your operating system.
    - Run the installer and make sure to check the "Add Python to PATH" option during the installation process.
2. **Install Dependencies**:
    - Open the command prompt or terminal and navigate to the project directory.
    - If the project has a `requirements.txt` file, run `pip install -r requirements.txt` to install the required Python libraries. Otherwise, ensure that you have installed `tkinter` (usually included in the Python standard library), `Pillow`, `shutil`, `os`, `zipfile`, and `base64` libraries.
3. **Run the Program**: In the command prompt or terminal, navigate to the project directory and run `python downloaded_script.py` to start the font resource pack generation tool.

## Troubleshooting
### Resource Pack Not Working in Minecraft
- **Version Mismatch**: Ensure that the version you selected when generating the resource pack matches the version of your Minecraft game.
- **Incorrect Placement**: Make sure the resource pack is correctly placed in the Minecraft resource pack folder and is selected in the game's resource pack menu.
- **Conflicts**: Some Minecraft mods or other resource packs may conflict with the newly generated font resource pack. Try disabling other mods or resource packs and test again.

### Error During Generation
- **Check Error Messages**: Carefully read the error message. It usually contains information about the cause of the error, such as a missing font file or an invalid output folder path. Correct the corresponding settings according to the error message.
- **File Permissions**: If the error is related to file permissions, ensure that you have read and write permissions for the output folder and related files.
- **Report an Issue**: If the problem persists, please open an issue on the GitHub repository, providing detailed information about the error and your operation steps.

## Contribution
We welcome contributions from the community! If you'd like to contribute to this project, please follow these steps:
1. **Fork the Repository**: Click the "Fork" button on the GitHub repository page to create a copy of the project in your own GitHub account.
2. **Clone the Repository**: On your forked repository page, click the green "Code" button and copy the repository URL. Then, use the `git clone` command in your local command prompt or terminal to clone the repository to your computer, e.g., `git clone [repository URL]`.
3. **Create a New Branch**: Navigate to the cloned project directory and use the `git checkout -b [new branch name]` command to create a new branch for your feature or bug - fix. The branch name should clearly indicate the purpose of your work.
4. **Make Changes and Commit**: Make your code changes and use `git add.` to stage all the modified files. Then, use `git commit -m "[commit message]"` to commit your changes. The commit message should concisely describe the changes you've made.
5. **Push the Branch**: Use `git push origin [new branch name]` to push your local branch to your GitHub repository.
6. **Submit a Pull Request**: Go back to the original project's GitHub repository page. You should see a "Compare & pull request" button. Click it, select your branch, and submit a pull request. Provide a detailed description of your changes in the pull request.

We will review your pull request as soon as possible and provide feedback. If there are any required modifications, please adjust your code accordingly and resubmit.

## License
This project is licensed under the [[MIT License](LICENSE](https://github.com/teng-zh/Fonts-resource-pack-generator/blob/main/License.txt)). You are free to use, modify, and distribute the project code, but you must retain the original author's copyright notice and license information in related documents or products. Please refer to the LICENSE file for specific terms.

## Contact
If you encounter any problems during use, have suggestions, or ideas, you can contact us in the following ways:
- **GitHub Issues**: Submit detailed problem descriptions or suggestions on the [Issues page](https://github.com/teng - zh/Fonts - resource - pack - generator/issues) of the project repository. We will check and respond promptly.
- **Email**: You can also send an email to [lask27wq@hotmail.com] to communicate with us.

Thank you for using our tool! We hope it will bring more fun and creativity to your Minecraft journey.

# Minecraft字体资源包生成器

## 项目简介
本工具是一款专为 Minecraft 玩家和开发者设计的**字体资源包生成器**，旨在帮助用户快速、便捷地创建自定义字体资源包，从而轻松改变 Minecraft 游戏内的字体显示效果，为游戏增添个性化风格。无论是制作专属的冒险地图、搭建创意服务器，还是仅仅想为自己的游戏体验带来新鲜感，这款工具都能满足你的需求。

## 核心功能
### 1. 快速高效生成
- 借助优化的算法和代码架构，能够在极短时间内完成字体资源包的生成，大幅提升工作效率，减少等待时间。
- 即使是复杂的字体设置和高分辨率要求，也能迅速处理，确保流畅的使用体验。

### 2. 丰富的字体支持
- **格式支持**：全面兼容 True Type Font（TTF）和 Open Type Font（OTF）两种常见字体格式，可满足不同来源和类型的字体使用需求。
- **自定义配置**：允许用户灵活设置字体的各项参数，包括**左侧偏移**、**下侧偏移**、**字体大小**以及**分辨率**。通过调整这些参数，能够实现独特的字体显示效果，如微调字体位置、改变字体大小以适应不同界面布局、设置合适的分辨率保证字体清晰美观等。

### 3. 广泛的版本适配
- 支持从 Minecraft 1.13 到 1.21 的多个版本，无论是经典旧版本的回顾游玩，还是紧跟最新版本的创意探索，都能为你提供字体资源包支持，无需担心版本兼容性问题。

### 4. 便捷的图形化操作界面
- 采用直观的图形用户界面（GUI）设计，操作简单易懂，即使是初次使用的用户也能快速上手。
- 提供清晰的操作指引和提示信息，如文件选择、参数设置、生成进度展示等，让整个字体资源包创建过程一目了然。

## 安装指南
### 自动安装（推荐）
1. 确保你的计算机已连接网络。
2. 从 GitHub 仓库下载项目文件，并解压到本地任意目录。
3. 双击运行 `main.bat` 文件。该脚本会自动检测计算机中是否安装了 Python：
    - **若未安装**：脚本将自动下载并安装 Python 3.9.13 版本，安装过程为静默模式，无需手动干预。安装完成后，会自动启动字体资源包生成工具。
    - **若已安装**：直接启动字体资源包生成工具，开始使用。

### 手动安装
1. 安装 Python 3.9.13：
    - 访问 Python 官方网站（https://www.python.org/downloads/release/python - 3913/）下载对应操作系统的 Python 3.9.13 安装包。
    - 运行安装包，在安装过程中勾选“Add Python to PATH”选项，以便在命令行中能够直接调用 Python 命令。
2. 安装项目依赖：
    - 打开命令提示符或终端，切换到项目所在目录。
    - 运行 `pip install -r requirements.txt` 命令（如果项目包含该文件，用于安装所需的 Python 库）。若没有该文件，确保已安装 `tkinter`（Python 标准库，通常默认安装）、`Pillow`、`shutil`、`os`、`zipfile`、`base64` 等相关库。
3. 运行程序：在命令提示符或终端中，进入项目目录，运行 `python downloaded_script.py` 启动字体资源包生成工具。

## 使用教程
### 1. 启动工具
按照上述安装指南中的方法启动字体资源包生成工具，会弹出图形化操作界面。

### 2. 配置字体资源包
- **选择字体文件**：
    - 点击“选择字体文件”按钮，在弹出的文件选择窗口中，找到并选中你想要使用的 TTF 或 OTF 字体文件，然后点击“打开”。所选字体文件路径将显示在对应的输入框中。
- **设置图标（可选）**：
    - 点击“选择图标文件”按钮，选择一个 PNG 格式的图片作为字体资源包的图标。若不选择图标，工具将使用默认图标。
- **输入描述信息**：在“输入描述”输入框中，填写关于该字体资源包的描述内容，如字体用途、风格特点等。该描述信息将显示在 Minecraft 游戏内资源包的介绍中。
- **选择输出文件夹**：
    - 点击“选择输出文件夹”按钮，选择一个本地目录用于保存生成的字体资源包文件。
- **设置压缩包名称**：在“输入压缩包名称”输入框中，为生成的字体资源包输入一个名称。若选择输出格式为 ZIP，该名称将作为压缩包文件名；若选择输出为文件夹，该名称将作为文件夹名。
- **选择输出格式**：在“选择输出格式”下拉菜单中，可选择“文件夹”或“ZIP”。选择“文件夹”将生成一个包含资源包文件的文件夹；选择“ZIP”将生成一个压缩格式的资源包文件。
- **选择游戏版本**：在“选择游戏版本”下拉菜单中，根据你要使用字体资源包的 Minecraft 游戏版本进行选择，确保资源包与游戏版本兼容。
- **调整字体参数**：
    - 在“左侧偏移”输入框中，输入字体在水平方向上的偏移量（单位为像素），可调整字体的左右位置。
    - 在“下侧偏移”输入框中，输入字体在垂直方向上的偏移量（单位为像素），可调整字体的上下位置。
    - 在“字体大小”输入框中，输入字体的大小数值，控制字体在游戏内的显示尺寸。
    - 在“分辨率”输入框中，输入合适的分辨率数值，影响字体的清晰度和细节表现。

### 3. 生成资源包
完成上述所有配置后，点击“创建资源包”按钮，工具将开始生成字体资源包。界面中的进度条会实时显示生成进度，等待进度达到 100% 后，弹出提示框告知资源包生成成功，并显示资源包的保存路径。

### 4. 在 Minecraft 中使用资源包
- 打开 Minecraft 游戏，进入主菜单。
- 点击“选项”，然后选择“资源包”。
- 在资源包选择界面，点击“打开资源包文件夹”按钮，将生成的字体资源包文件（文件夹或 ZIP 压缩包）复制到该文件夹中。
- 返回资源包选择界面，在左侧未选中资源包列表中找到刚刚添加的字体资源包，点击“>”箭头将其移动到右侧已选中资源包列表中，即可在游戏中应用该字体资源包，体验全新的字体显示效果。

## 常见问题解答（FAQ）
### 1. 为什么生成的字体资源包在 Minecraft 中没有生效？
- 请确保你选择的游戏版本与生成资源包时所选版本一致，不匹配的版本可能导致资源包无法正常加载。
- 检查资源包是否正确放置在 Minecraft 的资源包文件夹中，并且已在游戏的资源包选择界面中选中启用。
- 部分 Minecraft 模组或其他资源包可能与新生成的字体资源包产生冲突，尝试禁用其他模组或资源包后再进行测试。

### 2. 支持导入哪些特殊字体？
理论上，只要是符合 TTF 或 OTF 格式标准的字体文件都可以导入使用。但某些包含特殊字符编码或复杂格式设置的字体，可能在游戏中显示异常。若遇到此类问题，建议尝试使用其他常规字体或对字体进行适当转换和调整。

### 3. 生成资源包时提示错误怎么办？
- 仔细查看错误提示信息，通常会包含导致错误的原因，如未选择字体文件、输出文件夹路径无效等。根据提示信息补充或修正相应的设置。
- 若错误提示与文件权限相关，请确保你对输出文件夹和相关文件拥有读写权限。
- 如果问题仍然存在，请在 GitHub 仓库的 [Issues](https://github.com/teng - zh/Fonts - resource - pack - generator/issues) 页面提交详细的错误描述和操作步骤，以便开发者及时排查和解决。

## 贡献指南
我们非常欢迎广大开发者和 Minecraft 爱好者参与到本项目的开发和完善中来！如果你想为项目贡献代码或提出建议，可参考以下步骤：
1. **Fork 仓库**：点击 GitHub 仓库页面右上角的“Fork”按钮，将本项目仓库复制到你自己的 GitHub 账号下。
2. **克隆仓库**：在你自己的 GitHub 仓库页面，点击绿色的“Code”按钮，复制仓库地址。然后打开本地命令提示符或终端，使用 `git clone` 命令将仓库克隆到本地计算机，例如：`git clone [你复制的仓库地址]`。
3. **创建分支**：进入克隆到本地的项目目录，使用 `git checkout -b [新分支名称]` 命令创建一个新的分支，用于开发你的功能或修复 bug。分支名称应尽量简洁明了，能够体现你所做的工作内容。
4. **开发与提交**：在新分支上进行代码开发或修改，完成后使用 `git add.` 命令添加所有变更文件，然后使用 `git commit -m "[提交信息]"` 命令提交你的更改。提交信息应清晰描述本次提交的目的和主要内容，方便其他开发者理解。
5. **推送分支**：使用 `git push origin [新分支名称]` 命令将你本地的分支推送到你在 GitHub 上的仓库。
6. **提交 Pull Request**：返回本项目的原始 GitHub 仓库页面，此时会显示一个“Compare & pull request”按钮，点击该按钮，选择你刚刚推送的分支与原始仓库的主分支进行对比。确认无误后，点击“Create pull request”按钮提交拉取请求，并在描述中详细说明你的更改内容和目的。

我们会尽快对提交的 Pull Request 进行审核和反馈。如果有任何需要修改的地方，请根据审核意见进行调整，并再次提交。

## 许可证
本项目基于 [MIT 许可证](LICENSE) 发布，这意味着你可以自由地使用、修改和分发本项目代码，但需在相关文档或产品中保留原作者的版权声明和许可证信息。具体使用条款请参考 LICENSE 文件内容。

## 联系与反馈
如果你在使用过程中遇到问题、有任何建议或想法，欢迎通过以下方式与我们联系：
- **GitHub Issues**：在 [项目仓库的 Issues 页面](https://github.com/teng - zh/Fonts - resource - pack - generator/issues) 提交详细的问题描述或建议，我们会及时查看和回复。
- **邮箱**：你也可以发送邮件至 [lask27wq@hotmail.com]，与我们进行沟通交流。

感谢你的使用和支持，希望这款工具能为你的 Minecraft 之旅带来更多乐趣和创意！    
