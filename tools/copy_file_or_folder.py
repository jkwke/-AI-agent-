import os
import shutil
from langchain.tools import tool


@tool
def copy_file_or_folder(source_path: str, destination_path: str) -> str:
    """
    复制文件或文件夹到指定位置

    Args:
        source_path: 源文件或文件夹的完整路径
        destination_path: 目标文件或文件夹的完整路径

    Returns:
        str: 操作结果信息
    """
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in source_path or source_path.startswith('~'):
            return "错误: 源路径不允许使用相对路径或用户主目录符号"

        if '..' in destination_path or destination_path.startswith('~'):
            return "错误: 目标路径不允许使用相对路径或用户主目录符号"

        # 检查源路径是否存在
        if not os.path.exists(source_path):
            return f"错误: 源路径不存在 - {source_path}"

        # 检查目标路径的父目录是否存在
        dest_parent = os.path.dirname(destination_path)
        if dest_parent and not os.path.exists(dest_parent):
            return f"错误: 目标路径的父目录不存在 - {dest_parent}"

        # 检查目标路径是否已存在
        if os.path.exists(destination_path):
            return f"错误: 目标路径已存在 - {destination_path}"

        # 根据源路径是文件还是目录选择适当的复制方法
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)  # copy2保留元数据
            item_type = "文件"
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)  # 递归复制目录
            item_type = "目录"
        else:
            return f"错误: 源路径既不是文件也不是目录 - {source_path}"

        return f"成功复制{item_type}: {source_path} -> {destination_path}"

    except PermissionError:
        return f"错误: 没有权限访问或复制 - {source_path} 或 {destination_path}"
    except OSError as e:
        return f"错误: 系统操作失败 - {str(e)}"
    except Exception as e:
        return f"错误: 复制时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 示例用法
    result = copy_file_or_folder.invoke({
        "source_path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_source.txt",
        "destination_path": r"C:\Users\30457\Desktop\文件夹\AI agent\copied_test.txt"
    })
    print(result)
