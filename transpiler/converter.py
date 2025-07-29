from lark import Lark, Transformer, Tree

class Converter(Transformer):
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
    start: normal_func+
    //
    
    //Functions
    normal_func: CNAME "=" "(" [arg_list] ")" "=>" "{" code_content "}" "<" TYPE ">"
    //
    """
    
    #The transpiler only accepts these platforms at the moment
    allowedPlatforms = ["linux", "windows", "mac"]
    #
    
    def start(self, items): return '\n\n'.join(items)
    
    def arg(self, items):
        type_, name = items
        return f"{ type_ } { name }"
    
    def arg_list(self, items):
        return ", ".join(items)
    
    def normal_func(self, items):
        name = str(items[0])
        args = items[1] if isinstance(items[1], str) else ""
        contentTree = items[2]
        content = "".join(str(token) for token in contentTree.children)
        returnType = str(items[3])
        
        return f"{ returnType } { name }({ args }) {{ \n\t{content} }}"
    
    
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
        
        
        