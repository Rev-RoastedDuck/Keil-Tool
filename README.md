<div align="center">
  <img src="res/header.webp" height="150">
  <h1>KeilTool</h1>
  <span>这是一个为 Keil 工程 (.uvprojx 文件) 提供自动化管理的工具😄
  </span>
</div>
<br>
<p align="center">
<a href="res/README_en.md">English</a> | <a href=" ">简体中文</a>
</p>

## 功能 
- 自动搜索并定位 `.uvprojx` 文件
- 根据目录结构和深度自动创建文件组
- 根据指定路径添加头文件目录到 Keil 工程
- 删除符合特定正则表达式的头文件路径或文件组

## 快速开始  
1. 克隆项目:
   ```bash  
   git clone https://github.com/Rev-RoastedDuck/Keil-Tool.git  
   cd Keil-Tool  
   ```  
2. 安装依赖:  
   ```bash  
   pip install -r requirements.txt  
   ``` 
3. 运行工具:
   ```bash  
   python keil_tool.py  
   ```  

## 命令
***1. 头文件路径管理***
- **`add_include_path <path>`**  
  - 将 `<path>` 指定的路径递归添加为 Keil 工程的头文件路径
  - 示例：`add_include_path ./include`  

- **`del_include_path <regex_pattern>`**  
  - 删除符合正则表达式 `<regex_pattern>` 的头文件路径
  - 示例：`del_include_path ^./include.*`  

***2. 文件组管理***
- **`creat_files_group <path> <max_depth> [group_root_name]`**  
  - 根据 `<path>` 路径及其子文件夹中的 .c 文件创建文件组，深度由 `<max_depth>` 指定
  - 示例：`creat_files_group ./src 2 MyGroup`  

- **`del_exist_group <regex_pattern>`**  
  - 删除符合正则表达式 `<regex_pattern>` 的文件组
  - 示例：`del_exist_group ^OldGroup.*`  

***3. 其他***
- **`update_root`**  
  - 重新加载 `.uvprojx` 文件的根节点。
- **`help`**  
  - 查看帮助文档
- **`exit`**  
  - 退出程序

## 贡献指南  
1. Fork 仓库
2. 创建功能分支 `git checkout -b feature/your-feature`
3. 提交修改 `git commit -m "Add your feature"`
4. 推送分支 `git push origin feature/your-feature`
5. 提交 Pull Request


## 注意事项  
- 确保当前目录中只有一个 `.uvprojx` 文件，否则会提示文件数目错误。  
- 使用本工具前请备份 `.uvprojx` 文件以防止误操作导致数据丢失。  


## 许可证  
KeilTool 基于 MIT 许可证。详情参见 [LICENSE](https://github.com/Rev-RoastedDuck/Keil-Tool/blob/main/LICENSE) 文件。 

如有问题，欢迎在 [GitHub Issues](https://github.com/Rev-RoastedDuck/Keil-Tool/issues) 提交反馈。
