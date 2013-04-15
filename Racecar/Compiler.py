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

    # start with an empty string
    pythonCode = ""

    if ast.value == "empty":
        return ""

    elif ast.value == "statements":
        pythonCode += generatePythonCode(ast.children[0])
        pythonCode += generatePythonCode(ast.children[1])

    elif ast.value == "drive_command":
        # drive numSteps direction steps -->
        # translate_car(numSteps, direction)\n
        pythonCode += "translate_car("
        pythonCode += generatePythonCode(ast.children[2])
        pythonCode += ", " + generatePythonCode(ast.children[1])
        pythonCode += ")\n"

    elif ast.value == "forward":
        pythonCode += "CarDirection.FORWARDS"

    elif ast.value == "backward":
        pythonCode += "CarDirection.BACKWARDS"

    elif ast.value == "turn":
        pythonCode += "rotate_car("
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += ")\n"


    elif ast.value == "declaration_command":
        # id is a whatever -->
        # id = None
        pythonCode += generatePythonCode(ast.children[0])
        pythonCode += " = None\n"

    elif ast.value == "ID":
        pythonCode += ast.value

    elif ast.value == "assignment_command":
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += " = "
        pythonCode += generatePythonCode(ast.children[3])
        pythonCode += "\n"

    elif ast.value == "print":
        pythonCode += "print_to_console("
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += ")\n"

    elif ast.value == "define_command":
        pythonCode += "def "
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += "():\n"
        pythonCode += generatePythonCode(ast.children[4])

    elif ast.value == "statement_block":
        prelimPythonCode = generatePythonCode(ast.children[1])
        # Insert 4 spaces (i.e. 1 tab) at the beginning of every line
        splitCode = prelimPythonCode.splitlines(True)

        pythonCode += "    " + "    ".join(splitCode)

    elif ast.value == "function_command":
        pythonCode += generatePythonCode(ast.children[0])
        pythonCode += "("
        pythonCode += generatePythonCode(ast.children[1])
        pythonCode += ")\n"

    elif ast.value == "opt_parameters":
        if len(ast.children) > 1:
            pythonCode += generatePythonCode(ast.children[0])
            pythonCode += generatePythonCode(ast.children[1])
            pythonCode += ", "
            



    else:
        pythonCode += ast.value

    return pythonCode
        


if __name__ == "__main__":
	inputString = ''
	while True:
	
		inputString = raw_input('enter expression > ')

		if inputString == 'exit':
			break

		else:
                        print getPythonCode(inputString)

