import os
from langchain.tools import tool


@tool
def rename_file_or_folder(source_path: str, new_name: str) -> str:
    """
    重命名文件或文件夹

    Args:
        source_path: 源文件或文件夹的完整路径
        new_name: 新的名称（不包含路径）

    Returns:
        str: 操作结果信息
    """
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in source_path or source_path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 验证新名称的安全性
        if '..' in new_name or new_name.startswith('/') or new_name.startswith('\\'):
            return "错误: 新名称不能包含路径分隔符或上级目录符号"

        # 检查源路径是否存在
        if not os.path.exists(source_path):
            return f"错误: 源路径不存在 - {source_path}"

        # 获取源路径的父目录
        parent_dir = os.path.dirname(source_path)
        if not parent_dir:
            parent_dir = "."

        # 构建新的完整路径
        new_path = os.path.join(parent_dir, new_name)

        # 检查目标路径是否已存在
        if os.path.exists(new_path):
            return f"错误: 目标路径已存在 - {new_path}"

        # 执行重命名操作
        os.rename(source_path, new_path)

        # 判断是文件还是目录
        if os.path.isfile(new_path):
            item_type = "文件"
        elif os.path.isdir(new_path):
            item_type = "目录"
        else:
            item_type = "项目"

        return f"成功重命名{item_type}: {source_path} -> {new_path}"

    except PermissionError:
        return f"错误: 没有权限访问或重命名 - {source_path}"
    except OSError as e:
        return f"错误: 系统操作失败 - {str(e)}"
    except Exception as e:
        return f"错误: 重命名时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 示例用法
    result = rename_file_or_folder.invoke({
        "source_path": r"C:\Users\30457\Desktop\文件夹\AI agent\旧文件名.txt",
        "new_name": "新文件名.txt"
    })
    print(result)
