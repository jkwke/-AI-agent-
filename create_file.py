import os
from langchain.tools import tool


@tool
def create_file_or_folder(path: str, is_folder: bool = False, content: str = "") -> str:
    """
    创建文件或文件夹

    Args:
        path: 要创建的文件或文件夹的完整路径
        is_folder: 是否创建文件夹，默认为False（创建文件）
        content: 如果创建文件，可指定初始内容

    Returns:
        str: 操作结果信息
    """
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in path or path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 规范化路径
        normalized_path = os.path.normpath(path)

        if is_folder:
            # 创建文件夹
            if os.path.exists(normalized_path):
                return f"错误: 路径已存在 - {normalized_path}"

            os.makedirs(normalized_path, exist_ok=True)
            return f"成功创建文件夹: {normalized_path}"
        else:
            # 创建文件
            # 检查内容长度，防止创建过大的文件
            if len(content) > 10 * 1024 * 1024:  # 10MB限制
                return f"错误: 内容过大 ({len(content)} 字符)，超过10MB限制"

            # 确保父目录存在
            parent_dir = os.path.dirname(normalized_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            # 创建或覆盖文件
            with open(normalized_path, 'w', encoding='utf-8') as file:
                file.write(content)

            return f"成功创建文件: {normalized_path}\n文件大小: {len(content)} 字符"

    except PermissionError:
        return f"错误: 没有权限创建路径 - {path}"
    except OSError as e:
        return f"错误: 操作系统错误 - {str(e)}"
    except Exception as e:
        return f"错误: 创建文件或文件夹时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 测试创建文件
    result = create_file_or_folder.invoke({
        "path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_created_file.txt",
        "is_folder": False,
        "content": "这是通过工具创建的测试文件内容"
    })
    print("创建文件测试:")
    print(result)

    print("\n" + "=" * 50 + "\n")

    # 测试创建文件夹
    result = create_file_or_folder.invoke({
        "path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_created_folder",
        "is_folder": True
    })
    print("创建文件夹测试:")
    print(result)
