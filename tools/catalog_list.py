import os
from langchain.tools import tool


@tool
def list_directory(dir_path: str) -> str:
    """
    列出指定目录中的文件和子目录

    Args:
        dir_path: 目录的完整路径

    Returns:
        str: 目录内容列表信息
    """
    try:
        # 验证路径安全性
        if '..' in dir_path or dir_path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 规范化路径
        normalized_path = os.path.normpath(dir_path)

        if not os.path.exists(normalized_path):
            return f"错误: 目录不存在 - {normalized_path}"

        if not os.path.isdir(normalized_path):
            return f"错误: 路径不是目录 - {normalized_path}"

        # 获取目录内容
        items = os.listdir(normalized_path)

        if not items:
            return f"目录为空: {normalized_path}"

        # 分别列出文件和目录
        files = []
        directories = []

        for item in items:
            item_path = os.path.join(normalized_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(f"  文件: {item} ({size} bytes)")
            elif os.path.isdir(item_path):
                directories.append(f"  目录: {item}")

        result = f"目录内容: {normalized_path}\n"
        result += f"总计: {len(files)} 个文件, {len(directories)} 个目录\n\n"

        if directories:
            result += "子目录:\n"
            result += "\n".join(directories) + "\n\n"

        if files:
            result += "文件:\n"
            result += "\n".join(files)

        return result

    except PermissionError:
        return f"错误: 没有权限访问目录 - {dir_path}"
    except Exception as e:
        return f"错误: 访问目录时发生异常 - {str(e)}"


if __name__ == "__main__":
    result = list_directory.invoke({"dir_path": r"C:\Users\30457\Desktop\文件夹\AI agent"})
    print(result)
