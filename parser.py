import ply.lex as lex
import ply.yacc as yacc
from Tree import *

reserved = {
  'drive' : 'DRIVE',
  'forward' : 'FORWARD',
  'forwards' : 'FORWARDS',
  'backward' : 'BACKWARD',
  'backwards' : 'BACKWARDS',
  'number' : 'NUMBER_TYPE',
  'word' : 'WORD_TYPE',
  'step' : 'STEP',
  'steps' : 'STEPS',
  'steer' : 'STEER',
  'left' : 'LEFT',
  'right' : 'RIGHT',
  'straight' : 'STRAIGHT',
  'canMove' : 'CAN_MOVE',
  'getCarPosition' : 'GET_CAR_POSITION',
  'define' : 'DEFINE',
  'using' : 'USING',
  'and' : 'AND',
  'or' : 'OR',
  'print' : 'PRINT',
  'if' : 'IF',
  'else' : 'ELSE',
  'repeat' : 'REPEAT',
  'times' : 'TIMES',
  'true' : 'TRUE',
  'false' : 'FALSE',
  'is' : 'IS',
  'is a' : 'IS_A',
  'is not' : 'IS_NOT',
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
t_WORD = r'"[^"]"'
t_GT = r'>'
t_LT = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_CONCAT = r'\+\+'
t_NEWLINE = r'\n|;' # semicolon for debugging interpreter use
t_ignore = ' '

def t_ID(t):
  r'[A-Za-z][A-Za-z0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_error(t):
  raise TypeError("Unknown text: `s'" % (t.value,))

lexer = lex.lex()

def p_error(p):
  raise SyntaxError()

def p_statements(p):
  '''statements : statements statement'''
  print p_statements.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].children.append(p[2])
  p[0].value = "statements"

def p_statements_empty(p):
  '''statements : empty'''
  print p_statements_empty.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].value = "statements"

def p_statement_block(p):
  """statement_block : '{' statements '}'"""
  print p_statement_block.__doc__
  p[0] = Tree()
  p[0].children.append('{')
  p[0].children.append(p[2])
  p[0].children.append('}')
  p[0].value = "statement_block"

def p_empty(p):
  '''empty :'''
  print p_empty.__doc__
  p[0] = Tree()
  p[0].value = "empty"

def p_statement_newline(p):
  '''statement : statement_contents NEWLINE
               | NEWLINE'''
  print p_statement_newline.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].children.append('NEWLINE')
  p[0].value = "statement"

def p_statement(p):
  '''statement_contents : drive_cmd
       | steer_cmd
       | define_cmd
       | repeat_if_cmd
       | repeat_times_cmd
       | if_cmd
       | print_cmd
       | assignment_cmd
       | declaration_cmd'''
  print p_statement.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].value = "statement_contents"

def p_expression(p):
  '''expression : expression OR and_expr'''
  print p_expression.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].children.append('OR')
  p[0].children.append(p[3])
  p[0].value = "expression"

def p_expression_to_and(p):
  '''expression : and_expr'''
  print p_expression_to_and.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].value = "expression"

def p_and_expr(p):
  '''and_expr : and_expr AND not_expr'''
  print p_and_expr.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].children.append('AND')
  p[0].children.append(p[3])
  p[0].value = "and_expr"


def p_and_expr_to_not(p):
  '''and_expr : not_expr'''
  print p_and_expr_to_not.__doc__
  p[0] = Tree()
  p[0].children.append(p[1])
  p[0].value = "and_expr"

def p_not_expr(p):
  '''not_expr : NOT not_expr
              | TRUE
              | FALSE
              | CAN_MOVE can_move_dir_enum
              | comparison'''
  print p_not_expr.__doc__

def p_can_move_dir_enum(p):
  '''can_move_dir_enum : drive_dir_enum
                       | steer_dir_enum'''
  print p_can_move_dir_enum.__doc__

def p_comparison(p):
  '''comparison : comparison comparison_operator number_expression
                | number_expression'''
  print p_comparison.__doc__

def p_comparison_operator(p):
  '''comparison_operator : IS
                   | IS_NOT
                   | NOT
                   | GT
                   | LT
                   | GEQ
                   | LEQ'''
  print p_comparison_operator.__doc__

def p_number_expression(p):
  '''number_expression : number_expression '+' term
                       | number_expression '-' term
                       | term'''
  print p_number_expression.__doc__

def p_term(p):
  '''term : term '*' word_expression
          | term '/' word_expression
          | word_expression'''
  print p_term.__doc__

def p_word_expression(p):
  '''word_expression : word_expression CONCAT function_term
                     | function_term'''
  print p_word_expression.__doc__

def p_function_term(p):
  '''function_term : function_term word_term
                   | word_term'''
  print p_function_term.__doc__

def p_word_term(p):
  '''word_term : '(' expression ')'
               | NUMBER
               | WORD
               | GET_CAR_POSITION
               | ID'''
  print p_word_term.__doc__

def p_drive_cmd(p):
  '''drive_cmd : DRIVE drive_dir_enum number_expression opt_steps'''
  print p_drive_cmd.__doc__

def p_drive_dir_enum(p):
  '''drive_dir_enum : FORWARD
           | FORWARDS
           | BACKWARD
           | BACKWARDS'''
  print p_drive_dir_enum.__doc__

def p_opt_steps(p):
  '''opt_steps : STEP
            | STEPS
            | empty'''
  print p_opt_steps.__doc__

def p_steer_cmd(p):
  '''steer_cmd : STEER steer_dir_enum'''
  print p_steer_cmd.__doc__

def p_steer_dir_enum(p):
  '''steer_dir_enum : LEFT
                 | RIGHT
                 | STRAIGHT'''
  print p_steer_dir_enum.__doc__

def p_define_cmd(p):
  """define_cmd : DEFINE ID opt_param_list statement_block"""
  print p_define_cmd.__doc__

def p_opt_param_list(p):
  '''opt_param_list : empty
                 | USING ID '(' type_enum ')' opt_extra_params'''
  print p_opt_param_list.__doc__

def p_opt_extra_params(p):
  '''opt_extra_params : empty
                   | AND ID '(' type_enum ')' opt_extra_params'''
  print p_opt_extra_params.__doc__

def p_type_enum(p):
  '''type_enum : WORD_TYPE
            | NUMBER_TYPE'''
  print p_type_enum.__doc__

def p_repeat_if_cmd(p):
  """repeat_if_cmd : REPEAT IF expression statement_block"""
  print p_repeat_if_cmd.__doc__

def p_repeat_times_cmd(p):
  """repeat_times_cmd : REPEAT number_expression TIMES statement_block"""
  print p_repeat_times_cmd.__doc__

def p_if_cmd(p):
  """if_cmd : IF expression statement_block opt_else_if opt_else"""
  print p_if_cmd.__doc__
  p[0] = Tree()
  p[0].children.append("IF")
  p[0].children.append(p[2])
  p[0].children.append(p[3])
  p[0].children.append(p[4])
  p[0].children.append(p[5])
  p[0].value = "if_cmd"

def p_opt_else_if(p):
  """opt_else_if : opt_else_if ELSE IF expression statement_block
                 | empty"""
  print p_opt_else_if.__doc__

def p_opt_else(p):
  """opt_else : ELSE statement_block
              | empty"""
  print p_opt_else.__doc__

def p_print_cmd(p):
  """print_cmd : PRINT word_expression"""
  print print_cmd.__doc__

def p_declaration_cmd(p):
  """declaration_cmd : ID IS_A type_enum"""
  print p_declaration_cmd.__doc__

def p_assignment_cmd(p):
  """assignment_cmd : SET ID TO expression"""
  print p_assignment_cmd.__doc__

parser = yacc.yacc()

inputString = ''
while True:
  
  inputString = raw_input('enter expression > ')

  if inputString == 'exit':
    break

  else:
    result = parser.parse(inputString)
    result.printTree()
    print
