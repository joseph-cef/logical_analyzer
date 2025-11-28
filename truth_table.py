"""
Truth table generator for logical expressions
Handles table generation and evaluation
"""
from logic_parser import LogicParser
import itertools

class TruthTableGenerator:
    """Generates truth tables for logical expressions"""
    
    def __init__(self):
        self.parser = LogicParser()
    
    def generate_truth_table(self, expression):
        """
        Generate complete truth table for expression
        
        Args:
            expression (str): Logical expression
            
        Returns:
            tuple: (table_data, variables)
        """
        # Validate expression first
        is_valid, message = self.parser.validate_expression(expression)
        if not is_valid:
            raise ValueError(f"Invalid expression: {message}")
            
        # Extract variables
        variables = sorted(self.parser.extract_variables(expression))
        
        if not variables:
            # Handle expressions with constants only
            return self._generate_constant_truth_table(expression)
            
        # Generate all possible combinations
        combinations = list(itertools.product([False, True], repeat=len(variables)))
        
        table_data = []
        for combo in combinations:
            # Create variable assignment
            assignment = dict(zip(variables, combo))
            
            try:
                # Evaluate expression
                result = self.parser.evaluate_expression(expression, assignment)
                
                # Create row data
                row = assignment.copy()
                row['result'] = result
                table_data.append(row)
                
            except Exception as e:
                raise ValueError(f"Error evaluating expression: {str(e)}")
                
        return table_data, variables
    
    def _generate_constant_truth_table(self, expression):
        """Generate truth table for constant expressions"""
        try:
            # Evaluate with empty variables (uses constants only)
            result = self.parser.evaluate_expression(expression, {})
            
            table_data = [{'result': result}]
            variables = []
            
            return table_data, variables
            
        except Exception as e:
            raise ValueError(f"Error evaluating constant expression: {str(e)}")
    
    def get_truth_table_summary(self, table_data, variables):
        """
        Generate summary statistics for truth table
        
        Args:
            table_data (list): Truth table data
            variables (list): Variable names
            
        Returns:
            dict: Summary statistics
        """
        if not table_data:
            return {}
            
        true_count = sum(1 for row in table_data if row['result'])
        false_count = len(table_data) - true_count
        
        return {
            'total_rows': len(table_data),
            'true_count': true_count,
            'false_count': false_count,
            'is_tautology': true_count == len(table_data),
            'is_contradiction': false_count == len(table_data),
            'is_contingency': true_count > 0 and false_count > 0
        }
    
    def find_minterms(self, table_data, variables):
        """
        Find minterms (rows where result is True)
        
        Args:
            table_data (list): Truth table data
            variables (list): Variable names
            
        Returns:
            list: Minterm indices
        """
        minterms = []
        for i, row in enumerate(table_data):
            if row['result']:
                minterms.append(i)
        return minterms
    
    def find_maxterms(self, table_data, variables):
        """
        Find maxterms (rows where result is False)
        
        Args:
            table_data (list): Truth table data
            variables (list): Variable names
            
        Returns:
            list: Maxterm indices
        """
        maxterms = []
        for i, row in enumerate(table_data):
            if not row['result']:
                maxterms.append(i)
        return maxterms