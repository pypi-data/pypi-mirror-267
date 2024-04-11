import logging
日志 = logging.getLogger()

#from .server import *
from socketman.objsocket import OBJSocket
import _var, server, cowork
server._var = _var
server.cowork = cowork
from server import *
import os, socket



日志.warning(尝试从文件载入端口定义())

try:
    日志.info('正在初始化')
    套子 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    套子.bind(_var.获取服务绑定用地址())
    套子.listen(1)
    日志.info('正在处理接入端口')

    while True:
        连接, 地址 = 套子.accept()
        对象连接 = OBJSocket(连接)
        if cowork.握手({'连接':对象连接}).角色('乙方'):
            完成 = cowork.分配端口({'连接':对象连接, '根据名称分配端口':根据名称分配端口}).角色('乙方')
        对象连接.close()

except Exception as e:
    日志.error(e)
    exit(1)

finally:
    套子.close()
    if '对象连接' in locals():
        对象连接.close()

exit(0)
