import os
from langchain.tools import tool


@tool
def open_file(file_path: str) -> str:
    """
    打开并读取指定路径的文件内容

    Args:
        file_path: 文件的完整路径

    Returns:
        str: 文件的内容或错误信息
    """
    try:
        # 验证文件路径的安全性，防止路径遍历攻击
        if '..' in file_path or file_path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误: 文件不存在 - {file_path}"

        # 检查是否为文件而非目录
        if not os.path.isfile(file_path):
            return f"错误: 路径不是文件 - {file_path}"

        # 检查文件大小，避免读取过大的文件
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # 10MB限制
            return f"错误: 文件过大 ({file_size} 字节)，超过10MB限制"

        # 尝试读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 限制返回内容长度，防止返回过长的内容
        if len(content) > 5000:
            content = content[:5000] + "\n... (内容已截断)"

        return f"成功读取文件: {file_path}\n文件大小: {file_size} 字节\n\n文件内容:\n{content}"

    except UnicodeDecodeError:
        # 如果UTF-8编码失败，尝试其他编码
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                content = file.read()
            if len(content) > 5000:
                content = content[:5000] + "\n... (内容已截断)"
            return f"成功读取文件 (GBK编码): {file_path}\n\n文件内容:\n{content}"
        except Exception as e:
            return f"错误: 无法读取文件 - {str(e)}"
    except PermissionError:
        return f"错误: 没有权限访问文件 - {file_path}"
    except Exception as e:
        return f"错误: 读取文件时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 测试函数
    file_path = r"C:\Users\30457\Desktop\文件夹\AI agent\天气.txt"
    result = open_file.invoke({"file_path": file_path})
    print(result)
