import os
from langchain.tools import tool


@tool
def write_file(file_path: str, content: str) -> str:
    """
    创建或覆盖文件并写入内容

    Args:
        file_path: 目标文件的完整路径
        content: 要写入文件的内容

    Returns:
        str: 操作结果信息
    """
    try:
        # 验证文件路径的安全性，防止路径遍历攻击
        if '..' in file_path or file_path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 验证文件路径的有效性
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            return f"错误: 目录不存在 - {directory}"

        # 检查内容长度，防止写入过大的文件
        if len(content) > 10 * 1024 * 1024:  # 10MB限制
            return f"错误: 内容过大 ({len(content)} 字符)，超过10MB限制"

        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return f"成功写入文件: {file_path}\n写入内容长度: {len(content)} 字符"

    except PermissionError:
        return f"错误: 没有权限写入文件 - {file_path}"
    except Exception as e:
        return f"错误: 写入文件时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 测试函数
    test_content = "这是一个测试文件内容"
    result = write_file.invoke({
        "file_path": r"C:\Users\30457\Desktop\文件夹\AI agent\test_output.txt",
        "content": test_content
    })
    print(result)
