from typing import Optional
from symengine.lib.symengine_wrapper import sympify
from .type import Type, Finite
from utils import indent_string


class Program:
    children = ["initial", "loop_body"]

    def __init__(self, types, variables, initial, loop_guard, loop_body):
        self.typedefs = {}
        self.finite_variables = []
        self.add_types(types)
        self.variables = {sympify(v) for v in variables}
        self.symbols = set()
        self.initial = initial
        self.loop_guard = loop_guard
        self.loop_body = loop_body
        self.var_to_index = {}  # initialized by info transformer
        self.index_to_var = {}  # initialized by info transformer

    def add_type(self, t: Type):
        if t is not None:
            self.typedefs[t.variable] = t
        if isinstance(t, Finite) and t.variable not in self.finite_variables:
            self.finite_variables.append(t.variable)

    def add_types(self, ts: [Type]):
        for t in ts:
            self.add_type(t)

    def get_type(self, expression) -> Optional[Type]:
        return self.typedefs.get(expression)

    def __str__(self):
        typedefs = "\n".join([str(t) for t in self.typedefs.values()])
        initial = "\n".join([str(i) for i in self.initial])
        body = "\n".join([str(b) for b in self.loop_body])

        string = ""
        if self.typedefs:
            string = f"types\n{indent_string(typedefs, 4)}\nend\n"

        string += f"{initial}\nwhile {str(self.loop_guard)}:\n{indent_string(body, 4)}\nend"
        return string
