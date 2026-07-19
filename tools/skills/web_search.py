from langchain.tools import tool
import os
from tavily import TavilyClient


@tool
def web_search(query: str) -> str:
    """
    使用 Tavily 搜索引擎进行网络搜索，返回相关信息

    Args:
        query: 搜索查询字符串

    Returns:
        str: 搜索结果摘要
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误：未找到 Tavily API 密钥，请在 .env 文件中设置 TAVILY_API_KEY"

    client = TavilyClient(api_key=api_key)

    try:
        # 执行搜索
        response = client.search(
            query=query,
            search_depth="advanced",  # 或 "basic"
            max_results=5,
            include_answer=True,
            include_sources=True
        )

        # 格式化结果
        result = f"搜索查询: {query}\n\n"

        if response.get('answer'):
            result += f"答案摘要: {response['answer']}\n\n"

        result += "搜索结果:\n"
        for i, item in enumerate(response.get('results', []), 1):
            result += f"{i}. {item['title']}\n"
            result += f"   链接: {item['url']}\n"
            result += f"   内容: {item['content'][:200]}...\n\n"

        return result.strip()
    except Exception as e:
        return f"搜索过程中发生错误: {str(e)}"
