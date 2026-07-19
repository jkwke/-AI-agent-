import os
import shutil
from langchain.tools import tool
try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False


@tool
def delete_file_or_folder(path: str) -> str:
    """
    删除指定路径的文件或文件夹

    Args:
        path: 要删除的文件或文件夹的完整路径

    Returns:
        str: 操作结果信息
    """
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in path or path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 规范化路径
        normalized_path = os.path.normpath(path)

        # 检查路径是否存在
        if not os.path.exists(normalized_path):
            return f"错误: 路径不存在 - {normalized_path}"

        # 检查是否为文件或目录
        if os.path.isfile(normalized_path):
            # 删除文件
            os.remove(normalized_path)
            return f"成功删除文件: {normalized_path}"

        elif os.path.isdir(normalized_path):
            # 删除目录及其内容
            shutil.rmtree(normalized_path)
            return f"成功删除目录: {normalized_path} 及其所有内容"

        else:
            return f"错误: 路径不是有效的文件或目录 - {normalized_path}"

    except PermissionError:
        return f"错误: 没有权限删除 - {normalized_path}"
    except OSError as e:
        return f"错误: 删除失败 - {str(e)}"
    except Exception as e:
        return f"错误: 删除时发生异常 - {str(e)}"


@tool
def move_to_trash(path: str) -> str:
    """
    将指定路径的文件或文件夹移至回收站

    Args:
        path: 要移至回收站的文件或文件夹的完整路径

    Returns:
        str: 操作结果信息
    """
    global HAS_SEND2TRASH
    if not HAS_SEND2TRASH:
        return "错误: 未安装send2trash库，请先运行 'pip install send2trash'"
    
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in path or path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 规范化路径
        normalized_path = os.path.normpath(path)

        # 检查路径是否存在
        if not os.path.exists(normalized_path):
            return f"错误: 路径不存在 - {normalized_path}"

        # 移至回收站
        send2trash(normalized_path)
        return f"成功将 {normalized_path} 移至回收站"

    except Exception as e:
        return f"错误: 移至回收站失败 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 测试函数
    # result = delete_file_or_folder.invoke({"path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_delete.txt"})
    # print(result)
    
    # 测试移至回收站功能
    result = move_to_trash.invoke({"path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_move_to_trash.txt"})
    print(result)
