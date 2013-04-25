# TODO handle errors for expressions elsewhere (besides just expression)

# TODO handle function cannot be nested

# TODO rename list1 to scopelist
# TODO change types to lowercase

# TODO check if the type is a function, if it is, you can use it wherever you want - IN SYMBOL TABLE CHECKING

# NOTE - this is my code so far for the semantic analyzer.  
# It will be difficult to understand at this point.  
# Basically I copied Sam’s AST traversal code and am now slowly changing it to adjust for semantic analysis.
# Functions with X’s next to them have not yet been worked on.

# Universal count is a unique number for every single scope,
# the purpose of which is to differentiate between scopes in the same layer.

from SymbolTable import *

table = SymbolLookupTable
count = 0
inFunction = False


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
   
   # word_expession Analyzer needed

   # Fetch the appropriate analyzer function from astAnalyzers
   # If there is no analyzer for ast.value, then just let the
   # "analyzer" be ast.value
   analyzer = astAnalyzers.get(ast.value, ast.value)


   # If the "anaylzer" is just a string (inherits from basestring)
   if isinstance(analyzer, basestring):
      # this should only be useful for evaluating the type of an expression
      if (ast.type == "WORD")
         return "WORD"
      else if (ast.type == "NUMBER")
         return "NUMBER"
      else if (ast.type == "ID")
         # do existence and scope checking right here
         # return type if passes
         id = ast.value
         idEntry = table.getEntry(SymbolTableEntry(id, None, list(list1))))
         if idEntry == None
            # ID does not exist or exists but the scoping is wrong
            # TODO return (OR PRINT) error
            # this is to be returned to binaryOperatorAnalyzer
            return "ERROR"
         return idEntry.type

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
   # TODO if the types are both words, check to see if the operator is "IS" or "IS_NOT"
   # SEND BOTH child 0 and child 2 through binaryOperatorAnalyze
   
   # child 0 needs to be an identifier
   # child 2 could be an identifier
   # child 2 needs to be of equal type
   
   result = binaryOperatorAnalyzer(ast, list1)
   if result == "NUMBER"
      return valid # TODO
   elif result == "WORD"
      if ast.children[1].value == "IS" or ast.children[1].value == "IS NOT":
         return valid
      else
         #TODO return error
   else
      #TODO return error


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
   # Note ast.children[3].type is word
   table.addEntry(SymbolTableEntry(ast.children[0].value, ast.children[3].value, list(list1)))


def assignmentCommandAnalyzer(ast, list1):
   # check for the existence of ID - child 1
   # and that it can be accessed in this block
   id = ast.children[1].value
   idEntry = table.getEntry(SymbolTableEntry(id, None, list(list1))))
   if idEntry == None
      # ID does not exist or exists but the scoping is wrong
      # TODO return error
   
   # do type checking
   # child 3 is an expression - it needs to be evaluated to a type
   child3Evaluation = analyze(ast.children[3])
   if child3Evaluation == "ERROR"
      # type check in expression failed
      # TODO return error
   else
      if idEntry.type != child3Evaluation
         # type check failed
         # TODO return an error


def printAnalyzer(ast, list1):
   # for the word or identifier
   analyze(ast.children[1], list1)
   # check will be done in analyze


def defineCommandAnalyzer(ast, list1):
   id = ast.children[1].value
   # TODO fix this
   table.addEntry(SymbolTableEntry(id, "function", list(list1)))
   list1.append(count+1)
   inFunction = True
   if ast.children[2].value == "opt_param_list":
      analyze(ast.children[2], list1)
   list1.pop()
   # for "statement_block"
   analyze(ast.children[4], list1)
   inFunction = False


def optParamListAnalyzer(ast, list1):
   table.addEntry(SymbolTableEntry(ast.children[1].value, ast.children[3].value, list(list1)))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list1)


def optExtraParamsAnalyzer(ast, list1):
   table.addEntry(SymbolTableEntry(ast.children[1].value, ast.children[3].value, list(list1)))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5], list1)


def statementBlockAnalyzer(ast, list1):
   count += 1
   list1.append(count)
   analyze(ast.children[1], list1)
   list1.pop()


# currently working on this
def functionCommandAnalyzer(ast, list1):
   
   
   pythonCode = generatePythonCode(ast.children[0])
   pythonCode += "("
   if len(ast.children) > 1:
      pythonCode += generatePythonCode(ast.children[1])
   pythonCode += ")\n"
   return pythonCode
   
   
def functionNameFinder(ast):
   if len(ast.children) == 1
      return ast.children[0].value
   else
      functionNameFinder(ast.children[0])
   
   
def functionParameterTypeFinder(ast):  
   # working on this


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


def binaryOperatorAnalyzer(ast, list1):
   result1 = analyze(ast.children[0], list1)
   result3 = analyze(ast.children[2], list1)
   
   if result1 == "ERROR" or result3 == "ERROR"
      return "ERROR"
   
   if result1 == result3
      return result1
      
   else
      return "ERROR" 


def plusExpressionAnalyzer(ast, list1):
   result = binaryOperatorAnalyzer(ast, list1)
   if result == "NUMBER"
      return valid # TODO
   else
      # TODO return error


def timesExpressionAnalyzer(ast, list1):
   result = binaryOperatorAnalyzer(ast, list1)
   if result == "NUMBER"
      return valid # TODO
   else
      # TODO return error

def wordExpressionAnalyzer(ast, list1):
   result = binaryOperatorAnalyzer(ast, list1)
   if result == "WORD"
      return valid # TODO
   else
      # TODO return error




