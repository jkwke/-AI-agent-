import datetime
from langchain.tools import tool


@tool
def get_time() -> str:
    """
    获取当前的日期和时间信息

    Returns:
        str: 格式化的当前日期和时间
    """
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
    day_of_week = now.strftime("%A")

    time_info = f"当前时间: {formatted_time}\n"
    time_info += f"星期: {day_of_week}\n"

    return time_info


# 测试代码
if __name__ == "__main__":
    # 测试函数
    result = get_time.invoke({})
    print(result)
