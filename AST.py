ids = {}


def add_id(new_id):
    if new_id in ids.keys():
        print(f'There alredy is {new_id}.')
        raise ValueError
    else:
        ids[new_id] = None


def change_value(the_id, value):
    ids[the_id] = value


class Node(object):
    def __init__(self, type, children=None, leaf=None):
        self.score = None
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        super().__init__(self.__class__, [left, right], operator)
        self.left = left
        self.operator = operator
        self.right = right
        self.check_type_identity()
        self.calculate()

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)

    def calculate(self):
        if self.operator == "+":
            self.score = self.left.primitive + self.right.primitive
        elif self.operator == "-":
            self.score = self.left.primitive - self.right.primitive
        elif self.operator == "/":
            self.score = self.left.primitive / self.right.primitive
        elif self.operator == "*":
            self.score = self.left.primitive * self.right.primitive

    def check_type_identity(self):
        if not (type(self.left.primitive) == type(self.right.primitive)):
            print(f'Types of {self.left.primitive} and {self.right.primitive} are different')
            raise

class UnaryExpression(Node):
    def __init__(self, operator, operand, left=True):
        super().__init__(self.__class__, [operand], operator)
        self.operator = operator
        self.operand = operand
        self.left = left

    def __repr__(self):
        order = [self.operator, self.operand] if self.left else [self.operand, self.operator]
        return '{}{}'.format(*order)


class Negation(UnaryExpression):
    def __init__(self, operand):
        super().__init__('-', operand)
        self.calculate()

    def calculate(self):
        self.score = self.operand * (-1)


class Assignment(Node):
    def __init__(self, left, operator, right):
        super().__init__(self.__class__, [left, right], operator)
        self.left = left
        self.operator = operator
        self.right = right
        self.score = right.score
        self.check_type_identity()
        ids[self.left.name] = self.right.score

    def check_type_identity(self):
        if getattr(self.left, 'primitive', None):
            if not (type(self.left.primitive) == type(self.right.score)):
                print(f'Types of {type(self.left.primitive)} and {type(self.right.score)} are different')
                raise
        else:
            if not (self.left.var_type in str(type(self.right.score))):
                print(f'Types of {self.left.var_type} and {str(type(self.right.score))} are different')
                raise


class Variable(Node):
    def __init__(self, name):
        super().__init__(self.__class__, [], name)
        self.name = str(name)
        if name not in ids.keys():
            print(f'No {name} in dict')
            raise ValueError
        self.primitive = ids[self.name]

    def __repr__(self):
        return '{}'.format(self.name)


class Initialization(Node):
    def __init__(self, name, var_type):
        super().__init__(self.__class__, [], name)
        self.name = name
        self.var_type = var_type
        add_id(name)

    def __repr__(self):
        return '{}'.format(self.name)


class If(Node):
    def __init__(self, condition, expression, else_expression=None):
        super().__init__(self.__class__, [condition, expression, else_expression], ["IF", "THEN", "ELSE"])
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression
        if else_expression == None:
            self.children = self.children[:-1]
            self.leaf = self.leaf[:-1]
        self.calculate()

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result

    def calculate(self):
        if self.condition:
            self.score = self.expression
        else:
            self.score = self.else_expression


class While(Node):
    def __init__(self, condition, body):
        super().__init__(self.__class__, [condition, body], "WHILE")
        self.condition = condition
        self.body = body
        self.calculate()

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)

    def calculate(self):
        while self.condition:
            self.score = self.body.score


class Range(Node):
    def __init__(self, start, end, step=1):
        super().__init__(self.__class__, [start, end, step], "RANGE")
        if step == 1: self.children = self.children[:-1]
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For(Node):
    def __init__(self, id, range, body):
        super().__init__(self.__class__, [id, range, body], "FOR")
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class Break(Node):
    def __init__(self):
        super().__init__(self.__class__, [], "BREAK")

    def __repr__(self):
        return 'BREAK'


class Continue(Node):
    def __init__(self):
        super().__init__(self.__class__, [], "CONTINUE")

    def __repr__(self):
        return 'CONTINUE'


class Return(Node):
    def __init__(self, result):
        super().__init__(self.__class__, [result], "RETURN")
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print(Node):
    def __init__(self, expression):
        super().__init__(self.__class__, [expression], "PRINT")
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)

class Error(Node):
    pass


class Block(Node):
    def __init__(self, instruction):
        super().__init__(self.__class__, [instruction])
        self.instructions = self.children
        self.score = self.instructions[0].score

    def __repr__(self):
        return "{\n" + "\n".join(map(str, self.instructions)) + "\n}"


class Program(Node):
    def __init__(self, program):
        super().__init__(self.__class__, [program])
        self.program = program
        self.score = program.score

    def __repr__(self):
        return str(self.program)


class Instruction(Node):
    def __init__(self, line):
        super().__init__(self.__class__, [line])
        self.line = line
        self.score = self.line.score

    def __repr__(self):
        return str(self.line)


class Value(Node):
    def __init__(self, primitive):
        super().__init__(self.__class__, [], primitive)
        self.primitive = primitive

    def __repr__(self):
        return "{}({})".format(type(self.primitive).__name__, self.primitive)


class Rows(Node):
    def __init__(self, sequence):
        super().__init__(self.__class__, [sequence])
        self.row_list = self.children

    def __repr__(self):
        return "[" + ", ".join(map(str, self.row_list)) + "]"

    def __len__(self):
        return len(self.row_list)

    def __getitem__(self, item):
        return self.row_list[item]


class Sequence(Node):
    def __init__(self, expression):
        super().__init__(self.__class__, [expression], "SEQ")
        self.expressions = self.children

    def __repr__(self):
        return "{}".format(self.expressions)

    def __len__(self):
        return len(self.expressions)

    def __getitem__(self, item):
        return self.expressions[item]