from pyco_types._common import CommonException, G_Symbol_UNSET


class CoExtBase():
    def __new__(cls, *args, _extra_kws=None, **kwargs):
        self = super().__new__(cls)
        self._kwargs = kwargs
        self._args = args
        if isinstance(_extra_kws, dict):
            self._extra_kws = _extra_kws
        else:
            self._extra_kws = {}
        return self

    def __init__(self, *args, _extra_kws=None, **kwargs):
        self._args = args
        self._kwargs = kwargs
        if isinstance(_extra_kws, dict):
            self._extra_kws = _extra_kws
        else:
            self._extra_kws = {}


    def __str__(self):
        tp = self.__class__.__name__
        return f"<{tp}:args={self._args},kwargs={self._kwargs}," \
               f"extra_kws={self._extra_kws}>"

    def __call__(self, kwargs: dict):
        self._kwargs.update(kwargs)
        return self

    def __repr__(self):
        tp = self.__class__.__name__
        # args = (*self._args, f"**{self._kwargs}", f"_extra_kws={self._extra_kws}")
        return f"<{tp}{self._args}({self._kwargs})>"

    def to_dict(self, verbose=0):
        ##;  注意不要修改 kwargs
        if verbose <= 1:
            return self._kwargs
        elif verbose == 2:
            return dict(
                self._kwargs,
                _args=self._args
            )
        else:
            return dict(
                self._kwargs,
                _args=self._args,
                _extra_kws=self._extra_kws
            )

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._args[key]
        elif key == "_args":
            return self._args
        v = self._kwargs.get(key, G_Symbol_UNSET)
        if v is G_Symbol_UNSET:
            v = self._extra_kws.get(key, G_Symbol_UNSET)
            if v is G_Symbol_UNSET:
                raise Exception(f"Invalid $key={key}")
        return v

    def __getattr__(self, item):
        ##; 先调用 __getattribute__，然后因为属性不存在调用 __getattr__
        try:
            return self[item]
        except Exception as e:
            raise CommonException(
                f"<{self.__class__.__name__}>.getattr({item}) failed! ({self})",
                errno=40042,
                origin_data=self,
            )

    def __eq__(self, other):
        if self._args == other._args:
            if self._kwargs == other._kwargs:
                return True
        return False


def DecoExtKwsClass(cls):
    """
    @DecoExtKwsClass
    class MyClass():
        pass    
    """
    base_class = CoExtBase
    class_name = f'PycoWrapped.{cls.__name__}'

    WrappedClass = type(
        class_name, (cls, base_class),
        {
            '__init__':
                lambda self, *args, **kwargs: (
                    base_class.__init__(self, *args, **kwargs)
                    if hasattr(base_class, '__init__'
                               ) else None and cls.__init__(
                        self, *args, **kwargs
                    ) if hasattr(cls, '__init__') else None
                )
        }
    )

    return WrappedClass
