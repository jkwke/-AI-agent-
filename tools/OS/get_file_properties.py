import os
import time
from langchain.tools import tool


@tool
def get_file_properties(file_path: str) -> str:
    """
    获取文件的详细属性信息

    Args:
        file_path: 文件的完整路径

    Returns:
        str: 文件属性信息
    """
    try:
        # 验证路径安全性，防止路径遍历攻击
        if '..' in file_path or file_path.startswith('~'):
            return "错误: 不允许使用相对路径或用户主目录符号"

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误: 文件不存在 - {file_path}"

        # 检查是否为文件而非目录
        if not os.path.isfile(file_path):
            return f"错误: 路径不是文件 - {file_path}"

        # 获取文件统计信息
        stat_info = os.stat(file_path)

        # 格式化时间
        created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_ctime))
        modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime))
        accessed_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_atime))

        # 获取文件大小（字节转人类可读格式）
        size_bytes = stat_info.st_size
        size_units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = size_bytes
        unit_index = 0
        while size >= 1024 and unit_index < len(size_units) - 1:
            size /= 1024
            unit_index += 1
        readable_size = f"{size:.2f} {size_units[unit_index]}"

        # 获取文件名和扩展名
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]

        # 获取权限信息
        permissions = oct(stat_info.st_mode)[-3:]

        # 构建返回信息
        properties_info = f"文件属性信息:\n"
        properties_info += f"  文件路径: {file_path}\n"
        properties_info += f"  文件名: {file_name}\n"
        properties_info += f"  文件扩展名: {file_ext}\n"
        properties_info += f"  文件大小: {readable_size} ({size_bytes} 字节)\n"
        properties_info += f"  权限码: {permissions}\n"
        properties_info += f"  创建时间: {created_time}\n"
        properties_info += f"  修改时间: {modified_time}\n"
        properties_info += f"  访问时间: {accessed_time}\n"

        return properties_info

    except PermissionError:
        return f"错误: 没有权限访问文件 - {file_path}"
    except OSError as e:
        return f"错误: 系统操作失败 - {str(e)}"
    except Exception as e:
        return f"错误: 获取文件属性时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 示例用法
    result = get_file_properties.invoke({
        "file_path": r"C:\Users\30457\Desktop\文件夹\AI agent\test.txt"
    })
    print(result)
