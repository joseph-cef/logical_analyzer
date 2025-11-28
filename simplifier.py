"""
Logical expression simplifier
Uses Boolean algebra rules and Karnaugh maps for simplification
"""
import re
from itertools import product

class ExpressionSimplifier:
    """Simplifies logical expressions using Boolean algebra"""
    
    def __init__(self):
        self.rules = {
            # Identity laws
            'A ∧ 1': 'A',
            'A ∨ 0': 'A',
            
            # Domination laws  
            'A ∧ 0': '0',
            'A ∨ 1': '1',
            
            # Idempotent laws
            'A ∧ A': 'A',
            'A ∨ A': 'A',
            
            # Double negation
            '¬¬A': 'A',
            
            # Complement laws
            'A ∧ ¬A': '0',
            'A ∨ ¬A': '1',
            
            # Commutative laws
            'A ∧ B': 'B ∧ A',
            'A ∨ B': 'B ∨ A',
            
            # Associative laws  
            '(A ∧ B) ∧ C': 'A ∧ (B ∧ C)',
            '(A ∨ B) ∨ C': 'A ∨ (B ∨ C)',
            
            # Distributive laws
            'A ∧ (B ∨ C)': '(A ∧ B) ∨ (A ∧ C)',
            'A ∨ (B ∧ C)': '(A ∨ B) ∧ (A ∨ C)',
            
            # De Morgan's laws
            '¬(A ∧ B)': '¬A ∨ ¬B',
            '¬(A ∨ B)': '¬A ∧ ¬B',
            
            # Absorption laws
            'A ∧ (A ∨ B)': 'A',
            'A ∨ (A ∧ B)': 'A',
            
            # Implication elimination
            'A → B': '¬A ∨ B',
            
            # Biconditional elimination
            'A ↔ B': '(A → B) ∧ (B → A)',
            
            # XOR elimination
            'A ⊕ B': '(A ∧ ¬B) ∨ (¬A ∧ B)'
        }
    
    def simplify(self, expression):
        """
        Simplify logical expression using Boolean algebra rules
        
        Args:
            expression (str): Original logical expression
            
        Returns:
            tuple: (simplified_expression, steps)
        """
        steps = []
        current_expr = self._normalize_expression(expression)
        original_expr = current_expr
        
        steps.append(f"Original: {current_expr}")
        
        # Apply simplification rules iteratively
        changed = True
        iteration = 0
        max_iterations = 20
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            # Try each simplification rule
            for pattern, replacement in self.rules.items():
                new_expr = self._apply_rule(current_expr, pattern, replacement)
                if new_expr != current_expr:
                    steps.append(f"Applied {pattern} → {replacement}: {new_expr}")
                    current_expr = new_expr
                    changed = True
                    break  # Restart with new expression
                    
            # Remove redundant parentheses
            new_expr = self._remove_redundant_parentheses(current_expr)
            if new_expr != current_expr:
                steps.append(f"Removed redundant parentheses: {new_expr}")
                current_expr = new_expr
                changed = True
                
        # Final cleanup
        final_expr = self._cleanup_expression(current_expr)
        if final_expr != current_expr:
            steps.append(f"Final cleanup: {final_expr}")
            current_expr = final_expr
            
        return current_expr, steps
    
    def _normalize_expression(self, expression):
        """Normalize expression to standard format"""
        # Convert to uppercase and standard operators
        expr = expression.upper()
        
        replacements = {
            '&&': '∧', ' AND ': ' ∧ ',
            '||': '∨', ' OR ': ' ∨ ',
            '->': '→', '=>': '→',
            '<->': '↔', '<=>': '↔',
            '^': '⊕', ' XOR ': ' ⊕ ',
            '!': '¬', '~': '¬'
        }
        
        for old, new in replacements.items():
            expr = expr.replace(old, new)
            
        # Ensure proper spacing around operators
        operators = ['∧', '∨', '→', '↔', '⊕', '¬']
        for op in operators:
            expr = expr.replace(op, f' {op} ')
            
        # Clean up multiple spaces
        expr = re.sub(r'\s+', ' ', expr).strip()
        
        return expr
    
    def _apply_rule(self, expression, pattern, replacement):
        """Apply a single simplification rule"""
        # Simple string replacement for basic rules
        if expression == pattern:
            return replacement
            
        # Handle patterns with variables
        if 'A' in pattern or 'B' in pattern or 'C' in pattern:
            return self._apply_variable_rule(expression, pattern, replacement)
            
        return expression
    
    def _apply_variable_rule(self, expression, pattern, replacement):
        """Apply rule with variable placeholders"""
        # This is a simplified implementation
        # A full implementation would need pattern matching with variables
        
        # For now, just do simple replacements
        if pattern in expression:
            return expression.replace(pattern, replacement)
            
        return expression
    
    def _remove_redundant_parentheses(self, expression):
        """Remove redundant parentheses from expression"""
        # Simple implementation - remove parentheses around single variables
        expr = expression
        
        # Remove parentheses around single letters/constants
        expr = re.sub(r'\(([A-Z01])\)', r'\1', expr)
        
        # Remove outer parentheses if they wrap the entire expression
        if expr.startswith('(') and expr.endswith(')'):
            inner = expr[1:-1]
            if self._is_balanced(inner):
                expr = inner
                
        return expr
    
    def _is_balanced(self, expression):
        """Check if parentheses are balanced"""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0
    
    def _cleanup_expression(self, expression):
        """Clean up the final expression"""
        expr = expression
        
        # Remove extra spaces
        expr = re.sub(r'\s+', ' ', expr).strip()
        
        # Ensure proper operator spacing
        operators = ['∧', '∨', '→', '↔', '⊕']
        for op in operators:
            expr = expr.replace(f' {op} ', op)
            
        # Add spaces around binary operators for readability
        for op in operators:
            expr = expr.replace(op, f' {op} ')
            
        # Clean up again
        expr = re.sub(r'\s+', ' ', expr).strip()
        
        return expr
    
    def simplify_with_karnaugh(self, expression, variables):
        """
        Simplify using Karnaugh maps (basic implementation)
        
        Args:
            expression (str): Logical expression
            variables (list): List of variables
            
        Returns:
            str: Simplified expression
        """
        # This is a placeholder for Karnaugh map implementation
        # A full implementation would involve:
        # 1. Generating truth table
        # 2. Creating K-map
        # 3. Finding prime implicants
        # 4. Generating minimal expression
        
        # For now, return the algebraically simplified expression
        simplified, _ = self.simplify(expression)
        return simplified
    
    def get_simplification_stats(self, original, simplified):
        """
        Get statistics about simplification
        
        Args:
            original (str): Original expression
            simplified (str): Simplified expression
            
        Returns:
            dict: Simplification statistics
        """
        orig_length = len(original)
        simp_length = len(simplified)
        
        return {
            'original_length': orig_length,
            'simplified_length': simp_length,
            'reduction_percent': ((orig_length - simp_length) / orig_length * 100) if orig_length > 0 else 0,
            'reduction_ratio': simp_length / orig_length if orig_length > 0 else 1
        }