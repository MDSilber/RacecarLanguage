# NOTE - this is my code so far for the semantic analyzer.  
# It will be difficult to understand at this point.  
# Basically I copied Sam’s AST traversal code and am now slowly changing it to adjust for semantic analysis.
# Functions with X’s next to them have not yet been worked on.

# OLD TODO add attributes to SymbolTable class for “tier number” and for "universal count"

# OLD Tier number is the "layer" of the scoping.  Universal count is a unique number for every single scope,
# the purpose of which is to differentiate between scopes in the same layer.

from SymbolTable import *
from Scope import *

table = SymbolLookupTable
count = 0

# OLD a list is passed in the first time this is called
# OLD it has one Scope object with the name "global" and number 0
# List will be a list of numbers, each number is a block's universal count
def analyze(ast, list1):
   '''Traverse the AST and check for semantic errors.'''

   # potential AST values and their associated analysis functions
   # use astAnalzyers.get() instead of a long chain of else-ifs
   astAnalyzers = {
       "assignment_command": assignmentCommandAnalyzer,,
       "comparison": comparisonAnalyzer,
       "declaration_command": declarationCommandAnalyzer,
       "define_command": defineCommandAnalyzer,
       "drive_command": driveCommandAnalyzer,
       "empty": emptyAnalyzer,
       "function_command": functionCommandAnalyzer,
       "if_command": ifCommandAnalyzer,
       "opt_else": optElseAnalyzer,
       "opt_else_if": optElseIfAnalyzer,
       "opt_extra_params": optExtraParamsAnalyzer,
       "opt_param_list": optParamListAnalyzer,
       "opt_parameters": optParametersAnalyzer,
       "plus_expression": plusExpressionAnalyzer,
       "print": printAnalyzer,
       "repeat_if_command": repeatIfAnalyzer,
       "repeat_times_command": repeatTimesAnalyzer,
       "statement_block": statementBlockAnalyzer,
       "statements": statementsAnalyzer,
       "times_expression": timesExpressionAnalyzer,
       "turn_command": turnCommandAnalyzer,
   }

   # Fetch the appropriate analyzer function from astAnalyzers
   # If there is no analyzer for ast.value then just let the
   # "analyzer" be ast.value
   analyzer = astAnalyzers.get(ast.value, ast.value)


   # If the "anaylzer" is just a string (inherits from basestring)
   if isinstance(analyzer, basestring):
      # not sure what to do here yet
      # need to check for variable existence
      # and scope checking

   # if the translator is a real function, then invoke it
   else:
       analyze(ast, list1)


def statementsAnalyzer(ast, list1):
   analyze(ast.children[0], list1)
   analyze(ast.children[1], list1)


def driveCommandAnalyzer(ast, list1):
   # for "plus_expression"
   analyze(ast.children[2], list1)


def turnCommandAnalyzer(ast, list1):
   # nothing to do here


def comparisonTranslator(ast):
   # why do we have a comparison production that does "comaprison -> comparison ..."
   
   # child 0 needs to be an identifier
   # child 2 could be an identifier
   # child 2 needs to be of equal type
   
   # check that child 0 is an identifier
   if (ast.children[0].type != "ID")
      # TODO raise error
   
   # child 0 is an identifier - check scope
   # TODO verify scope
   
   # check that the type is the same on each
   # TODO type check


def optElseIfAnalyzer(ast, list1):
   # for "expression"
   if ast.children[1].value != "empty":
      analyze(ast.children[1])
   # for "statement_block"
   if ast.chidlren[3].value != "empty":
      analyze(ast.children[3])
   # for "optional_else_if"
   if ast.children[4].value != "empty":
      analyze(ast.children[4])


def optElseAnalyzer(ast, list1):
   # for "statement_block"
   if ast.children[2].value != "empty":
      analyze(ast.children[2])


def ifCommandAnalyzer(ast, list1):
   # for "expression"
   analyze(ast.children[1])
   # for "statement_block"
   analyze(ast.children[3])

   if ast.children[4].value != "empty":
       analyze(ast.children[4])

   if ast.children[5].value != "empty":
       analyze(ast.children[5])


def repeatTimesAnalyzer(ast, list1):
   # for "plus_expression"
   analyze(ast.children[1])
   # for "statement_block"
   analyze(ast.children[4])


def repeatIfAnalyzer(ast, list1):
   # for "expression"
   analyze(ast.children[2])
   # for "statement_block"
   analyze(ast.children[4])


def declarationCommandAnalyzer(ast, list1):
   table.addEntry(SymbolTableEntry(analyze(ast.children[0], list1), analyze(ast.children[1], list1), list(list1)))


def assignmentCommandAnalyzer(ast, list1):
   # check for the existence of ID - child 1
   # and if it exists, check that it can be accessed in this block
   # TODO verify ID
   
   # if these tests pass, do type checking
   # child 3  is an expression - it needs to be evaluated to a type
   # TODO type check


def printAnalyzer(ast, list1):
   # for the word or identifier
   analyze(ast.children[1], list1)
   # check will be done in analyze


def defineCommandAnalyzer(ast, list1):
   id = analyze(ast.children[1], list1)
   table.addEntry(SymbolTableEntry(id, "function", list(list1)))
   list1.append(count+1)
   if ast.children[2].value == "opt_param_list":
      analyze(ast.children[2], list1)
   list1.pop()
   # for "statement_block"
   analyze(ast.children[4], list1)                                                                                                                                                                              


def optParamListAnalyzer(ast, list1):
   table.addEntry(SymbolTableEntry(analyzer(ast.children[1], list1), analyzer(ast.children[3], list1), list(list1)))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list1)


def optExtraParamsAnalyzer(ast, list1):
   table.addEntry(SymbolTableEntry(analyzer(ast.children[1], list1), analyzer(ast.children[3], list1), list(list1)))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list1)

def statementBlockAnalyzer(ast, list1):
   count += 1
   list1.append(count)
   analyze(ast.children[1], list1)
   list1.pop()

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


def plusExpressionAnalyzer(ast, list1):
   return binaryOperatorAnalyzer(ast, list1)


def timesExpressionAnalyzer(ast, list1):
   return binaryOperatorAnalyzer(ast, list1)





