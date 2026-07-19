from .skills import *
from .OS import *

# 定义导出的工具列表
__all__ = [
    'get_time',  # 获取时间
    'get_weather',  # 获取天气
    'open_file',  # 打开文件
    'write_file',  # 写入文件
    'create_file_or_folder',  # 创建文件或文件夹
    'list_directory',  # 列出目录
    'delete_file_or_folder',  # 删除文件或文件夹
    'move_to_trash',  # 移动到回收站
    'rename_file_or_folder',  # 重命名文件或文件夹
    'move_file_or_folder',  # 移动文件或文件夹
    'copy_file_or_folder',  # 复制文件或文件夹
    'get_file_properties',  # 获取文件属性
    'execute_command',  # 执行命令
    'open_url',  # 打开URL
    'web_search',  # 网络搜索
]

# 工具名称中文映射
tool_name_zh_map = {
    "web_search": "网络搜索",
    "delete_file_or_folder": "删除文件或文件夹",
    "move_to_trash": "移动到回收站",
    "create_file": "创建文件",
    "write_file": "写入文件",
    "rename_file_or_folder": "重命名文件或文件夹",
    "move_file_or_folder": "移动文件或文件夹",
    "copy_file_or_folder": "复制文件或文件夹",
    "get_file_properties": "获取文件属性",
    "open_file": "打开文件",
    "list_directory": "列出目录内容",
    "get_time": "获取时间",
    "get_weather": "获取天气",
    "execute_command": "执行命令行",
    "open_url": "打开URL",
}
