import logging
logger = logging.getLogger()
from common import PType, 参数, 暗号, 端口字段类
import socket




class Server:

    def __init__(我):#, PType, 参数, 暗号, 端口字段类):
        我.参数, 我.暗号, 我.PType, 我.端口字段类 = 参数, 暗号, PType, 端口字段类
        我.端口定义 = 我.从文件获取端口定义() if 参数.保存端口定义到文件 else {}
        我.服务 = None


    def 从文件获取端口定义(我):
        import os, json
        if os.path.exists(我.参数.端口定义文件路径):
        try:日志
            with open(我.参数.端口定义文件路径, 'rt') as fp:
                端口定义 =  json.load(fp)
            return 端口定义
        except:
            pass
        return {}


    def 保存端口定义文件(我):
        import os, json
        try:
            with open(我.参数.端口定义文件路径, 'wt') as fp:
                json.dump(我.端口定义 ,fp)
        except:
            pass



from threading import Thread
class 服务子类(Thread):

    def __init__(我, 连接, 端口定义, PType, 参数, 暗号, 端口字段类):
        我.参数, 我.暗号, 我.PType, 我.端口字段类 = 参数, 暗号, PType, 端口字段类
        我.连接 = 连接
        我.端口定义 = 端口定义


    def 握手(我):
        assert 我.连接 is not None
        连接.send(我.暗号.我是客户端)
        assert 连接.recv() == 我.暗号.我是服务端()
        我.连接 = 连接
        return True

    def 分配端口(我, 请求段):
        #assert isinstance(接收段, 我.端口字段类)
        if 请求段.类型 == 我.PType.p2p
        # todo


    def run(我): # 仅处理一次请求
        try:
            我._握手()
        except Exception as e:
            logger.error(e)
            我.连接.close()
            return False
        请求段 = 我.连接.recv()
        try:
            assert isinstance(请求段, 我.端口字段类)
            logger.error(f'请求 {请求段} 非法')
            回复段 = 我.分配端口(请求段)
            assert isinstance(回复段, 我.端口字段类)
            我.连接.send(回复段)
        except:
            pass
        finally:
            我.连接.close()



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

