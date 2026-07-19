from langchain.tools import tool

@tool
def open_url(url: str) -> str:
    """
    打开指定的URL链接

    Args:
        url: 要打开的URL地址

    Returns:
        str: 打开结果或错误信息
    """
    try:
        import webbrowser

        # 验证URL格式
        if not url.startswith(('http://', 'https://', 'www.')):
            return f"错误: URL格式无效，请使用完整格式（如 http:// 或 https://） - {url}"

        # 尝试打开URL
        webbrowser.open(url)

        return f"成功打开URL:\n{url}"

    except Exception as e:
        return f"错误: 打开URL时发生异常 - {str(e)}"



# 测试代码
if __name__ == "__main__":
    # 测试函数
    result = launch_application.invoke({"app_path": "notepad.exe"})
    print(result)
