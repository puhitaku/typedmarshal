def pretty_print_recursive(obj, indent=0):
    def i_print(s):
        print(' ' * indent + s)

    if obj is None:
        i_print('None')
    elif isinstance(obj, (int, float, str)):
        i_print(f'{obj}')
    elif isinstance(obj, list):
        for l in obj:
            pretty_print_recursive(l, indent=indent+2)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            i_print(f'{k}: {repr(v)}')
    else:
        for k, v in obj.__dict__.items():
            if not k.startswith('_'):
                if v is None:
                    i_print(f'{k}: None')
                elif v.__class__.__name__ not in __builtins__:
                    i_print(f'{k}:')
                    pretty_print_recursive(v, indent=indent+2)
                elif isinstance(v, (list, dict)):
                    i_print(f'{k}:')
                    pretty_print_recursive(v, indent=indent)
                else:
                    i_print(f'{k}: {repr(v)}')
