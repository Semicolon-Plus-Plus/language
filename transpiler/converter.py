from lark import Lark, Transformer

class Converter(Transformer):
    #The transpiler only accepts these platforms at the moment
    allowedPlatforms = ["linux", "windows", "mac"]
    #
    
    grammar = r"""
    %import common.CNAME
    %import common.INT
    %import common.FLOAT
    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %import common.SIGNED_NUMBER
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %import common.NEWLINE
    %import common.LETTER
    %import common.DIGIT
    %import common.WS
    %ignore WS
    
    //Creating variables
    STRING: ESCAPED_STRING
    TYPE: CNAME
    arg_list: arg ("," arg)*
    arg: TYPE CNAME
    ?content: (balanced_paren | /[^()]+/)*
    balanced_paren: "(" content ")"
    code_content: (/[^{}<>]+/)*
    start: (normal_func | fast_func)+
    //
    
    //Statements
    ?statement: var_decl
        | return_decl
        | expr_stmt
        | block_scope
        | if_stmt_inline
        
    inline_statement: var_decl | return_decl | expr_stmt | if_stmt_inline
    inline_block: inline_statement+
    //
    
    //Expressions
    ?expr: expr "+" expr -> add
        | expr "-" expr -> sub
        | expr "*" expr -> mul
        | expr "/" expr -> div
        | expr "==" expr -> eq
        | expr "!=" expr -> neq
        | expr ">" expr -> gt
        | expr "<" expr -> lt
        | expr ">=" expr -> gtos
        | expr "<=" expr -> ltos
        | expr "||" expr -> or_
        | expr "&&" expr -> and_
        | SIGNED_NUMBER
        | CNAME
        | STRING
        | "(" expr ")" -> put_brackets
        | func_call
        
    arg_expr_list: expr ("," expr)*
    //
    
    //Declarators
    var_decl:  CNAME "@" TYPE "=" expr ";"
    return_decl: "die" expr ";"
    expr_stmt: expr ";"
    //
    
    //Scopes
    block_scope: "{" statement* "}"
    //
    
    //Functions
    normal_func: CNAME "=" "|" [arg_list] "|" "=>" block_scope "->" TYPE
    fast_func: CNAME "=" "|" [arg_list] "|" ":" inline_block "!"
    func_call: CNAME "(" [arg_expr_list] ")"
    //
    
    //Logic
    if_stmt_inline: "if" "(" expr ")" ":" inline_block ["else" ":" (if_stmt_inline | inline_block)] "!"
    //
    
    """
    
    
    #Start of def's for lark parsing
    def start(self, items): return '\n\n'.join(items)
    
    #Setters
    def normal_setter(self, items):
        type_, name, val = items
        return f"{ type_ } { name } = { val };\n"
    #
    
    #Creating variables
    def CNAME(self, token): return str(token)
    def SIGNED_NUMBER(self, token): return str(token)
    def STRING(self, token): return str(token)
    #
    
    #Statements
    def inline_statement(self, items):
        return items[0]
    
    def inline_block(self, items):
        def flatten(lst):
            for i in lst:
                if isinstance(i, list):
                    yield from flatten(i)
                else:
                    yield i
                    
        return "".join(flatten(items))
    #
    
    #Declarators
    def var_decl(self, items):
        type_, cname, expr = items
        return f"{ type_ } { cname } = { expr };\n"
    
    def return_decl(self, items):
        expr = items[0]
        return f"return { expr };\n"
    
    def expr_stmt(self, items):
        expr = items[0]
        return f"{ expr };\n"
    #
    
    #Scopes
    def block_scope(self, items):
        content = "".join(items)
        return f"{{\n{ content }}}\n"
    #
    
    #Expressions
    def expr(self, items):
        expr = items[0]
        return str(expr)
    
    @staticmethod
    def exprConv(items, sign):
        a, b = items
        return f"{ a } { sign } { b }"
    
    def add(self, items): return Converter.exprConv(items, "+")
    def sub(self, items): return Converter.exprConv(items, "-")
    def mul(self, items): return Converter.exprConv(items, "*")
    def div(self, items): return Converter.exprConv(items, "/")
    def eq(self, items): return Converter.exprConv(items, "==")
    def neq(self, items): return Converter.exprConv(items, "!=")
    def gt(self, items): return Converter.exprConv(items, ">")
    def lt(self, items): return Converter.exprConv(items, "<")
    def gtos(self, items): return Converter.exprConv(items, ">=")
    def ltos(self, items): return Converter.exprConv(items, "<=")
    def or_(self, items): return Converter.exprConv(items, "||")
    def and_(self, items): return Converter.exprConv(items, "&&")
    
    def arg_expr_list(self, items):
        return ", ".join(items)
    
    def put_brackets(self, items):
        return f"({ "".join(items) })"
    #
    
    #Creating variables
    def arg(self, items):
        type_, name = items
        return f"{ type_ } { name }"
    
    def arg_list(self, items):
        return ", ".join(items)
    
    #
    
    #Functions
    def normal_func(self, items):
        name = str(items[0])
        args = items[1] if isinstance(items[1], str) else ""
        content = str(items[2])
        returnType = str(items[3])
        
        return f"{ returnType } { name }({ args }) \n\t{content}"
    
    def func_call(self, items):
        name, args = items
        if (len(args) == 0): args = ""
        return f"{ name }({ args })"
        
    def fast_func(self, items):
        name, _, content = items
        args = items[1] if isinstance(items[1], str) else ""
        return f"void { name } ({ args }) {{ { content } }}"
        
    #
    
    #Logic
    def if_stmt_inline(self, items):
        expr = str(items[0])
        then_block = str(items[1])
        else_block = None
        
        if len(items) == 3 and items[2] is not None:
            else_block = str(items[2])
            
        s = f"if ({ expr }) {{ { then_block } }}"
        
        if else_block:
            if else_block.strip().startswith("if "):
                s += f" else {else_block}"#Else if
            else:
                s += f" else {{ {else_block} }}"#Else block
                
        return s + "\n"
    #
    
    #End of def's for lark parsing
    
    @staticmethod
    def convert(inFile, outFile, platform):
        content = ""
        try:
            file = open(inFile, "r")
            content = file.read()
            file.close()
            
        except:
            print(f"Error: could not open file '{ inFile }'")
            exit(1)
            
        #Setting up the parser and outBuff
        parser = Lark(Converter.grammar, parser="lalr", transformer=Converter())
        
        outBuff = parser.parse(content)
        #
        
        #Manipulating outBuff
        outBuff = outBuff.replace("string", "std::string")
        header = ""
        
        if (platform in Converter.allowedPlatforms):
            header += "#include <iostream>\n"
            header += "void say(std::string txt) { std::cout << txt; }\n"
            
        else:
            print(f"Error: platform '{ platform }' not supported in '{ ', '.join(Converter.allowedPlatforms) }'")
            exit(2)
            
        #Adding content based on platform
        if (platform == Converter.allowedPlatforms[0]):#linux
            None
        
        elif (platform == Converter.allowedPlatforms[1]):#windows
            None
            
        elif (platform == Converter.allowedPlatforms[2]):#mac
            None
            
        #
        
        outBuff = header + "\n\n" + outBuff
        
        #
        
        try:
            print(outFile)
            output = open(outFile, "w")
            output.write(outBuff)
            output.close()
            
        except:
            print(f"Error: could not create and write outfile. Check premissions.")
            exit(3)