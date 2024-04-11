import logging
日志 = logging.getLogger()

_var = None     # 待绑定
cowork = None   # 待绑定


_端口定义 = {}
#_套子 = None


def 尝试从文件载入端口定义():
    import os, json
    global _端口定义
    if os.path.exists(_var.端口定义文件路径):
        try:
            with open(_var.端口定义文件路径, 'rt') as fp:
                _端口定义 =  json.load(fp)
        except:
            pass
    return _端口定义


def 保存端口定义文件():
    import os, json
    global _端口定义
    try:
        with open(_var.端口定义文件路径, 'wt') as fp:
            json.dump(_端口定义 ,fp)
    except:
        pass


import socket
def 检查端口是否可以绑定(端口):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as 套子:
            套子.bind(('localhost', 端口))
    except Exception as e:
        日志.warning(f"{端口}:{e}")
        return False
    return True


def 从给定端口开始查找可用的端口(第一个端口, 最大尝试次数=10):
    for 增量 in range(最大尝试次数):
        if 检查端口是否可以绑定(第一个端口+增量):
            return 第一个端口+增量
    return None


def 根据名称分配端口(端口名称):
    global _端口定义
    assert type(端口名称) is str and len(端口名称)>0
    if 端口名称 in _端口定义:
        return _端口定义[端口名称], '客户端', None
    可用端口 = 从给定端口开始查找可用的端口(max(_var.分配起始端口, max(_端口定义.values())+1 if len(_端口定义)>0 else -1))
    if 可用端口 is not None:
        _端口定义[端口名称] = 可用端口
        保存端口定义文件()
        return 可用端口, '服务端', None
    return None, None, None

