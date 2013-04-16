from Parser import parseString

def getPythonCode(code):

    #return "translate_car(5, CarDirection.FORWARDS)"
    # first parse the string
    ast = parseString(code)

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
    astTranslators = {
      "empty" : emptyTranslator,
      "statements" : statementsTranslator,
      "drive_command" : driveCommandTranslator,
      "forward" : forwardTranslator,
      "backward" : backwardTranslator,
      "turn_command" : turnCommandTranslator,
      "left" : leftTranslator,
      "right" : rightTranslator,
      "declaration_command" : declarationCommandTranslator,
      "ID" : idTranslator,
      "assignment_command" : assignmentCommandTranslator,
      "print" : printTranslator,
      "statement_block" : statementBlockTranslator,
      "define_command" : defineCommandTranslator,
      "function_command" : functionCommandTranslator,
      "opt_parameters" : optParametersTranslator,
    }

    # "declare" pythonCode
    pythonCode = None

    # Fetch the appropriate translator function from astTranslators
    # If there is no translator for ast.value then just let the translator be ast.value
    translator = astTranslators.get(ast.value, ast.value)

    # If the "translator" is just a string, then return that translator
    if type(translator) == type(""):
        pythonCode = ast.value

    # if the translator is a real function then invoke it
    else:
        pythonCode = translator(ast)

    return pythonCode

def emptyTranslator(ast):
    return ""

def statementsTranslator(ast):
    pythonCode = generatePythonCode(ast.children[0])
    pythonCode += generatePythonCode(ast.children[1])
    return pythonCode

def driveCommandTranslator(ast):
    # drive numSteps direction steps -->
    # translate_car(numSteps, direction)\n
    pythonCode = "translate_car("
    pythonCode += generatePythonCode(ast.children[2])
    pythonCode += ", " + generatePythonCode(ast.children[1])
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

def leftTranslator(ast):
    pythonCode = "WheelDirection.LEFT"
    return pythonCode

def rightTranslator(ast):
    pythonCode = "WheelDirection.RIGHT"
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
      pythonCode += "():\n"
      pythonCode += generatePythonCode(ast.children[4])
      return pythonCode

def statementBlockTranslator(ast):
    prelimPythonCode = generatePythonCode(ast.children[1])
    # Insert 4 spaces (i.e. 1 tab) at the beginning of every line
    splitCode = prelimPythonCode.splitlines(True)

    pythonCode = "    " + "    ".join(splitCode)
    return pythonCode

def functionCommandTranslator(ast):
    pythonCode = generatePythonCode(ast.children[0])
    pythonCode += "("
    pythonCode += generatePythonCode(ast.children[1])
    pythonCode += ")\n"
    return pythonCode

def optParametersTranslator(ast):
    if len(ast.children) > 1:
        pythonCode = generatePythonCode(ast.children[0])
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += ", "
        return pythonCode
    else:
        return ""
            

if __name__ == "__main__":
	inputString = ''
	while True:
	
		inputString = raw_input('enter expression > ')

		if inputString == 'exit':
			break

		else:
                        print getPythonCode(inputString)

