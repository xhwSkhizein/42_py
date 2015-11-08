#! -*- coding:utf8 -*-
# 实体类id加密解密
#

import base64

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton(*args):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class EntityIdHelper(object):
    def __init__(self, s=None):
        # FIXME 使用确定的字符串进行加盐其实效果不好，需要替换成更安全的方式
        self.salt_map                 = {}
        self.salt_map['User']         = "d41d8cd98f00b204e"
        self.salt_map['UserPassport'] = "bdb83783e924afbe7"
        self.salt_map['Ticket']       = "0998ecf8427e"

    def encode(self, id, cls):
        return base64.b64encode(self.get_salt(cls) + str(id))

    def decode(self, id, cls):
        real_id_with_salt = base64.b64decode(id)
        return real_id_with_salt.replace(self.get_salt(cls), "", 1)

    def get_salt(self, cls):
        return self.salt_map[cls]

if __name__ == '__main__':
    helper = EntityIdHelper()
    encrypt = helper.encode(1, "User")
    print encrypt
    print helper.decode(encrypt, "User")
