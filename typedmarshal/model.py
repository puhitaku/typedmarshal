import json, io
from collections import OrderedDict
from typing import get_type_hints
from typing import List, Dict, Tuple, TypeVar, Any, Union, Optional

TypeLike = TypeVar('TypeLike')


class TypeCheckError(TypeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MarshalModel:
    _attrs = None
    _attr_tree = None
    _obj = None
    _iterable = False
    _objs = []

    def __init__(self):
        self._attrs, self._attr_tree = self._create_attr_info(self)

    def __iter__(self):
        if not self._iterable:
            raise Exception('Not iterable; load multi-item structure first')
        return self

    def __next__(self):
        if not self._iterable or len(self._objs) < 1:
            raise Exception('Not iterable; load multi-item structure firsts')

        for i in self._objs:
            self._unmarshal(self, self._attr_tree, i)
            yield self

    @classmethod
    def _create_attr_info(cls, obj):
        if isinstance(obj, type):
            ins = obj()
        else:
            ins = obj
        attrs = [a for a, v in ins.__class__.__dict__.items() if not a.startswith('_') and not isinstance(v, type)]
        annot = get_type_hints(ins)
        attr_dict = OrderedDict((k, annot.get(k, None)) for k in attrs)
        attr_tree = cls._convert_annot_type_tree(attr_dict)
        return attr_dict, attr_tree

    @staticmethod
    def _is_builtin(typ) -> bool:
        if isinstance(typ, type):
            return typ.__name__ in __builtins__
        else:
            return typ.__class__.__name__ in __builtins__

    @staticmethod
    def _has_public_attribute(typ) -> bool:
        if isinstance(typ, type):
            return len([x for x in typ.__dict__ if not x.startswith('_')]) > 0
        else:
            return len([x for x in typ.__class__.__dict__ if not x.startswith('_')]) > 0

    @staticmethod
    def _get_attribute_list(typ) -> List[str]:
        return [x for x in typ.__dict__ if not x.startswith('__')]

    @staticmethod
    def _is_generic(typ) -> bool:
        """Identify attr type: builtin or derived from Generic class"""
        # return Generic in a.__mro__  # Derived from Generic
        return hasattr(typ, '__origin__')

    @staticmethod
    def _is_any_option_union(typ) -> bool:
        """Identify attr type: Any, Union (Optional) or else"""
        if hasattr(typ, '__origin__'):
            return typ.__origin__ is Union or typ is Union
        else:
            return any(typ is t for t in [Any, Union, Optional])

    @classmethod
    def _get_root(cls, typ):
        if cls._is_any_option_union(typ):
            if hasattr(typ, '__origin__'):
                if typ is Union:
                    return Union
                return typ.__origin__
            else:
                return typ
        elif cls._is_generic(typ):
            if typ.__origin__ is None:
                return typ
            else:
                return typ.__origin__
        else:
            return typ

    @staticmethod
    def _has_nested_type(typ) -> bool:
        return typ.__origin__ is not None

    @classmethod
    def _tree_recursive(cls, typ) -> Union[Tuple[TypeLike, ...], Dict[str, Tuple]]:
        if cls._is_generic(typ) and cls._has_nested_type(typ):
            return (typ.__origin__,) + tuple(cls._tree_recursive(t) for t in typ.__args__)
        elif not cls._is_builtin(typ) and cls._has_public_attribute(typ):
            _, tree = cls._create_attr_info(typ)
            return tree, typ
        else:
            return typ,

    @classmethod
    def _convert_annot_type_tree(cls, annots) -> Dict[str, Tuple]:
        attr_tree = OrderedDict()
        for key, typ in annots.items():
            if typ is None:
                attr_tree[key] = None
            else:
                attr_tree[key] = cls._tree_recursive(typ)
        return attr_tree

    def _unmarshal_with_type_check(self, attr, typ: Tuple[TypeLike]) -> Any:
        err = TypeCheckError('Type of value is different than annotated type.')

        if self._is_any_option_union(typ[0]):
            if self._get_root(typ[0]) is Any:
                return attr

            elif self._get_root(typ[0]) is Union:
                # This case is only for Optional type.
                # De-serialized data structures don't preserve type definition,
                # so unmarshaller doesn't check type strictly for now.

                if any(not self._is_builtin(t) for t in typ[1:]):
                    raise TypeCheckError('Unmarshaller does not support arbitrary Union. Primitive builtin types only.')

                if attr is None:
                    return None
                else:
                    if any(isinstance(attr, t) for t in typ[1:]):
                        return attr
                    else:
                        raise err

            elif self._get_root(typ[0]) is Optional:
                # Plain Optional means there's no more type info.
                # Unmarshaller checks nothing more.
                return attr

        elif self._is_generic(typ[0]):
            if typ[0] is Dict:
                if not isinstance(attr, dict):
                    raise err

                if not len(typ) > 1:  # Further type annotation is not available
                    return attr

                dict_items = OrderedDict()
                for k, v in attr.items():
                    if not isinstance(k, typ[1]):
                        raise err
                    else:
                        dict_items[k] = self._unmarshal_with_type_check(v, typ[2])
                return dict_items

            elif typ[0] is List:
                if not isinstance(attr, list):
                    raise err

                if not len(typ) > 1:  # Has nested type annotation
                    return attr

                list_items = []
                for i in attr:
                    list_items.append(self._unmarshal_with_type_check(i, typ[1]))
                return list_items

            elif typ[0] is Tuple:
                if not isinstance(attr, tuple):
                    raise err

                if not len(typ) > 1:
                    return attr

                if not len(typ[1:]) == len(attr):
                    raise TypeCheckError('Length of type list and tuple are different.')

                tuple_items = []
                for i, v in enumerate(attr):
                    tuple_items.append(self._unmarshal_with_type_check(attr[i], typ[i + 1]))
                return tuple(tuple_items)

        elif isinstance(typ[0], OrderedDict):
            new_attr_tree = typ[0]
            new_target = typ[1]()
            self._unmarshal(new_target, new_attr_tree, attr)
            return new_target

        else:
            if not isinstance(attr, typ[0]):
                raise err
            return attr

    def _unmarshal(self, target, target_attr_tree, item):
        for key, typ in target_attr_tree.items():
            if typ is None:
                setattr(target, key, item.get(key, None))
            else:
                setattr(target, key, self._unmarshal_with_type_check(item.get(key, None), typ))

    def load_json(self, json_in: Union[str, io.IOBase], lines=False, **kwargs):
        if isinstance(json_in, str):
            obj = json.loads(json_in, **kwargs)
        elif isinstance(json_in, io.IOBase):
            obj = json.load(json_in, **kwargs)
        else:
            raise TypeError('String or IO class instance must be passed.')

        if not isinstance(obj, dict):
            raise TypeError('JSON\'s root must be a single object (dict).')

        if lines:
            self._objs.append(obj)
        else:
            self._raw = obj
            self._unmarshal(self, self._attr_tree, self._raw)

    def load_json_lines(self, json_in: Union[str, List[str], io.IOBase], **kwargs):
        self._iterable = True

        if isinstance(json_in, str):
            lines = json_in.split('\n')
        elif isinstance(json_in, list):
            lines = json_in
        elif isinstance(json_in, io.IOBase):
            lines = json_in.readlines()
        else:
            t = '{}'.format(Union[str, List[str], io.IOBase]).replace('typing.', '')
            raise TypeError(f'json_in must be {t}')

        for l in lines:
            self.load_json(l, lines=True, **kwargs)
