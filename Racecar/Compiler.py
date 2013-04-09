from Parser import parseString

def getPythonCode(code):
    #return "translate_car(5, CarDirection.FORWARDS)"
    # first parse the string
    ast = parseString(code)
    # then run the string through the semantic analyzer
    # ast = runSemanticAnalyzer(ast)
    # then generate python code!
    pythonCode = generatePythonCode(ast)

    return pythonCode


def generatePythonCode(ast):
    pythonCode = ""
    if ast.value == "empty":
        return ""
    elif ast.value == "statements":
        pythonCode += generatePythonCode(ast.children[0])
        pythonCode += generatePythonCode(ast.children[1])
    elif ast.value == "drive_command":
        pythonCode += "translate_car("
        pythonCode += generatePythonCode(ast.children[2])
        pythonCode += ", " + generatePythonCode(ast.children[1])
        pythonCode += ")\n"
    elif ast.value == "forward":
        pythonCode += "CarDirection.FORWARDS"
    elif ast.value == "backward":
        pythonCode += "CarDirection.BACKWARDS"
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
			result = parseString(inputString)
                        result.printTree()
                        print generatePythonCode(result)

