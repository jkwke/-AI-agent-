import requests
from langchain.tools import tool

# 开发者信息
ID = "10019141"
KEY = "193d053e0c55f6512b33b9ba686ea9a6"

# 天气接口（用能用的地址）
url = "http://81.68.85.14/api/tianqi/tqyb.php"

@tool
def get_weather(place: str) -> str:
    """
    获取指定城市的天气信息
    
    Args:
        place: 城市名称
        
    Returns:
        str: 格式化的天气信息
    """
    params = {
        "id": ID,
        "key": KEY,
        "place": place,
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.encoding = "utf-8"
        data = response.json()

        if data.get("code") == 200:
            weather_info = f"城市: {data.get('name', '未知')}\n"
            weather_info += f"天气: {data.get('weather1', '未知')}\n"
            weather_info += f"温度: {data.get('wd1', '未知')}°C / {data.get('wd2', '未知')}°C\n"
            weather_info += f"风向: {data.get('winddirection1', '未知')}\n"
            weather_info += f"风力: {data.get('windleve1', '未知')}\n"
            weather_info += f"更新时间: {data.get('uptime', '未知')}\n"

            # 如果有实时数据
            now = data.get('nowinfo', {})
            if now:
                weather_info += f"\n实时温度: {now.get('temperature', '未知')}°C\n"
                weather_info += f"实时湿度: {now.get('humidity', '未知')}%\n"
                weather_info += f"体感温度: {now.get('feelst', '未知')}°C\n"
                
            return weather_info
        else:
            return f"查询失败: {data.get('msg', '未知错误')}"

    except Exception as e:
        return f"请求出错: {e}"

# 保持原有的测试代码作为示例
if __name__ == "__main__":
    # 测试函数
    result = get_weather.invoke({"place": "西安"})
    print(result)
