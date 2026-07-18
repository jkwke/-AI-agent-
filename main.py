from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk, ToolMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
import tools
import colorama
from colorama import Fore, Style

colorama.init()


class AIChatAssistant:
    def __init__(self):
        """初始化AI聊天助手"""
        load_dotenv()
        os.environ["DEEPSEEK_API_KEY"] = os.getenv("OPENAI_API_KEY")

        tool_have = []
        if hasattr(tools, '__all__'):
            for tool_name in tools.__all__:
                tool = getattr(tools, tool_name)
                tool_have.append(tool)
        else:
            print("警告：tools 模块未定义 __all__，无法自动加载工具。")

        self.agent = create_agent(
            model="deepseek-chat",
            tools=tool_have,
            system_prompt="你是一个文件管理助手。"
                          "对于任何涉及文件增删改查的操作，你必须调用相应的工具，严禁仅用文字回复‘已完成’。"
                          "如果工具执行失败，必须向用户报错。"
        )
        self.history = []

    def run(self):
        """运行聊天循环"""
        print("聊天已启动 (输入 'tc' 退出)...")
        while True:
            try:
                user_input = input(f"\n[{Fore.RED}用户{Style.RESET_ALL}]: ")
                if user_input.lower() == 'tc':
                    break

                self.history.append(HumanMessage(content=user_input))

                called_tool_flag = False
                # === 关键修复：使用 AIMessageChunk 的累加器 ===
                # 我们不直接存储 chunk，而是用一个变量来累积内容
                ai_chunks_accumulator = AIMessageChunk(content="")
                tool_messages = []

                # 流式输出处理
                for chunk in self.agent.stream(
                        {"messages": self.history},
                        stream_mode="messages",
                ):
                    if isinstance(chunk, tuple):
                        msg, metadata = chunk
                    else:
                        msg = chunk

                    # 处理 AI 文本输出 或 工具调用指令碎片
                    if isinstance(msg, AIMessageChunk):
                        # 打印内容
                        if msg.content:
                            print(msg.content, end="", flush=True)

                        # 【核心修复】累加 chunk，而不是直接存储
                        # 这会将所有的文本片段和 tool_call 片段合并成一个完整的对象
                        ai_chunks_accumulator += msg

                        if msg.tool_call_chunks:
                            called_tool_flag = True

                    # 处理工具返回结果
                    elif isinstance(msg, ToolMessage):
                        called_tool_flag = True
                        print(f"\n{Fore.YELLOW}[系统: 正在调用工具 {msg.name}...]{Style.RESET_ALL}", flush=True)
                        tool_messages.append(msg)

                print("", flush=True)

                # === 更新对话历史 (序列化安全版) ===

                # 1. 处理 AI 的输出（合并后的完整消息）
                # 将累加器转换为一个完整的 AIMessage
                # 修复：AIMessageChunk 没有 to_dict() 方法，使用内容和工具调用来构建 AIMessage
                full_ai_message = AIMessage(
                    content=str(ai_chunks_accumulator.content),
                    tool_calls=getattr(ai_chunks_accumulator, 'tool_calls', [])
                )

                # 只有当 AI 真的有内容时（说了话或者调了工具），才加入历史
                if full_ai_message.content or full_ai_message.tool_calls:
                    self.history.append(full_ai_message)

                # 2. 处理工具调用结果
                # 必须放在 AIMessage 之后，因为是对 AI 工具调用的响应
                if tool_messages:
                    self.history.extend(tool_messages)

                # 3. 幻觉检测 (防止偷懒)
                action_keywords = ["创建", "删除", "写入", "查看", "列出", "打开"]
                success_keywords = ["成功", "已完成", "已创建", "已删除", "完毕", "好了"]
                needs_fix = False

                if not called_tool_flag:
                    full_text_content = ai_chunks_accumulator.content
                    has_action = any(k in user_input for k in action_keywords)
                    has_success = any(k in full_text_content for k in success_keywords)
                    if has_action and has_success:
                        needs_fix = True

                if needs_fix:
                    print(f"\n{Fore.RED}[系统警告: 检测到模型口头答应但未实际执行，正在强制纠正...]{Style.RESET_ALL}")

                    # 移除最后一条虚假的 AI 消息
                    if self.history and isinstance(self.history[-1], AIMessage):
                        self.history.pop()

                    fix_instruction = "请严格使用工具执行刚才的操作，不要仅用文字描述结果。"
                    self.history.append(HumanMessage(content=fix_instruction))
                    print(f"\n[{Fore.GREEN}助手{Style.RESET_ALL}]: 收到，正在重新实际调用工具...")

            except Exception as e:
                print(f"\n[系统错误]: {e}")
                if self.history and isinstance(self.history[-1], HumanMessage):
                    self.history.pop()
                continue

        print("\n对话结束。")


if __name__ == "__main__":
    try:
        assistant = AIChatAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print(f"\n结束对话")
