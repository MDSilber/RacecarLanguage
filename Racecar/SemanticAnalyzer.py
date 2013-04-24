# NOTE - this is my code so far for the semantic analyzer.  It will be difficult to understand at this point.  Basically I copied Sam’s AST traversal code and am now slowly changing it to adjust for semantic analysis.  Functions with X’s next to them have not yet been worked on.

# TODO add attribute to SymbolTable class for “scope number,” which is essentially a count of the “depth” of scopes. NOTE a variable can be created if there is not a variable with the same scope name and a LOWER or EQUAL scope number - a variable can be used as long as there is a variable with the same name, same scope name, and a LOWER or EQUAL scope number

from SymbolTable import *
from Scope import *

table = SymbolLookupTable
counter = 0

# a list is passed in the first time this is called
# it has one Scope object with the name "global" and number 0
def analyze(ast, list):
   '''Traverse the AST and check for semantic errors.'''

   # potential AST values and their associated analysis functions
   # use astAnalzyers.get() instead of a long chain of else-ifs
   astAnalyzers = {
       "ID": idAnalyzer,
       "assignment_command": assignmentCommandAnalyzer,
       "backward": backwardAnalyzer,
       "backwards": backwardAnalyzer,
       "comparison": comparisonAnalyzer,
       "declaration_command": declarationCommandAnalyzer,
       "define_command": defineCommandAnalyzer,
       "drive_command": driveCommandAnalyzer,
       "empty": emptyAnalyzer,
       "forward": forwardAnalyzer,
       "forwards": forwardAnalyzer,
       "function_command": functionCommandAnalyzer,
       "if_command": ifCommandAnalyzer,
       "left": leftAnalyzer,
       "opt_else": optElseAnalyzer,
       "opt_else_if": optElseIfAnalyzer,
       "opt_extra_params": optExtraParamsAnalyzer,
       "opt_param_list": optParamListAnalyzer,
       "opt_parameters": optParametersAnalyzer,
       "plus_expression": plusExpressionAnalyzer,
       "print": printAnalyzer,
       "repeat_if_command": repeatIfAnalyzer,
       "repeat_times_command": repeatTimesAnalyzer,
       "right": rightAnalyzer,
       "statement_block": statementBlockAnalyzer,
       "statements": statementsAnalyzer,
       "times_expression": timesExpressionAnalyzer,
       "turn_command": turnCommandAnalyzer,
   }

   # Fetch the appropriate analyzer function from astAnalyzers
   # If there is no analyzer for ast.value then just let the
   # "analyzer" be ast.value
   analyzer = astAnalyzers.get(ast.value, ast.value)

# I have not dealt with the code between these asterisk lines yet as I need to confer with Sam about it
*************
   # If the "anaylzer" is just a string (inherits from basestring),
   # then return that analyzer
   if isinstance(analyzer, basestring):
       pythonCode = ast.value

   # if the translator is a real function then invoke it
   else:
       pythonCode = translator(ast)

   return pythonCode
*************

def statementsAnalyzer(ast, list):
   analyze(ast.children[0], list)
   analyze(ast.children[1], list)


X def driveCommandTranslator(ast):
   # drive numSteps direction steps -->
   # translate_car(numSteps, direction)\n
   pythonCode = "translate_car("
   pythonCode += generatePythonCode(ast.children[1])
   pythonCode += ", " + generatePythonCode(ast.children[0])
   pythonCode += ")\n"
   return pythonCode


X def forwardTranslator(ast):
   pythonCode = "CarDirection.FORWARDS"
   return pythonCode


X def backwardTranslator(ast):
   pythonCode = "CarDirection.BACKWARDS"
   return pythonCode


X def turnCommandTranslator(ast):
   pythonCode = "rotate_car("
   pythonCode += generatePythonCode(ast.children[1])
   pythonCode += ")\n"
   return pythonCode


X def comparisonTranslator(ast):
   pythonCode = generatePythonCode(ast.children[0])
   if ast.children[1].value == "is not":
       pythonCode += " != "
       pythonCode += ast.children[2].value
   elif ast.children[1].value == "is":
       pythonCode += " == "
       pythonCode += generatePythonCode(ast.children[2])
   else:
       pythonCode += " " + generatePythonCode(ast.children[1])
       pythonCode += " " + generatePythonCode(ast.children[2])

   return pythonCode


X def optElseIfTranslator(ast):
   pythonCode = "elif "
   pythonCode += generatePythonCode(ast.children[1]) + ":\n"
   pythonCode += generatePythonCode(ast.children[3])

   if ast.children[4].value != "empty":
       pythonCode += generatePythonCode(ast.children[4])

   return pythonCode


X def optElseTranslator(ast):
   pythonCode = "else:\n"
   prelimPythonCode = generatePythonCode(ast.children[2])
   pythonCode += generatePythonCode(ast.children[2])
   return pythonCode


X def ifCommandTranslator(ast):
   pythonCode = "if " + generatePythonCode(ast.children[1]) + ":\n"
   pythonCode += generatePythonCode(ast.children[3])

   if ast.children[4].value != "empty":
       pythonCode += generatePythonCode(ast.children[4])

   if ast.children[5].value != "empty":
       pythonCode += generatePythonCode(ast.children[5])
   return pythonCode


X def leftTranslator(ast):
   pythonCode = "WheelDirection.LEFT"
   return pythonCode


X def rightTranslator(ast):
   pythonCode = "WheelDirection.RIGHT"
   return pythonCode


X def repeatTimesTranslator(ast):
   if ast.children[2].value == "times":
       pythonCode = "for x in range(" + ast.children[1].value + "):\n"
       pythonCode += generatePythonCode(ast.children[4])
   return pythonCode


X def repeatIfTranslator(ast):
   pythonCode = "while " + generatePythonCode(ast.children[2]) + ":\n"
   pythonCode += generatePythonCode(ast.children[4])
   return pythonCode


def declarationCommandAnalyzer(ast, list):
   scopeNode = list.pop()
   list.append(scopeNode)
   table.addEntry(SymbolTableEntry(analyze(ast.children[0], list), analyze(ast.children[1], list), scopeNode.name, scopeNode.number, counter)


def idAnalyzer(ast, list):
   name = ast.value
   return name

X def assignmentCommandTranslator(ast):
   pythonCode = generatePythonCode(ast.children[1])
   pythonCode += " = "
   pythonCode += generatePythonCode(ast.children[3])
   pythonCode += "\n"
   return pythonCode


X def printTranslator(ast):
   pythonCode = "print_to_console("
   pythonCode += generatePythonCode(ast.children[1])
   pythonCode += ")\n"
   return pythonCode


def defineCommandAnalyzer(ast, list):
   id = analyze(ast.children[1], list)
   scopeNode = list.pop()
   table.addEntry(SymbolTableEntry(id, “function”, scopeNode.name, scopeNode.number, counter))
   list.append(scopeNode)
   list.append(Scope(id, 0))
   if ast.children[2].value == "opt_param_list":
      analyze(ast.children[2], list)
   analyze(ast.children[4], list)
   list.pop()                                                                                                                                                                                


def optParamListAnalyzer(ast, list):
   scopeNode = list.pop()
   table.addEntry(SymbolTableEntry(analyzer(ast.children[1], list), analyzer(ast.children[3], list), scopeNode.name, scopeNode.number, counter)
   list.append(scopeNode)
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list)


def optExtraParamsAnalyzer(ast, list):
   scopeNode = list.pop()
   table.addEntry(SymbolTableEntry(analyzer(ast.children[1], list), analyzer(ast.children[3], list), scopeNode.name, scopeNode.number, counter)
   list.append(scopeNode)
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list)

# at the end we pop since we are exiting a scope
# and we can decrease the scope count by 1
def statementBlockTranslator(ast, list):
   analyze(ast.children[1], list)

X def functionCommandTranslator(ast):
   pythonCode = generatePythonCode(ast.children[0])
   pythonCode += "("
   if len(ast.children) > 1:
       pythonCode += generatePythonCode(ast.children[1])
   pythonCode += ")\n"
   return pythonCode


X def optParametersTranslator(ast):
   numChildren = len(ast.children)
   if numChildren > 0:
       pythonCode = generatePythonCode(ast.children[0])
       if numChildren == 2:
           pythonCode += ", "
           pythonCode += generatePythonCode(ast.children[1])
       return pythonCode
   else:
       return ""


X def binaryOperatorTranslator(ast):
   pythonCode = "(("
   pythonCode += generatePythonCode(ast.children[0])
   pythonCode += ") "
   pythonCode += generatePythonCode(ast.children[1])
   pythonCode += " ("
   pythonCode += generatePythonCode(ast.children[2])
   pythonCode += "))"
   return pythonCode


X def plusExpressionTranslator(ast):
   return binaryOperatorTranslator(ast)


X def timesExpressionTranslator(ast):
   return binaryOperatorTranslator(ast)




