import json
import uuid
# import inspect
from pprint import pformat
from datetime import datetime
from logging import root as logger
from pyco_types._convert_meta import find_converter, Converter
from pyco_types._common import K_Python_Common_Types, CommonException


def pformat_any(data, depth=2, width=80, indent=2, **kwargs):
    return " :: ".join([str(type(data)), pformat(data, indent=indent, width=width, depth=depth)])


def parse_json(data, **kwargs):
    if isinstance(data, str) and data.startswith('"') and data.endswith('"'):
        try:
            obj = json.loads(data, **kwargs)
            return obj
        except:
            ## import json5
            return data
    else:
        return data


class CustomJSONEncoder(json.JSONEncoder):
    """
    default support datetime.datetime and uuid.UUID
    enable convert object by custom `http exception`
    usually:
        "to_json":  Common Class
        "to_dict":  Custom Model
        "as_dict"： SQLAlchemy Rows
        "get_json": json response
        "__html__": jinja templates

    """
    _jsonify_methods = [
        "jsonify",
        "to_json",
        "get_json",  # json response
        "to_dict",
        "as_dict",  # SQLAlchemy Rows
        "__html__",  # jinja templates
        "_asdict",  ## collections, namedtuple 
        "toJson",
        "getJson",  # json response
        "toDict",
        "asDict",  # SQLAlchemy Rows
    ]

    ##； @_jsonify_strict: 如果设置为 True, 则尝试使用原生 JSON, 可能会异常
    ##； @_jsonify_strict: 如果设置为 False, 则不管怎样都能返回 序列化的结果（不一定符合预期）
    _custom_kwargs = dict(
        datetime_fmt='%Y-%m-%d %H:%M:%S',
        jsonify_methods=_jsonify_methods,
    )
    _jsonify_strict = False
    _pformat_depth = 2
    _datetime_fmt = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def stringify_with_converter(cls, obj):
        cvt = find_converter(obj)
        if cvt is None:
            return False, pformat_any(obj, depth=cls._pformat_depth)
        else:
            return True, cvt.stringify(obj)

    @classmethod
    def serialize(cls, obj, strict=False, with_converter=True, **kwargs):
        ##; common types
        datetime_fmt = kwargs.pop("datetime_fmt", cls._datetime_fmt)
        if isinstance(obj, datetime):
            # default use TZ-LOCAL, eg: "2021-03-22 20:32:02.271068+08:00"
            return obj.strftime(datetime_fmt)
        elif isinstance(obj, uuid.UUID):
            return str(obj)

        ##; stringify with instance
        for k in cls._jsonify_methods:
            fn = getattr(obj, k, None)  ## instance_method
            if callable(fn):
                return fn()
            elif isinstance(fn, K_Python_Common_Types):
                return fn

        ##; stringify_with_converter
        if with_converter:
            flag, txt = cls.stringify_with_converter(obj)
            if flag:
                return txt
            elif not strict:
                return txt

        raise CommonException(
            f"Object({type(obj)}) is not serializable. \nobj:{obj}",
            errno=50020,
            origin=obj,
            with_converter=with_converter,
        )

    def default(self, obj):
        return self.serialize(obj, strict=True)


def json_format(data, indent=2, autoflat=True, cls=CustomJSONEncoder, ensure_ascii=False, **kwargs):
    if isinstance(data, str) and autoflat:
        data = parse_json(data)
    return json.dumps(
        data, indent=indent,
        cls=cls, ensure_ascii=ensure_ascii, **kwargs
    )


##; json_stringify 总能返回字符串结果, 不会抛出 TypeError
json_stringify = lambda obj: json.dumps(obj, indent=2, default=CustomJSONEncoder.serialize)
