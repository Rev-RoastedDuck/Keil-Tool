"""
keil_tool.h

 Created on: 2025_01_05
     Author: Rev_RoastDuck
     Github: https://github.com/Rev-RoastedDuck

:copyright: (c) 2023 by Rev-RoastedDuck.
"""

import os
import re
from pathlib import Path
from lxml import etree
from lxml.etree import _Element


class KeilTool:
    def __init__(self):
        self.uvprojx_path = ""
        self.etree_root = None

    def find_uvprojx_files(self) -> str:
        """
        搜索指定路径的.uvprojx文件
        :return: .uvprojx文件路径
        """
        current_dir = Path.cwd()
        uvprojx_files = []
        for file_path in current_dir.rglob("*.uvprojx"):
            uvprojx_files.append(str(file_path.relative_to(current_dir)))
        if not len(uvprojx_files) == 1:
            print("Keil-Tool: 请检查当前文件夹是否不存在或存在多个.uvprojx文件")
            return ""
        self.uvprojx_path = uvprojx_files[0]
        return uvprojx_files[0]

    def get_root(self, path: str = None) -> _Element:
        """
        获取uvprojx文件的根节点
        :param path:
        :return:
        """
        root_str = etree.tostring(etree.parse(path if path else self.uvprojx_path)).decode('utf-8')
        self.etree_root = etree.XML(root_str)
        return self.etree_root

    def get_file_type(self, suffix):
        """
        获取文件类型对应的映射值
        :param suffix: 文件后缀
        :return:
        """
        suffix_map = {".c": 1, ".h": 5}
        return str(suffix_map[suffix])

    def get_files_by_suffix(self, directory, suffix: list[str]):
        """
        搜索指定文件夹及子文件夹下所有特定后缀的文件
        :param directory: 要搜索的文件夹路径
        :param suffix: 指定的文件后缀
        :return:
        """
        file_info_list = []
        directory_path = Path(directory)
        for file_path in directory_path.rglob("*"):
            if file_path.suffix in suffix:
                file_info = {
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "file_type": self.get_file_type(file_path.suffix)
                }
                file_info_list.append(file_info)
        return file_info_list

    def get_folder_with_specific_files(self, root_dir, suffix: list[str]):
        """
        获取包含指定后缀文件的文件夹
        :param root_dir: 开始深度搜索的文件夹路径
        :param suffix: 文件后缀
        :return:
        """
        result = []
        root_path = Path(root_dir)
        for dir_path in root_path.rglob('*'):
            if dir_path.is_dir():
                for file_path in dir_path.glob('*'):
                    if file_path.is_file() and file_path.suffix in suffix:
                        result.append(str(dir_path).replace("\\", "/"))
                        break
        return result

    def creat_files_group(self, path: str, max_depth: int, group_root_name: str = None):
        """
        根据当前目录的格式和指定递归的深度，为uvprojx文件添加文件组
        :param etree_root: uvprojx文件的根节点
        :param path: 文件路径
        :param max_depth: 递归深度
        :param group_root_name: 组名字的前缀
        :return:
        """
        path = path.replace("\\", "/")
        folders = self.get_subfolders(path, max_depth)
        for folder in folders:
            infos = self.get_files_by_suffix(folder, [".c"])
            name = folder if not group_root_name else folder.replace(path, group_root_name)
            group = self.get_group(self.etree_root, name)

            files = group.xpath('.//Files')[0]
            for info in infos:
                self.add_file_to_files(files, info)
            # print(etree.tostring(group, pretty_print=True).decode())

        self.write_to_file(self.etree_root, self.uvprojx_path)

    def is_group_exist(self, etree_root: _Element, group_name: str):
        groups_name = etree_root.xpath(f'//Groups//GroupName[text()="{group_name}"]')
        return len(groups_name) > 0

    def get_group(self, etree_root: _Element, name: str):
        group_name_el = etree_root.xpath(f'//Groups//GroupName[text()="{name}"]')
        if group_name_el:
            return group_name_el[0].getparent()

        groups = etree_root.xpath('//Groups')[0]
        group = etree.Element("Group")
        group_name = etree.Element("GroupName")
        group_name.text = name
        group.append(group_name)
        files = etree.Element("Files")
        group.append(files)
        groups.append(group)

        return group

    def add_file_to_files(self, files: _Element, info: dict):
        file_name_el = files.xpath(f'.//FileName[text()="{info["file_name"]}"]')
        if file_name_el:
            return

        file = etree.Element("File")

        file_name = etree.Element("FileName")
        file_name.text = info["file_name"]

        file_type = etree.Element("FileType")
        file_type.text = info["file_type"]

        file_path = etree.Element("FilePath")
        file_path.text = self.get_relative_path_uvprojx(info["file_path"]).replace("\\", "/")

        file.append(file_name)
        file.append(file_type)
        file.append(file_path)

        files.append(file)

    def del_exist_group(self, regex_pattern: str):
        groups = self.etree_root.xpath(f'//Groups')[0]
        # group_name_list = self.etree_root.xpath(f'//Groups//GroupName[text()="{group_name}"]')
        group_name_list = self.etree_root.xpath(f'//Groups//GroupName')
        pattern = re.compile(regex_pattern)
        for group_name in group_name_list:
            if pattern.search(group_name.text):
                groups.remove(group_name.getparent())
        self.write_to_file(self.etree_root, self.uvprojx_path)

    def add_include_path(self, path: str):
        """
        为uvprojx添加目标编译的头文件路径
        :param path: 递归起始路径
        :return:
        """
        include_folders = self.get_folder_with_specific_files(path, [".h"])
        include_folders = [self.get_relative_path_uvprojx(folder).replace("\\", "/") for folder in include_folders]
        include_path_el = self.etree_root.xpath('//TargetArmAds//VariousControls/IncludePath')[0]

        include_path_list = include_path_el.text.split(";") + include_folders
        include_path_list = list(set(include_path_list))
        include_path_list.sort()
        include_path_el.text = ";".join(include_path_list)
        self.write_to_file(self.etree_root, self.uvprojx_path)

    def del_include_path(self, regex_pattern: str):
        """
        为uvprojx添加目标编译的头文件路径
        :param path: 递归起始路径
        :return:
        """
        include_path_el = self.etree_root.xpath('//TargetArmAds//VariousControls/IncludePath')[0]

        pattern = re.compile(regex_pattern)
        include_path_list = include_path_el.text.split(";")
        include_path_list = [item for item in include_path_list if not pattern.search(item)]
        include_path_el.text = ";".join(list(set(include_path_list)))
        self.write_to_file(self.etree_root, self.uvprojx_path)

    def get_relative_path(self, file_a, file_b):
        """
        获取文件的相对位置
        :param file_a:
        :param file_b:
        :return:
        """
        path_a = Path(file_a)
        path_b = Path(file_b)
        try:
            abs_path_a = path_a.resolve()
            abs_path_b = path_b.resolve()
            # 从文件 A 的绝对路径中移除文件 B 的父目录的绝对路径部分
            relative_path_parts = []
            i = 0
            while i < len(abs_path_a.parts) and i < len(abs_path_b.parts) and abs_path_a.parts[i] == abs_path_b.parts[
                i]:
                i += 1
            for j in range(i, len(abs_path_b.parts) - 1):
                relative_path_parts.append("..")
            relative_path_parts.extend(abs_path_a.parts[i:])
            relative_path = Path(*relative_path_parts)
            return str(relative_path)
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def get_relative_path_uvprojx(self, file_a) -> str:
        return self.get_relative_path(file_a, self.uvprojx_path)

    def write_to_file(self, etree_root, output_file):
        """
        将 XML 元素树写入文件
        :param etree_root: XML 元素树的根节点
        :param output_file: 输出文件的路径
        """
        tree = etree.ElementTree(etree_root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

    def get_subfolders(self, path: str, max_depth: int):
        """
        获取指定深度的文件夹路径
        :param path: 递归路径
        :param max_depth: 最深层目录的层数
        :return:
        """
        result = []

        for root, dirs, files in os.walk(path):
            depth = root[len(path):].count(os.sep)
            if depth < max_depth:
                if not len(dirs):
                    result.append(root)
                    del dirs[:]

                if depth == max_depth - 1:
                    for dir_name in dirs:
                        result.append(os.path.join(root, dir_name))
                    del dirs[:]
            else:
                del dirs[:]

        return [path.replace('\\', '/') for path in result]


def manual(language: str = None):
    def print_help_en():
        print("Available Commands:")
        print("\tadd_include_path <path>")
        print(
            "\t\t- Add header file path. <path> is the file system path to be added, such as '/path/to/include' or 'C:\\path\\to\\include'.")
        print("\tdel_include_path <regex_pattern>")
        print(
            "\t\t- Delete header file path. <regex_pattern> is a regular expression, for example, '^/path/to/.*' can be used to match paths that start with '/path/to/'.")
        print("\tcreat_files_group <path> <max_depth> [group_root_name]")
        print(
            "\t\t- Create a file group. <path> is the starting file system path, <max_depth> is the maximum search depth (an integer), and [group_root_name] is the optional root name of the group, for example, '/path/to/directory 2 MyGroup'.")
        print("\tdel_exist_group <regex_pattern>")
        print(
            "\t\t- Delete an existing file group. <regex_pattern> is a regular expression, for example, '^RRD*' can be used to match groups that start with 'RRD'.")
        print("\tupdate_root")
        print("\t\t- Update the root node.")
        print("\texit")
        print("\t\t- Exit the program.")
        print("Project Information:")
        print("\t- Author: Rev_RoastDuck")
        print("\t- Creation Time: 2024_01_08")
        print("\t- Github: https://github.com/Rev-RoastedDuck")

    def print_help_cn():
        print("可用的命令:")
        print("\tadd_include_path <path>")
        print("\t\t- 添加头文件路径。<path> 是要添加的文件系统路径，例如 '/path/to/include' 或 'C:\\path\\to\\include'。")
        print("\tdel_include_path <regex_pattern>")
        print("\t\t- 删除头文件路径。<regex_pattern> 是一个正则表达式，例如 '^/path/to/.*' 可用于匹配以 '/path/to/' 开头的路径。")
        print("\tcreat_files_group <path> <max_depth> [group_root_name]")
        print(
            "\t\t- 创建文件组。<path> 是起始文件系统路径，<max_depth> 是查找的最大深度（整数），[group_root_name] 是可选的组根名称，例如 '/path/to/directory 2 MyGroup'。")
        print("\tdel_exist_group <regex_pattern>")
        print("\t\t- 删除存在的文件组。<regex_pattern> 是一个正则表达式，例如 '^RRD*' 可用于匹配以 'RRD' 开头的组。")
        print("\tupdate_root")
        print("\t\t- 更新根节点。")
        print("\texit")
        print("\t\t- 退出程序。")
        print("项目信息:")
        print("\t- 作者：Rev_RoastDuck")
        print("\t- 创建时间：2024_01_08")
        print("\t- Github：https://github.com/Rev-RoastedDuck")

    if "en" == language:
        print_help_en()
    else:
        print_help_cn()


def main():
    manual()
    tool = KeilTool()
    g_file_path = tool.find_uvprojx_files()
    tool.get_root(g_file_path)

    command_table = {
        "add_include_path": tool.add_include_path,
        "del_include_path": tool.del_include_path,
        "creat_files_group": tool.creat_files_group,
        "del_exist_group": tool.del_exist_group,
        "update_root": tool.get_root,
        "help": manual
    }

    def parse_param(cmd: str, params: list):
        if "add_include_path" == cmd:
            return [params[0]]
        elif "creat_files_group" == cmd:
            return [params[0], int(params[1]), None if not len(params) == 3 else params[2]]
        elif "del_exist_group" == cmd:
            return [params[0]]
        elif "del_include_path" == cmd:
            return [params[0]]
        elif "update_root" == cmd:
            return []
        elif "help" == cmd:
            return ["" if not len(params) == 1 else params[0]]
        return []

    while True:
        user_input = input("keil tool: ")
        if user_input.lower() == 'exit':
            break

        try:
            parts = user_input.split()
            command = parts[0]
            if command not in command_table:
                print("无效的指令")
                continue
            tool.get_root()
            func = command_table[command]
            params = parse_param(command, parts[1:])
            if params is not None:
                func(*params)

        except IndexError:
            print("Keil-Tool: 输入格式错误，输入`help`或`help en`查看帮助文档。")
        except ZeroDivisionError as e:
            print(e)


main()
