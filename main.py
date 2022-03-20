import requests
import itchat

KEY = '9c8df86f6e66293cd425b0ce52bd45c2'


def get_response(msg):
    # 这里实现与图灵机器人的交互
    # 构造了要发送给服务器的数据
    apiUrl = 'https://api.ownthink.com/bot'
    data = {
        'appid': KEY,
        'spoken': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r['data']['info']['text']
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except Exception as e:
        print(e)
        # 将会返回一个None
        return


# 这里实现微信消息的获取
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply


# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
