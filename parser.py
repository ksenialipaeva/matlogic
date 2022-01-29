class Lexeme ():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.id = -1


class LexemeBuffer():
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.pos = 0
        self.len = len(lexemes)

    def next(self):
        self.pos += 1
        return self.lexemes[self.pos]

    def back(self):
        self.pos -= 1

    def getPos(self):
        return self.pos

    def getLen(self):
        return self.len


def lexAnalyze(text):
    lex_list = []
    pos = 0
    text = text + "#"
    while text[pos] != "#":
        c = text[pos]
        if c == "(":
            lex_list.append(Lexeme("OPEN_BR", c))
            pos += 1
        elif c == ")":
            lex_list.append(Lexeme("CLOSE_BR", c))
            pos += 1
        elif c == "|":
            lex_list.append(Lexeme("DIS", c))
            pos += 1
        elif c == "&":
            lex_list.append(Lexeme("CON", c))
            pos += 1
        elif c == "!":
            lex_list.append(Lexeme("NEG", c))
            pos += 1
        elif c == "-" and text[pos+1] == ">":
            lex_list.append(Lexeme("IMP", text[pos:pos+2]))
            pos += 2
        elif c == " ":
            pos += 1
        else:
            pos2 = pos
            while text[pos2] not in " -!&|()#":
                pos2 += 1
            lex_list.append(Lexeme("VAR", text[pos:pos2]))
            pos = pos2
    return lex_list


def expr(Buffer):
    if Buffer.getPos() >= Buffer.getLen():
        return 0;
    else:
        Buffer.back()
        a = imp(Buffer)
        return a


def imp(Buffer):
    value = dij(Buffer)
    if Buffer.pos < Buffer.len - 1:
        lexeme = Buffer.next()
        if lexeme.value == "->":
            a = factor(Buffer)
            return (not(value) or a)
        else:
            Buffer.back()
            return value
    else:
        return value


def dij(Buffer):
    value = con(Buffer)
    if Buffer.pos < Buffer.len - 1:
        lexeme = Buffer.next()
        if lexeme.value == "|":
            return value or factor(Buffer)
        else:
            Buffer.back()
            return value
    else:
        return value


def con(Buffer):
    value = factor(Buffer)
    if Buffer.pos < Buffer.len - 1:
        lexeme = Buffer.next()
        if lexeme.value == "&":
            a = factor(Buffer)
            return value and a
        else:
            Buffer.back()
            return value
    else:
        return value


def factor(Buffer):
    lexeme = Buffer.next()
    if lexeme.type == "NEG":
        value = factor(Buffer)
        return not(value)
    elif lexeme.type == "VAR":
        return lexeme.value
    elif lexeme.type == "OPEN_BR":
        lexeme = Buffer.next()
        value = expr(Buffer)
        lexeme = Buffer.next()
        return value


def list_bin(x, r):
    x = str(x)
    while len(x) < r:
        x = '0' + x
    return x


variable = []
expression_text = "!(!A&B)"
lex_list = lexAnalyze(expression_text)
Buffer = LexemeBuffer(lex_list)
k = 0
for item in Buffer.lexemes:
    if item.type == "VAR":
        if item.value not in variable:
            variable.append(item.value)
            item.id = k
            k+=1
        else:
            item.id = variable.index(item.value)

variation = 2 ** k
list_var = []
for i in range(0, variation):
    list_var.append(list_bin(bin(i)[2:], k))
    i += 1
true_var = 0
false_var = 0

for item in list_var:
    for lex in Buffer.lexemes:
        if lex.type == "VAR":
            if item[lex.id] == "0":
                lex.value = False
            else:
                lex.value = True
    Buffer.pos = 0
    result = expr(Buffer)
    #print("item:", item, "result:", result)
    if result:
        true_var += 1
    else:
        false_var += 1

if true_var == 0:
    print("Unsatisfiable")
elif false_var == 0:
    print("Valid")
else:
    print("Satisfiable and invalid,", true_var, "true and", false_var, "false cases")
