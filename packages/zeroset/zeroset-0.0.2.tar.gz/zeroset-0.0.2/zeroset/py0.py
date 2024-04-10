# py basic advanced util functions
import os, sys
import inspect
import numpy as np
from tabulate import tabulate


def print0(*args, print_type="table"):
    def parse_dict(name, d):
        ret = []
        for k, v in d.items():
            ret.append([f'{name}["{k}"]', v])
        return ret

    variable_names = []  # variable name, value,
    for k, v in inspect.currentframe().f_back.f_locals.items():
        variable_names.append([k, v])
        if isinstance(v, dict):
            variable_names += [e for e in parse_dict(k, v)]
    table = []
    for arg in args:
        # variable_name = [k for k, v in inspect.currentframe().f_back.f_locals.items() if v is arg]
        variable_name = [e[0] for e in variable_names if e[1] is arg]
        variable_name = variable_name[-1] if len(variable_name) > 0 else "CONSTANT"
        # if isinstance(arg, np.ndarray):
        #     print(f'{variable_name} (type={type(arg).__name__},shape={arg.shape})\n{arg}')
        # else:
        #     print(f'{variable_name} (type={type(arg).__name__}): {arg}')
        if isinstance(arg, np.ndarray):
            typename = f'{type(arg).__name__}\n - shape: {arg.shape}'
            val = arg
        elif isinstance(arg, list):
            typename = f'{type(arg).__name__}\n - len: {len(arg)}'
            val = str(arg)
            line_length = 100
            val = "\n".join([val[i:i + line_length] for i in range(0, len(val), line_length)])
        else:
            typename = type(arg).__name__
            val = arg
        table.append([variable_name, typename, val])
    headers = ["Variable", "Type", "Value"]
    print(tabulate(table, headers=headers, tablefmt="simple_grid"))


if __name__ == '__main__':
    arr = np.random.random((2, 3))
    d = {
        "a": 1,
        "b": 2,
        "c": 3,
        "x": {
            "y": 777,
            "z": 888
        }
    }
    c = 666
    lst = [1, 2, 3] * 50
    lst2 = [[1, 2], [3, 4], [5, 6]] * 50
    print0(arr)
    print0(c)
    print0(d["a"])
    print0(d)
    print0(d["x"])

    print0(arr, c, d["b"], d)

    print0(lst2)
