# coding=utf8
import datetime
import time
from glob import glob
import json
from os.path import dirname, abspath, join
import sys
import unparse as unparse
import utils.toml
import utils.xmltodict
reload(sys)
sys.setdefaultencoding('utf-8')

if sys.version_info < (3,):
    _range = xrange
    iteritems = dict.iteritems
else:
    unicode = str
    _range = range
    basestring = str
    unichr = chr
    iteritems = dict.items
    long = int



def modifyDic(handle, value):
    d = {}
    for k, v in iteritems(value):
        # print handle[jump_to(v)]
        # v= v.decode("utf-8")
        state = jump_to(v)
        if (state == "dic"):
            d[k] = handle[state](handle, v)
        else:
            d[k] = handle[state](v)
    return d


def modifyList(value):
    a = []
    for v in value:
        a.append(v)
    try:
        a[0]
    except KeyError:
        return a
    except IndexError:
        pass
    return a


def ModifyStr(value):
    return value


def modifyBool(value):
    return str(value).lower()


def modifyInt(value):
    return str(value)


def modifyLong(value):
    return str(value)


def modifyFloat(value):
    return repr(value)


def modifyDate(value):
    sdate = value.strftime('%Y-%m-%dT%H:%M:%SZ')
    return sdate


def exit():
    sys.exit()


def jump_to(value):
    #状态工厂
    if isinstance(value, dict):
        return "dic"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, basestring):
        return "baseStr"
    elif isinstance(value, bool):
        return "bools"
    elif isinstance(value, int):
        return "ints"
    elif isinstance(value, long):
        return "longs"
    elif isinstance(value, float):
        return "floats"
    elif isinstance(value, datetime.datetime):
        return "dates"
    else:
        return "exit"


def scheduler(handle, value):
    val = jump_to(value)
    dicts=handle[val](handle, value)
    print json.dumps(dicts)#将字典转化为json
    dts={"dit":dicts}
    print utils.xmltodict.unparse(dts);#将字典转化为xml

if __name__ == '__main__':
    with open("tt.toml") as conffile:
        config = utils.toml.loads(conffile.read())
    #状态函数字典
    handle = {
        'dic': modifyDic,
        'list': modifyList,
        'baseStr': ModifyStr,
        'bools': modifyBool,
        'ints': modifyInt,
        'longs': modifyLong,
        'floats': modifyFloat,
        'dates': modifyDate,
        'exit': exit,
    }

    scheduler(handle, config)
