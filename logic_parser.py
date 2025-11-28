"""
Logical expression parser and validator
Handles expression parsing, validation, and variable extraction
"""
import re
import itertools

class LogicParser:
    """Parser for logical expressions with validation"""
    
    def __init__(self):
        self.operators = {
            '¬', '~', '!',  # Negation
            '∧', '&', '&&', 'AND',  # Conjunction
            '∨', '|', '||', 'OR',   # Disjunction  
            '→', '->', '=>', 'IMP',  # Implication
            '↔', '<->', '<=>', 'XNOR', # Biconditional
            '⊕', '^', 'XOR',        # Exclusive OR
            'NAND', 'NOR'
        }
        
        self.operator_precedence = {
            '¬': 4, '~': 4, '!': 4,
            '∧': 3, '&': 3, '&&': 3, 'AND': 3,
            '∨': 2, '|': 2, '||': 2, 'OR': 2,
            '→': 1, '->': 1, '=>': 1, 'IMP': 1,
            '↔': 1, '<->': 1, '<=>': 1, 'XNOR': 1,
            '⊕': 2, '^': 2, 'XOR': 2,
            'NAND': 3, 'NOR': 2
        }
        
    def validate_expression(self, expression):
        """
        Validate logical expression syntax
        
        Args:
            expression (str): Logical expression to validate
            
        Returns:
            tuple: (is_valid, message)
        """
        if not expression or not expression.strip():
            return False, "Expression cannot be empty"
            
        expr = expression.strip()
        
        # Check for balanced parentheses
        if not self._check_balanced_parentheses(expr):
            return False, "Unbalanced parentheses"
            
        # Check for invalid characters
        invalid_chars = self._find_invalid_characters(expr)
        if invalid_chars:
            return False, f"Invalid characters: {', '.join(invalid_chars)}"
            
        # Check operator placement
        op_error = self._check_operator_placement(expr)
        if op_error:
            return False, op_error
            
        # Check variable names
        var_error = self._check_variable_names(expr)
        if var_error:
            return False, var_error
            
        return True, "Valid expression"
    
    def _check_balanced_parentheses(self, expression):
        """Check if parentheses are balanced"""
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return len(stack) == 0
    
    def _find_invalid_characters(self, expression):
        """Find invalid characters in expression"""
        # Allowed: letters, numbers (for constants), operators, parentheses, spaces
        pattern = r'[^A-Za-z0-9\s¬~!∧&∨|→↔⊕<>=\-\^\(\)]'
        invalid_matches = re.findall(pattern, expression)
        return list(set(invalid_matches))  # Return unique invalid characters
    
    def _check_operator_placement(self, expression):
        """Check for proper operator placement"""
        tokens = self._tokenize(expression)
        
        for i, token in enumerate(tokens):
            if self._is_operator(token):
                # Check binary operators (not at start/end)
                if token not in ['¬', '~', '!'] and (i == 0 or i == len(tokens) - 1):
                    return f"Binary operator '{token}' at invalid position"
                    
                # Check unary operators (must be followed by variable or '(')
                if token in ['¬', '~', '!'] and i == len(tokens) - 1:
                    return f"Unary operator '{token}' at end of expression"
                    
        return None
    
    def _check_variable_names(self, expression):
        """Validate variable names"""
        tokens = self._tokenize(expression)
        
        for token in tokens:
            if self._is_variable(token) and len(token) > 1 and not token.isdigit():
                # Multi-character tokens should be valid operators or constants
                if token not in self.operators and token not in ['0', '1', 'true', 'false', 'TRUE', 'FALSE']:
                    return f"Invalid variable/operator name: '{token}'"
                    
        return None
    
    def _tokenize(self, expression):
        """Tokenize the expression into operators, variables, and parentheses"""
        # Replace multi-character operators with placeholders
        expr = expression.upper()
        replacements = {
            '&&': ' ∧ ', ' AND ': ' ∧ ',
            '||': ' ∨ ', ' OR ': ' ∨ ',
            '->': ' → ', '=>': ' → ', ' IMP ': ' → ',
            '<->': ' ↔ ', '<=>': ' ↔ ', ' XNOR ': ' ↔ ',
            ' XOR ': ' ⊕ ', ' NAND ': ' NAND ', ' NOR ': ' NOR '
        }
        
        for old, new in replacements.items():
            expr = expr.replace(old, new)
            
        # Tokenize
        tokens = re.findall(r'[A-Za-z0-9]+|[¬~!∧∨→↔⊕\(\)]', expr)
        return [token for token in tokens if token.strip()]
    
    def _is_operator(self, token):
        """Check if token is an operator"""
        return token.upper() in [op.upper() for op in self.operators] or token in ['(', ')']
    
    def _is_variable(self, token):
        """Check if token is a variable"""
        return token.isalpha() and len(token) == 1 and token.isupper()
    
    def extract_variables(self, expression):
        """
        Extract all unique variables from expression
        
        Args:
            expression (str): Logical expression
            
        Returns:
            set: Set of variable names
        """
        tokens = self._tokenize(expression)
        variables = set()
        
        for token in tokens:
            if self._is_variable(token):
                variables.add(token.upper())
                
        return variables
    
    def to_postfix(self, expression):
        """
        Convert infix expression to postfix (RPN) notation
        
        Args:
            expression (str): Infix logical expression
            
        Returns:
            list: Postfix expression tokens
        """
        tokens = self._tokenize(expression)
        output = []
        stack = []
        
        for token in tokens:
            if self._is_variable(token) or token in ['0', '1']:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
            else:  # Operator
                while (stack and stack[-1] != '(' and 
                       self.operator_precedence.get(token, 0) <= 
                       self.operator_precedence.get(stack[-1], 0)):
                    output.append(stack.pop())
                stack.append(token)
                
        while stack:
            output.append(stack.pop())
            
        return output
    
    def evaluate_expression(self, expression, variable_values):
        """
        Evaluate expression with given variable values
        
        Args:
            expression (str): Logical expression
            variable_values (dict): Variable to boolean mapping
            
        Returns:
            bool: Expression result
        """
        postfix = self.to_postfix(expression)
        stack = []
        
        for token in postfix:
            if self._is_variable(token) or token in ['0', '1']:
                if token in ['0', '1']:
                    stack.append(token == '1')
                else:
                    stack.append(variable_values.get(token.upper(), False))
            else:
                if token in ['¬', '~', '!']:  # Unary operator
                    if not stack:
                        raise ValueError("Invalid expression: missing operand for negation")
                    operand = stack.pop()
                    stack.append(not operand)
                else:  # Binary operator
                    if len(stack) < 2:
                        raise ValueError(f"Invalid expression: missing operands for operator '{token}'")
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(self._apply_operator(left, right, token))
                    
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return stack[0]
    
    def _apply_operator(self, left, right, operator):
        """Apply binary operator to operands"""
        operator = operator.upper()
        
        if operator in ['∧', '&', '&&', 'AND']:
            return left and right
        elif operator in ['∨', '|', '||', 'OR']:
            return left or right
        elif operator in ['→', '->', '=>', 'IMP']:
            return (not left) or right
        elif operator in ['↔', '<->', '<=>', 'XNOR']:
            return left == right
        elif operator in ['⊕', '^', 'XOR']:
            return left != right
        elif operator == 'NAND':
            return not (left and right)
        elif operator == 'NOR':
            return not (left or right)
        else:
            raise ValueError(f"Unknown operator: {operator}")