from onebot.fliters import Filter


class Regex(Filter):
    def __init__(self, content):
        content = content

    async def support(self, app, message: dict, context: dict) -> bool:
        if 'text' not in context:
            return False
        text = ''.join(context.get('text'))
        # TODO 消息过滤器待实现

