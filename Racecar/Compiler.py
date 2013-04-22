from Parser import parseString


def getPythonCode(code):
    '''Convert the given Racecar code into the Python code that will
    run in the GUI.'''

    # first parse the string
    ast = parseString(code)

    # then check for errors
    if len(ast.errors) > 0:
        return (None, ast.errors)

    # then run the string through the semantic analyzer
    # ast = runSemanticAnalyzer(ast)

    # then generate python code!
    pythonCode = generatePythonCode(ast)

    return (pythonCode, None)


def generatePythonCode(ast):
    '''Traverse the AST and output a string containing the python code
    to execute in the GUI.'''

    # potential AST values and their associated translation functions
    # use astTranslators.get() instead of a long chain of else-ifs
    astTranslators = {
        "ID": idTranslator,
        "assignment_command": assignmentCommandTranslator,
        "backward": backwardTranslator,
        "backwards": backwardTranslator,
        "comparison" : comparisonTranslator,
        "declaration_command": declarationCommandTranslator,
        "define_command": defineCommandTranslator,
        "drive_command": driveCommandTranslator,
        "empty": emptyTranslator,
        "forward": forwardTranslator,
        "forwards": forwardTranslator,
        "function_command": functionCommandTranslator,
        "if_command" : ifCommandTranslator,
        "left": leftTranslator,
        "opt_else" : optElseTranslator,
        "opt_else_if" : optElseIfTranslator,
        "opt_extra_params": optExtraParamsTranslator,
        "opt_param_list": optParamListTranslator,
        "opt_parameters": optParametersTranslator,
        "plus_expression": plusExpressionTranslator,
        "print": printTranslator,
        "repeat_if_command" : repeatIfTranslator,
        "repeat_times_command" : repeatTimesTranslator,
        "right": rightTranslator,
        "statement_block": statementBlockTranslator,
        "statements": statementsTranslator,
        "times_expression": timesExpressionTranslator,
        "turn_command": turnCommandTranslator,
    }

    # "declare" pythonCode since otherwise its first use is inside
    # an if statement
    pythonCode = ""

    # Fetch the appropriate translator function from astTranslators
    # If there is no translator for ast.value then just let the
    # "translator" be ast.value
    translator = astTranslators.get(ast.value, ast.value)

    # If the "translator" is just a string (inherits from basestring),
    # then return that translator
    if isinstance(translator, basestring):
        pythonCode = ast.value

    # if the translator is a real function then invoke it
    else:
        pythonCode = translator(ast)

    return pythonCode


def indentLines(unindentedLines):
    '''Insert 4 spaces (i.e. 1 tab) at the beginning of every line'''

    splitCode = unindentedLines.splitlines(True)

    pythonCode = "    " + "    ".join(splitCode)
    return pythonCode


def emptyTranslator(ast):
    return "\n"


def statementsTranslator(ast):
    pythonCode = generatePythonCode(ast.children[0])
    pythonCode += generatePythonCode(ast.children[1])
    return pythonCode


def driveCommandTranslator(ast):
    # drive numSteps direction steps -->
    # translate_car(numSteps, direction)\n
    pythonCode = "translate_car("
    pythonCode += generatePythonCode(ast.children[1])
    pythonCode += ", " + generatePythonCode(ast.children[0])
    pythonCode += ")\n"
    return pythonCode


def forwardTranslator(ast):
    pythonCode = "CarDirection.FORWARDS"
    return pythonCode


def backwardTranslator(ast):
    pythonCode = "CarDirection.BACKWARDS"
    return pythonCode


def turnCommandTranslator(ast):
    pythonCode = "rotate_car("
    pythonCode += generatePythonCode(ast.children[1])
    pythonCode += ")\n"
    return pythonCode

def comparisonTranslator(ast):
    pythonCode = generatePythonCode(ast.children[0])
    if ast.children[1].value == "is not":
        pythonCode += " != "
        pythonCode += ast.children[2].value
    elif ast.children[1].value == "is":
        pythonCode += " = "
        pythonCode += generatePythonCode(ast.children[2])
    else:
        pythonCode += " " + generatePythonCode(ast.children[1])
        pythonCode += " " + generatePythonCode(ast.children[2])
    
    return pythonCode

def optElseIfTranslator(ast):
    pythonCode = "elif "
    pythonCode += generatePythonCode(ast.children[1]) + ":\n"
    pythonCode += generatePythonCode(ast.children[3])

    if ast.children[4].value != "empty":
        pythonCode += generatePythonCode(ast.children[4])

    return pythonCode

def optElseTranslator(ast):
    pythonCode = "else:\n"
    prelimPythonCode = generatePythonCode(ast.children[2])
    pythonCode += generatePythonCode(ast.children[2])
    return pythonCode

def ifCommandTranslator(ast):
    pythonCode = "if " + generatePythonCode(ast.children[1]) + ":\n"
    pythonCode += generatePythonCode(ast.children[3])

    if ast.children[4].value != "empty":
        pythonCode += generatePythonCode(ast.children[4])
    
    if ast.children[5].value != "empty":
        pythonCode += generatePythonCode(ast.children[5])
    return pythonCode

def leftTranslator(ast):
    pythonCode = "WheelDirection.LEFT"
    return pythonCode


def rightTranslator(ast):
    pythonCode = "WheelDirection.RIGHT"
    return pythonCode


def repeatTimesTranslator(ast):
    if ast.children[2].value == "times":
        pythonCode = "for x in range(" + ast.children[1].value + "):\n"
        pythonCode += generatePythonCode(ast.children[4])
    return pythonCode


def repeatIfTranslator(ast):
    pythonCode = "while " + generatePythonCode(ast.children[2]) + ":\n"
    pythonCode += generatePythonCode(ast.children[4])
    return pythonCode


def declarationCommandTranslator(ast):
    # id is a whatever -->
    # id = None
    pythonCode = generatePythonCode(ast.children[0])
    pythonCode += " = None\n"
    return pythonCode


def idTranslator(ast):
    pythonCode = ast.value
    return pythonCode


def assignmentCommandTranslator(ast):
    pythonCode = generatePythonCode(ast.children[1])
    pythonCode += " = "
    pythonCode += generatePythonCode(ast.children[3])
    pythonCode += "\n"
    return pythonCode


def printTranslator(ast):
    pythonCode = "print_to_console("
    pythonCode += generatePythonCode(ast.children[1])
    pythonCode += ")\n"
    return pythonCode


def defineCommandTranslator(ast):
    pythonCode = "def "
    pythonCode += generatePythonCode(ast.children[1])
    pythonCode += "("
    if ast.children[2].value == "opt_param_list":
        pythonCode += generatePythonCode(ast.children[2])
    pythonCode += "):\n"
    pythonCode += generatePythonCode(ast.children[4])
    return pythonCode


def optParamListTranslator(ast):
    pythonCode = generatePythonCode(ast.children[1])
    if ast.children[5].value == "opt_extra_params":
        pythonCode += generatePythonCode(ast.children[5])
    return pythonCode


def optExtraParamsTranslator(ast):
    pythonCode = ", "
    pythonCode += generatePythonCode(ast.children[1])
    if ast.children[5].value == "opt_extra_params":
        pythonCode += generatePythonCode(ast.children[5])
    return pythonCode


def statementBlockTranslator(ast):
    prelimPythonCode = generatePythonCode(ast.children[1])

    pythonCode = indentLines(prelimPythonCode)

    return pythonCode


def functionCommandTranslator(ast):
    pythonCode = generatePythonCode(ast.children[0])
    pythonCode += "("
    if len(ast.children) > 1:
        pythonCode += generatePythonCode(ast.children[1])
    pythonCode += ")\n"
    return pythonCode


def optParametersTranslator(ast):
    numChildren = len(ast.children)
    if numChildren > 0:
        pythonCode = generatePythonCode(ast.children[0])
        if numChildren == 2: 
            pythonCode += ", "
            pythonCode += generatePythonCode(ast.children[1])
        return pythonCode
    else:
        return ""


def binaryOperatorTranslator(ast, op):
    pythonCode = "(("
    pythonCode += generatePythonCode(ast.children[0])
    pythonCode += ") " + op + " ("
    pythonCode += generatePythonCode(ast.children[2])
    pythonCode += "))"
    return pythonCode


def plusExpressionTranslator(ast):
    return binaryOperatorTranslator(ast, "+")


def timesExpressionTranslator(ast):
    return binaryOperatorTranslator(ast, "*")


if __name__ == "__main__":
    inputString = ''
    while True:

        inputString = raw_input('enter expression > ')

        if inputString == 'exit':
            break

        else:
            print getPythonCode(inputString)
