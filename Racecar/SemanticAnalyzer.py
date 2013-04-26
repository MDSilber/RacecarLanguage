# TODO handle function parameter number and types

# Scoping done using a universal count, which is a unique number for every single scope

from SymbolTable import *

table = SymbolLookupTable
count = 0
inFunction = False
function = None
scopeList = [0]
errorList = []
firstPass = True

def analyzeStart(ast):
  analyze(ast)
  firstPass = False
  analyze(ast)

def analyze(ast):
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
       "word_expression": wordExpressionAnalyzer,
   }

   # Fetch the appropriate analyzer function from astAnalyzers
   # If there is no analyzer for ast.value, then just let the
   # "analyzer" be ast.value
   analyzer = astAnalyzers.get(ast.value, ast.value)


   # If the "anaylzer" is just a string (inherits from basestring)
   if isinstance(analyzer, basestring):
      # this should only be useful for evaluating the type of an expression
      if (ast.type.lower() == "word")
         return "word"
      else if (ast.type.lower() == "number")
         return "number"
      else if (ast.type == "ID")
         # do existence and scope checking right here
         # return type if passes
         id = ast.value
         idEntry = table.getEntry(SymbolTableEntry(id, None, list(scopeList), function)))
         if idEntry == None
            # ID does not exist or exists but the scoping is wrong
            # this is to be returned to binaryOperatorAnalyzer
            return "ERROR"
         return idEntry.type

   # if the translator is a real function, then invoke it
   else:
       analyzer(ast)


def statementsAnalyzer(ast):
  if firstPass
      if ast.children[0].value == "define_command" or ast.children.value == "statements"
          analyze(ast.children[0])
      if ast.children[1].value == "define_command" or ast.children[1].value == "statements"
          analyze(ast.children[1])
  else
      analyze(ast.children[0])
      analyze(ast.children[1])


def driveCommandAnalyzer(ast):
   # for "plus_expression"
   analyze(ast.children[2])


def turnCommandAnalyzer(ast):
   # nothing to do here


def comparisonTranslator(ast):
   result = binaryOperatorAnalyzer(ast)
   if result == "number"
      return valid
   elif result == "word"
      if ast.children[1].value == "IS" or ast.children[1].value == "IS NOT":
         return valid
      else
         errorList.append("Error in comparison: words must be compared using 'is' or 'is not'")
      else
      errorList.append("Error in comparison: use only words or only numbers; cannot mix both")


def optElseIfAnalyzer(ast):
   # for "expression"
   if ast.children[1].value != "empty":
      analyze(ast.children[1])
   # for "statement_block"
   if ast.chidlren[3].value != "empty":
      analyze(ast.children[3])
   # for "optional_else_if"
   if ast.children[4].value != "empty":
      analyze(ast.children[4])


def optElseAnalyzer(ast):
   # for "statement_block"
   if ast.children[2].value != "empty":
      analyze(ast.children[2])


def ifCommandAnalyzer(ast):
   # for "expression"
   analyze(ast.children[1])
   # for "statement_block"
   analyze(ast.children[3])

   if ast.children[4].value != "empty":
       analyze(ast.children[4])

   if ast.children[5].value != "empty":
       analyze(ast.children[5])


def repeatTimesAnalyzer(ast):
   # for "plus_expression"
   analyze(ast.children[1])
   # for "statement_block"
   analyze(ast.children[4])


def repeatIfAnalyzer(ast):
   # for "expression"
   analyze(ast.children[2])
   # for "statement_block"
   analyze(ast.children[4])


def declarationCommandAnalyzer(ast):
   # Note ast.children[3].type is word
   table.addEntry(SymbolTableEntry(ast.children[0].value, ast.children[3].value, list(scopeList), function))


def assignmentCommandAnalyzer(ast):
   # check for the existence of ID - child 1
   # and that it can be accessed in this block
   id = ast.children[1].value
   idEntry = table.getEntry(SymbolTableEntry(id, None, list(scopeList), function)))
   if idEntry == None
      # ID does not exist or exists but the scoping is wrong
      errorList.append("Error in assignment: variable does not exist or cannot be used here")
   
   # do type checking
   # child 3 is an expression - it needs to be evaluated to a type
   child3Evaluation = analyze(ast.children[3])
   if child3Evaluation == "ERROR"
      # type check in expression failed
      errorList.append("Error in assignment: use only words or only numbers; cannot mix both")
   else
      if idEntry.type != child3Evaluation
         # type check failed
          errorList.append("Error in assignment: variable and value must have the same type")


def printAnalyzer(ast):
   # for the word or identifier
   analyze(ast.children[1])
   # check will be done in analyze


def defineCommandAnalyzer(ast):
   id = ast.children[1].value
   if firstPass
      table.addEntry(SymbolTableEntry(id, "function", list(scopeList), function))
      return
   if scopeList[-1] != 0
      errorList.append("Error in function creation: functions cannot be created in other functions or a nested block")
   scopeList.append(count+1)
   inFunction = True
   function = id
   if ast.children[2].value == "opt_param_list":
      analyze(ast.children[2])
   scopeList.pop()
   # for "statement_block"
   analyze(ast.children[4])
   inFunction = False
   function = None


def optParamListAnalyzer(ast):
   table.addEntry(SymbolTableEntry(ast.children[1].value, ast.children[3].value, list(scopeList), function))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5])


def optExtraParamsAnalyzer(ast):
   table.addEntry(SymbolTableEntry(ast.children[1].value, ast.children[3].value, list(scopeList), function))
   if ast.children[5].value == "opt_extra_params":
       analyze(ast.children[5])


def statementBlockAnalyzer(ast):
   count += 1
   scopeList.append(count)
   analyze(ast.children[1])
   scopeList.pop()


# currently working on this
def functionCommandAnalyzer(ast):
   
   
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

# this is for user-defined function parameters
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


def binaryOperatorAnalyzer(ast):
   result1 = analyze(ast.children[0])
   result3 = analyze(ast.children[2])
   
   if result1 == "ERROR" or result3 == "ERROR"
      return "ERROR"
   
   if result1 == result3
      return result1
      
   else
      return "ERROR" 


def plusExpressionAnalyzer(ast):
   result = binaryOperatorAnalyzer(ast)
   if result == "number"
      return valid
   else
      errorList.append("Error in an expression: use only words or only numbers; cannot mix both")


def timesExpressionAnalyzer(ast):
   result = binaryOperatorAnalyzer(ast)
   if result == "number"
      return valid
   else
      errorList.append("Error in an expression: use only words or only numbers; cannot mix both")

def wordExpressionAnalyzer(ast):
   result = binaryOperatorAnalyzer(ast)
   if result == "word"
      return valid
   else
      errorList.append("Error in an expression: use only words or only numbers; cannot mix both")




