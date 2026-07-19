import subprocess
import os
import shlex
from langchain.tools import tool


@tool
def execute_command(command: str) -> str:
    """
    在操作系统上执行命令行指令

    Args:
        command: 要执行的命令字符串

    Returns:
        str: 命令执行的结果或错误信息
    """
    try:
        # 安全检查：防止危险命令
        dangerous_commands = [
            'rm -rf', 'rm -fr', 'del /f /q', 'format', 'mkfs',
            'dd if=', 'cat /dev/zero', 'shutdown', 'reboot',
            'poweroff', 'halt', 'init 0', 'init 6'
        ]

        # 检查命令是否包含危险指令
        lower_command = command.lower()
        for danger_cmd in dangerous_commands:
            if danger_cmd in lower_command:
                return f"错误: 检测到危险命令 '{danger_cmd}'，已阻止执行"

        # 对于Windows系统，进一步检查危险命令
        if os.name == 'nt':  # Windows系统
            windows_dangerous = ['rd /s /q', 'diskpart', 'cipher /w:']
            for danger_cmd in windows_dangerous:
                if danger_cmd in lower_command:
                    return f"错误: 检测到危险命令 '{danger_cmd}'，已阻止执行"

        # 使用subprocess执行命令
        # 设置合理的超时时间，防止长时间挂起
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,  # 30秒超时
            cwd=os.getcwd()  # 使用当前工作目录
        )

        # 检查输出长度，限制返回内容
        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""

        # 限制输出长度，防止过长的内容
        if len(stdout) > 3000:
            stdout = stdout[:3000] + "\n... (输出已截断)"
        if len(stderr) > 3000:
            stderr = stderr[:3000] + "\n... (错误输出已截断)"

        if result.returncode == 0:
            # 成功执行
            if stdout:
                return f"命令执行成功:\n{command}\n\n标准输出:\n{stdout}"
            else:
                return f"命令执行成功:\n{command}\n(无输出)"
        else:
            # 执行失败
            if stderr:
                return f"命令执行失败:\n{command}\n\n错误信息:\n{stderr}"
            else:
                return f"命令执行失败:\n{command}\n(无错误信息)"

    except subprocess.TimeoutExpired:
        return f"错误: 命令执行超时 (超过30秒):\n{command}"

    except FileNotFoundError:
        return f"错误: 找不到命令或程序:\n{command}"

    except PermissionError:
        return f"错误: 没有权限执行命令:\n{command}"

    except Exception as e:
        return f"错误: 执行命令时发生异常 - {str(e)}"


# 测试代码
if __name__ == "__main__":
    # 测试函数
    test_command = "dir" if os.name == 'nt' else "ls -la"
    result = execute_command.invoke({"command": test_command})
    print(result)
