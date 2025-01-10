<div align="center">
  <img src="header.webp" height="150">
  <h1>KeilTool</h1>
  <span>This is a tool that provides automated management for Keil projects (.uvprojx files).😄
  </span>
</div>
<br>
<p align="center">
<a href="_">English</a> | <a href="../README.md">简体中文</a>
</p>

## Features 
- Automatically search and locate `.uvprojx` files.
- Automatically create file groups based on directory structure and depth.
- Add header file directories to the Keil project based on specified paths.
- Delete header file paths or file groups that match specific regular expressions.  

## Quick Start  
1. Clone the project:
   ```bash  
   git clone https://github.com/Rev-RoastedDuck/Keil-Tool.git  
   cd Keil-Tool  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ``` 
3. Run the tool:
   ```bash  
   python keil_tool.py  
   ```  

## Commands
***1. Header File Path Management***
- **`add_include_path <path>`**  
  - Recursively add the path specified by `<path>` as the header file path of the Keil project.
  - Example: `add_include_path./include`  

- **`del_include_path <regex_pattern>`**  
  - Delete header file paths that match the regular expression `<regex_pattern>`.
  - Example: `del_include_path ^./include.*`  

***2. File Group Management***
- **`creat_files_group <path> <max_depth> [group_root_name]`**  
  - Create file groups based on `.c` files in the `<path>` path and its subfolders, with the depth specified by `<max_depth>`.
  - Example: `creat_files_group./src 2 MyGroup`  

- **`del_exist_group <regex_pattern>`**  
  - Delete file groups that match the regular expression `<regex_pattern>`.
  - Example: `del_exist_group ^OldGroup.*`  

***3. Others***
- **`update_root`**  
  - Reload the root node of the `.uvprojx` file.
- **`help`**  
  - View the help documentation.
- **`exit`**  
  - Exit the program.


## Contribution Guidelines  
1. Fork the repository.
2. Create a feature branch `git checkout -b feature/your-feature`.
3. Commit your changes `git commit -m "Add your feature"`.
4. Push the branch `git push origin feature/your-feature`.
5. Submit a Pull Request.


## Notes  
- Ensure that there is only one `.uvprojx` file in the current directory, otherwise an error message about the number of files will be displayed.  
- Please back up the `.uvprojx` file before using this tool to prevent data loss due to accidental operations.  


## License  
KeilTool is based on the MIT License. See the [LICENSE](https://github.com/Rev-RoastedDuck/Keil-Tool/blob/main/LICENSE) file for details. 

If you have any questions, feel free to submit feedback on [GitHub Issues](https://github.com/Rev-RoastedDuck/Keil-Tool/issues).