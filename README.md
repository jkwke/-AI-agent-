此Agent基于 LangChain 和 DeepSeek API 构建的智能助手，通过自然语言指令执行文件操作（创建、删除、读取、写入等）目前只支持这些功能，可扩展，支持流式对话

使用前在.env中配置你的DeepSeek API

后续扩展功能可将功能脚本放置在tools文件夹里，并修改__init__.py，Agent即可使用
