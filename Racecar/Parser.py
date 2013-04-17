import ply.lex as lex
import ply.yacc as yacc
from Tree import *

reserved = {
  'drive' : 'DRIVE',
  'forward' : 'FORWARD',
  'forwards' : 'FORWARDS', # never passed on to parser
  'backward' : 'BACKWARD',
  'backwards' : 'BACKWARDS',# never passed on to parser 
  'number' : 'NUMBER_TYPE',
  'word' : 'WORD_TYPE',
  'step' : 'STEP',
  'steps' : 'STEPS',# never passed on to parser
  'turn' : 'TURN',
  'left' : 'LEFT',
  'right' : 'RIGHT',
  'canMove' : 'CAN_MOVE',
  'getCarPosition' : 'GET_CAR_POSITION',
  'getWheelDirection' : 'GET_WHEEL_DIRECTION',
  'define' : 'DEFINE',
  'using' : 'USING',
  'and' : 'AND',
  'or' : 'OR',
  'print' : 'PRINT',
  'elseIf' : 'ELSE_IF',
  'if' : 'IF',
  'else' : 'ELSE',
  'repeat' : 'REPEAT',
  'times' : 'TIMES',
  'true' : 'TRUE',
  'false' : 'FALSE',
  'a' : 'A',
  'is' : 'IS',
  'not' : 'NOT',
  'set' : 'SET',
  'to' : 'TO',
}


tokens = [ "NUMBER",
           "WORD",
           "ID",
           "GT",
           "LT",
           "GEQ",
           "LEQ",
           "CONCAT",
           "NEWLINE",
] + list(reserved.values())

literals = "{}()+-*/"

t_NUMBER = r'[0-9]+'
t_WORD = r'".*?"'
t_GT = r'>'
t_LT = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_CONCAT = r'\+\+'
t_ignore = ' \t'

def t_ID(t):
  r'[A-Za-z][A-Za-z0-9]*( a)?'
  t.type = reserved.get(t.value, 'ID')
  # get rid of forward/forwards, backward/backwards, and step/steps ambiguity
  if t.type == "FORWARDS" or t.type == "BACKWARDS" or t.type == "STEPS":
    t.type = t.type[:-1]
    t.value = t.value[:-1]
  return t
  
def t_NEWLINE(t):
  r'\n|;' # semicolon for debugging interpreter use
  t.lexer.lineno += 1
  return t

def t_error(t):
  print "Illegal character '%s' at line '%s'" % (t.value[0], t.lexer.lineno)
  t.lexer.skip(1)
  return t

lexer = lex.lex()

def p_error(p):
  if p == None:
    raise SyntaxError("Reached end of file unexpectedly!")
  elif p.value[0] == None:
    print "Lexing Error with character ", p.value[1]
    p.value = p.value[1]
  else:
    print "Syntax error at token ", p.type#, " at line ", p.lineno(num), " and position ", p.lexpos(num)
    # Read ahead looking for a closing '}'
    #while 1:
    #  tok = yacc.token()             # Get the next token
    #  if not tok or tok.type == 'NEWLINE': break
    #yacc.restart()

def makeParseTreeNode(p, value):
  '''Returns a Tree object containing
     as children p[1:] and a value of value'''
  toReturn = Tree()
  for element in p[1:]:
    if type(element) == type(toReturn):
      toReturn.children.append(element)
      toReturn.errors += element.errors
    else:
      # the element is not a tree. wrap it in a tree
      newElement = Tree()
      newElement.value = element
      toReturn.children.append(newElement)

  toReturn.value = value
  if value == "error":
    toReturn.errors.append(p[1])
 
  return toReturn


def p_statements(p):
  '''statements : statements statement'''
  #print p_statements.__doc__
  if p[1].value == "empty" and p[2].value != "empty":
    p[0] = p[2]
  elif p[2].value == "empty" and p[1].value != "empty":
    p[0] = p[1]
  elif p[2].value == "empty" and p[1].value == "empty":
    p[0] = makeParseTreeNode(p, "empty")
  else:
    p[0] = makeParseTreeNode(p, "statements")

def p_error_statement(p):
  '''statement : error NEWLINE'''
  p[0] = makeParseTreeNode(p, "error")

def p_statements_empty(p):
  '''statements : empty'''
  p[0] = p[1]
  #print p_statements_empty.__doc__

def p_statement_block(p):
  """statement_block : '{' statements '}' NEWLINE"""
  #print p_statement_block.__doc__
  p[0] = makeParseTreeNode(p, "statement_block")

def p_empty(p):
  '''empty :'''
  #print p_empty.__doc__
  p[0] = Tree()
  p[0].value = "empty"

def p_statement_simple_compound(p):
  '''statement : simple_statement
               | compound_statement'''
  p[0] = p[1]

def p_simple_statement_command(p):
  '''simple_statement : statement_contents NEWLINE'''
  #print p_statement_command.__doc__
  p[0] = p[1]

def p_statement_newline(p):
  '''simple_statement : NEWLINE'''
  #print p_statement_newline.__doc__
  p[0] = Tree()
  p[0].value = "empty"

def p_statement_contents_drive(p):
  '''statement_contents : drive_command'''
  #print p_statement_contents_drive.__doc__
  p[0] = p[1]

def p_statement_contents_turn(p):
  '''statement_contents : turn_command'''
  #print p_statement_contents_turn.__doc__
  p[0] = p[1]

def p_compound_statement_define(p):
  '''compound_statement : define_command'''
  #print p_statement_contents_define.__doc__
  p[0] = p[1]

def p_compound_statement_repeat_if(p):
  '''compound_statement : repeat_if_command'''
  #print p_statement_contents_repeat_if.__doc__
  p[0] = p[1]

def p_compound_statement_repeat_times(p):
  '''compound_statement : repeat_times_command'''
  #print p_statement_contents_repeat_times.__doc__
  p[0] = p[1]

def p_compound_statement_if(p):
  '''compound_statement : if_command'''
  #print p_statement_contents_if.__doc__
  p[0] = p[1]

def p_statement_contents_print(p):
  '''statement_contents : print_command'''
  #print p_statement_contents_print.__doc__
  p[0] = p[1]

def p_statement_contents_assignment(p):
  '''statement_contents : assignment_command'''
  #print p_statement_contents_assignment.__doc__
  p[0] = p[1]

def p_statement_contents_declaration(p):
  '''statement_contents : declaration_command'''
  #print p_statement_contents_declaration.__doc__
  p[0] = p[1]

def p_statement_contents_function(p):
  '''statement_contents : function_command'''
  #print p_statement_contents_function.__doc__
  p[0] = p[1]

def p_expression(p):
  '''expression : expression OR and_expression'''
  #print p_expression.__doc__
  p[0] = makeParseTreeNode(p, "expression")

def p_expression_to_and(p):
  '''expression : and_expression'''
  #print p_expression_to_and.__doc__
  p[0] = p[1]

def p_and_expression(p):
  '''and_expression : and_expression AND not_expression'''
  #print p_and_expression.__doc__
  p[0] = makeParseTreeNode(p, "and_expression")


def p_and_expr_to_not(p):
  '''and_expression : not_expression'''
  #print p_and_expr_to_not.__doc__
  p[0] = p[1]

def p_not_expression_not(p):
  '''not_expression : NOT not_expression'''
  #print p_not_expression_not.__doc__
  p[0] = makeParseTreeNode(p, "not_expression")

def p_not_expression_true_false(p):
  '''not_expression : TRUE
                    | FALSE'''
  #print p_not_expression_true.__doc__
  p[0] = makeParseTreeNode(p, "not_expression")

def p_not_expression_can_move(p):
  '''not_expression : CAN_MOVE can_move_direction'''
  #print p_not_expression_can_move.__doc__
  p[0] = makeParseTreeNode(p, "not_expression")

def p_not_expression_comparison(p):
  '''not_expression : comparison'''
  #print p_not_expression_comparison.__doc__
  p[0] = p[1]

def p_can_move_direction(p):
  '''can_move_direction : drive_direction
                        | turn_direction'''
  #print p_can_move_direction.__doc__
  p[0] = p[1]

def p_comparison_with_operator(p):
  '''comparison : comparison comparison_operator plus_expression'''
  #print p_comparison_operator.__doc__
  p[0] = makeParseTreeNode(p, "comparison")

def p_comparison_plus(p):
  '''comparison : plus_expression'''
  #print p_comparison_plus.__doc__
  p[0] = p[1]

def p_comparison_operator(p):
  '''comparison_operator : IS
                   | IS NOT
                   | GT
                   | LT
                   | GEQ
                   | LEQ'''
  #print p_comparison_operator.__doc__
  if len(p) == 3: # i.e. token is IS NOT
    p[0] = p[1] + " " + p[2]
  else: # any other token
    p[0] = p[1]

def p_plus_expression_plus_minus(p):
  '''plus_expression : plus_expression '+' times_expression
                       | plus_expression '-' times_expression'''
  #print p_plus_expression_plus_minus.__doc__
  p[0] = makeParseTreeNode(p, "plus_expression")

def p_plus_expression_times_expression(p):
  '''plus_expression : times_expression'''
  #print p_plus_expression_times_expression.__doc__
  p[0] = p[1]

def p_times_expression_times_divide(p):
  '''times_expression : times_expression '*' word_expression
          | times_expression '/' word_expression'''
  #print p_times_expression_times_divide.__doc__
  p[0] = makeParseTreeNode(p, "times_expression")

def p_times_expression_word_expression(p):
  '''times_expression : word_expression'''
  #print p_times_expression_word_expression.__doc__
  p[0] = p[1]

def p_word_expression_concat(p):
  '''word_expression : word_expression CONCAT primary_expression'''
  #print p_word_expression_concat.__doc__
  p[0] = makeParseTreeNode(p, "word_expression")

def p_word_expression_primary_expression(p):
  '''word_expression : primary_expression'''
  #print p_word_expression_primary_expression.__doc__
  p[0] = p[1]

def p_primary_expression_parens(p):
  """primary_expression : '(' expression ')'"""
  #print p_primary_expression_parens.__doc__
  p[0] = makeParseTreeNode(p, "primary_expression")

def p_primary_expression_token(p):
  '''primary_expression : NUMBER
               | WORD
               | GET_CAR_POSITION
               | GET_WHEEL_DIRECTION
               | ID'''
  #print p_primary_expression_token.__doc__
  p[0] = p[1]

def p_function_command(p):
  '''function_command : primary_expression opt_parameters'''
  #print p_function_command.__doc__
  p[0] = makeParseTreeNode(p, "function_command")

def p_opt_parameters(p):
  '''opt_parameters : opt_parameters primary_expression
                    | empty'''
  if p[1].value == "empty":
    p[0] = makeParseTreeNode(p, "empty")
  else:
    p[0] = makeParseTreeNode(p, "opt_parameters")

def p_drive_command(p):
  '''drive_command : DRIVE drive_direction plus_expression opt_steps'''
  #print p_drive_command.__doc__
  p[0] = makeParseTreeNode(p, "drive_command")

def p_drive_direction(p):
  '''drive_direction : FORWARD
           | BACKWARD'''
  #print p_drive_direction.__doc__
  p[0] = p[1]

def p_opt_steps(p):
  '''opt_steps : STEP
            | empty'''
  #print p_opt_steps.__doc__
  p[0] = p[1]

def p_turn_command(p):
  '''turn_command : TURN turn_direction'''
  #print p_turn_command.__doc__
  p[0] = makeParseTreeNode(p, "turn_command")

def p_turn_direction(p):
  '''turn_direction : LEFT
                 | RIGHT'''
  #print p_turn_direction.__doc__
  p[0] = p[1]

def p_define_command(p):
  """define_command : DEFINE ID opt_param_list NEWLINE statement_block"""
  #print p_define_command.__doc__
  p[0] = makeParseTreeNode(p, "define_command")

def p_opt_param_list(p):
  '''opt_param_list : empty
                 | USING ID '(' type_enum ')' opt_extra_params'''
  #print p_opt_param_list.__doc__
  p[0] = makeParseTreeNode(p, "opt_param_list")

def p_opt_extra_params(p):
  '''opt_extra_params : empty
                   | AND ID '(' type_enum ')' opt_extra_params'''
  #print p_opt_extra_params.__doc__
  p[0] = makeParseTreeNode(p, "opt_extra_params")

def p_type_enum(p):
  '''type_enum : WORD_TYPE
            | NUMBER_TYPE'''
  #print p_type_enum.__doc__
  p[0] = p[1]

def p_repeat_if_command(p):
  """repeat_if_command : REPEAT IF expression NEWLINE statement_block"""
  #print p_repeat_if_command.__doc__
  p[0] = makeParseTreeNode(p, "repeat_if_command")

def p_repeat_times_command(p):
  """repeat_times_command : REPEAT plus_expression TIMES NEWLINE statement_block"""
  #print p_repeat_times_command.__doc__
  p[0] = makeParseTreeNode(p, "repeat_times_command")

def p_if_command(p):
  """if_command : IF expression NEWLINE statement_block opt_else_if opt_else"""
  #print p_if_command.__doc__
  p[0] = makeParseTreeNode(p, "if_command")

def p_opt_else_if(p):
  """opt_else_if : ELSE_IF expression NEWLINE statement_block opt_else_if
                 | empty"""
  #print p_opt_else_if.__doc__
  p[0] = makeParseTreeNode(p, "opt_else_if")

def p_opt_else(p):
  """opt_else : ELSE NEWLINE statement_block
              | empty"""
  #print p_opt_else.__doc__
  p[0] = makeParseTreeNode(p, "opt_else")

def p_print_command(p):
  """print_command : PRINT word_expression"""
  #print p_print_command.__doc__
  p[0] = makeParseTreeNode(p, "print")

def p_declaration_command(p):
  """declaration_command : ID IS A type_enum"""
  #print p_declaration_command.__doc__
  p[0] = makeParseTreeNode(p, "declaration_command")

def p_assignment_command(p):
  """assignment_command : SET ID TO expression"""
  #print p_assignment_command.__doc__
  p[0] = makeParseTreeNode(p, "assignment_command")

parser = yacc.yacc()

def parseString(stringToParse):
  '''Returns the parse tree for the given string'''
  return parser.parse(stringToParse)

if __name__ == "__main__":
	inputString = ''
	while True:
	
		inputString = raw_input('enter expression > ')

		if inputString == 'exit':
			break

		else:
                        try:
                          result = parser.parse(inputString)
                        except SyntaxError as e:
                          print "Error: ", e
                        else:
                          result.printTree()
                          print
                          print "errors: ",result.errors
