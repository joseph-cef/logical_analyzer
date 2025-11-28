"""
Modern GUI implementation using CustomTkinter
Handles all user interface components and interactions
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from logic_parser import LogicParser
from truth_table import TruthTableGenerator
from simplifier import ExpressionSimplifier
import csv
import os

class LogicalAnalyzerApp:
    """Main application class for the Logical Expression Analyzer"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_theme()
        self.create_widgets()
        self.initialize_components()
        
    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("Logical Expression Analyzer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
    def setup_theme(self):
        """Initialize theme and appearance settings"""
        ctk.set_appearance_mode("Dark")  # Default to dark mode
        ctk.set_default_color_theme("blue")
        
    def initialize_components(self):
        """Initialize business logic components"""
        self.parser = LogicParser()
        self.truth_table_gen = TruthTableGenerator()
        self.simplifier = ExpressionSimplifier()
        
    def create_widgets(self):
        """Create all GUI widgets and layout"""
        self.create_main_frame()
        self.create_header()
        self.create_input_section()
        self.create_logical_keyboard()
        self.create_results_notebook()
        self.create_status_bar()
        
    def create_main_frame(self):
        """Create the main container frame"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_header(self):
        """Create the header section with title and controls"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Logical Expression Analyzer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Theme switch
        self.theme_var = ctk.StringVar(value="Dark")
        theme_switch = ctk.CTkSwitch(
            header_frame,
            text="Light Mode",
            variable=self.theme_var,
            onvalue="Light",
            offvalue="Dark",
            command=self.toggle_theme
        )
        theme_switch.pack(side=tk.RIGHT, padx=10, pady=10)
        
    def create_input_section(self):
        """Create expression input section"""
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input label
        input_label = ctk.CTkLabel(
            input_frame,
            text="Enter Logical Expression:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Input field with validation
        input_inner_frame = ctk.CTkFrame(input_frame)
        input_inner_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.expression_var = ctk.StringVar()
        self.expression_entry = ctk.CTkEntry(
            input_inner_frame,
            textvariable=self.expression_var,
            placeholder_text="e.g., (A ∧ B) ∨ ¬C",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.expression_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.expression_entry.bind("<KeyRelease>", self.validate_expression)
        
        # Parse button
        self.parse_button = ctk.CTkButton(
            input_inner_frame,
            text="Parse Expression",
            command=self.parse_expression,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=120,
            height=35
        )
        self.parse_button.pack(side=tk.RIGHT)
        
        # Validation label
        self.validation_label = ctk.CTkLabel(
            input_frame,
            text="",
            font=ctk.CTkFont(size=11)
        )
        self.validation_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
    def create_logical_keyboard(self):
        """Create virtual logical keyboard"""
        keyboard_frame = ctk.CTkFrame(self.main_frame)
        keyboard_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Keyboard label
        keyboard_label = ctk.CTkLabel(
            keyboard_frame,
            text="Logical Keyboard:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        keyboard_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Keyboard buttons
        buttons_frame = ctk.CTkFrame(keyboard_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Logical operators in rows
        operators = [
            # Row 1: Basic operators
            ["¬", "∧", "∨", "→", "↔"],
            # Row 2: Advanced operators
            ["⊕", "XOR", "NAND", "NOR"],
            # Row 3: Parentheses and common symbols
            ["(", ")", "[", "]", "{", "}"],
            # Row 4: Variables A-J
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            # Row 5: Variables K-T  
            ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
            # Row 6: Variables U-Z and constants
            ["U", "V", "W", "X", "Y", "Z", "1", "0"]
        ]
        
        for row_ops in operators:
            row_frame = ctk.CTkFrame(buttons_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            for op in row_ops:
                btn = ctk.CTkButton(
                    row_frame,
                    text=op,
                    width=40,
                    height=30,
                    font=ctk.CTkFont(size=11),
                    command=lambda o=op: self.insert_operator(o)
                )
                btn.pack(side=tk.LEFT, padx=2)
                
            # Add some spacing between rows
            row_frame.pack_configure(pady=1)
            
        # Control buttons row
        control_frame = ctk.CTkFrame(buttons_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        clear_btn = ctk.CTkButton(
            control_frame,
            text="Clear",
            command=self.clear_expression,
            width=80,
            height=30,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        backspace_btn = ctk.CTkButton(
            control_frame,
            text="⌫",
            command=self.backspace,
            width=60,
            height=30
        )
        backspace_btn.pack(side=tk.LEFT, padx=2)
        
        space_btn = ctk.CTkButton(
            control_frame,
            text="Space",
            command=lambda: self.insert_operator(" "),
            width=80,
            height=30
        )
        space_btn.pack(side=tk.LEFT, padx=2)
        
    def create_results_notebook(self):
        """Create tabbed results area"""
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Truth Table tab
        self.truth_table_tab = self.notebook.add("Truth Table")
        self.setup_truth_table_tab()
        
        # Simplification tab
        self.simplification_tab = self.notebook.add("Simplification")
        self.setup_simplification_tab()
        
    def setup_truth_table_tab(self):
        """Setup truth table tab content"""
        # Control frame
        control_frame = ctk.CTkFrame(self.truth_table_tab)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        generate_btn = ctk.CTkButton(
            control_frame,
            text="Generate Truth Table",
            command=self.generate_truth_table,
            font=ctk.CTkFont(weight="bold")
        )
        generate_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        export_btn = ctk.CTkButton(
            control_frame,
            text="Export CSV",
            command=self.export_truth_table,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        export_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Table frame
        table_frame = ctk.CTkFrame(self.truth_table_tab)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview with scrollbars
        self.setup_truth_table_widgets(table_frame)
        
    def setup_truth_table_widgets(self, parent):
        """Setup truth table treeview and scrollbars"""
        # Create scrollbars
        v_scrollbar = ctk.CTkScrollbar(parent, orientation=tk.VERTICAL)
        h_scrollbar = ctk.CTkScrollbar(parent, orientation=tk.HORIZONTAL)
        
        # Create treeview
        self.truth_tree = ttk.Treeview(
            parent,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            show='headings',
            style="Custom.Treeview"
        )
        
        # Configure scrollbars
        v_scrollbar.configure(command=self.truth_tree.yview)
        h_scrollbar.configure(command=self.truth_tree.xview)
        
        # Pack widgets
        self.truth_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure style for alternating colors
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       rowheight=25,
                       font=('TkDefaultFont', 10))
        style.map("Custom.Treeview",
                 background=[('selected', '#347083')])
        
    def setup_simplification_tab(self):
        """Setup simplification tab content"""
        # Control frame
        control_frame = ctk.CTkFrame(self.simplification_tab)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        simplify_btn = ctk.CTkButton(
            control_frame,
            text="Simplify Expression",
            command=self.simplify_expression,
            font=ctk.CTkFont(weight="bold")
        )
        simplify_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Results frame
        results_frame = ctk.CTkFrame(self.simplification_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Original expression
        orig_frame = ctk.CTkFrame(results_frame)
        orig_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(orig_frame, text="Original Expression:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        self.original_expr_text = ctk.CTkTextbox(orig_frame, height=40)
        self.original_expr_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.original_expr_text.configure(state="disabled")
        
        # Simplified expression
        simplified_frame = ctk.CTkFrame(results_frame)
        simplified_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(simplified_frame, text="Simplified Expression:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        self.simplified_expr_text = ctk.CTkTextbox(simplified_frame, height=40)
        self.simplified_expr_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.simplified_expr_text.configure(state="disabled")
        
        # Steps (optional)
        steps_frame = ctk.CTkFrame(results_frame)
        steps_frame.pack(fill=tk.BOTH, expand=True)
        
        ctk.CTkLabel(steps_frame, text="Simplification Steps:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        self.steps_text = ctk.CTkTextbox(steps_frame)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.steps_text.configure(state="disabled")
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_frame = ctk.CTkFrame(self.main_frame, height=25)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        ctk.set_appearance_mode(self.theme_var.get())
        
    def insert_operator(self, operator):
        """Insert operator at current cursor position"""
        current = self.expression_var.get()
        cursor_pos = self.expression_entry.index(tk.INSERT)
        
        new_text = current[:cursor_pos] + operator + current[cursor_pos:]
        self.expression_var.set(new_text)
        
        # Move cursor after inserted text
        new_cursor_pos = cursor_pos + len(operator)
        self.expression_entry.icursor(new_cursor_pos)
        self.expression_entry.focus()
        
        self.validate_expression()
        
    def clear_expression(self):
        """Clear the expression entry"""
        self.expression_var.set("")
        self.validation_label.configure(text="")
        self.expression_entry.focus()
        
    def backspace(self):
        """Remove character before cursor"""
        current = self.expression_var.get()
        cursor_pos = self.expression_entry.index(tk.INSERT)
        
        if cursor_pos > 0:
            new_text = current[:cursor_pos-1] + current[cursor_pos:]
            self.expression_var.set(new_text)
            self.expression_entry.icursor(cursor_pos-1)
            
        self.validate_expression()
        
    def validate_expression(self, event=None):
        """Validate expression in real-time"""
        expression = self.expression_var.get()
        
        if not expression:
            self.validation_label.configure(text="")
            return
            
        try:
            is_valid, message = self.parser.validate_expression(expression)
            if is_valid:
                self.validation_label.configure(text="✓ Valid expression", text_color="#27AE60")
            else:
                self.validation_label.configure(text=f"⚠ {message}", text_color="#F39C12")
        except Exception as e:
            self.validation_label.configure(text=f"✗ Error: {str(e)}", text_color="#E74C3C")
            
    def parse_expression(self):
        """Parse the current expression"""
        expression = self.expression_var.get().strip()
        
        if not expression:
            messagebox.showwarning("Input Error", "Please enter a logical expression")
            return
            
        try:
            is_valid, message = self.parser.validate_expression(expression)
            if not is_valid:
                messagebox.showerror("Validation Error", f"Invalid expression: {message}")
                return
                
            # Extract variables for display
            variables = self.parser.extract_variables(expression)
            self.update_status(f"Parsed expression with variables: {', '.join(sorted(variables))}")
            messagebox.showinfo("Success", f"Expression parsed successfully!\nVariables: {', '.join(sorted(variables))}")
            
        except Exception as e:
            messagebox.showerror("Parsing Error", f"Error parsing expression: {str(e)}")
            
    def generate_truth_table(self):
        """Generate and display truth table"""
        expression = self.expression_var.get().strip()
        
        if not expression:
            messagebox.showwarning("Input Error", "Please enter a logical expression first")
            return
            
        try:
            # Clear existing table
            for item in self.truth_tree.get_children():
                self.truth_tree.delete(item)
            self.truth_tree["columns"] = []
            
            # Generate truth table
            table_data, variables = self.truth_table_gen.generate_truth_table(expression)
            
            if not table_data:
                messagebox.showerror("Error", "Could not generate truth table")
                return
                
            # Setup columns
            columns = variables + ['Result']
            self.truth_tree["columns"] = columns
            
            # Configure columns
            for col in columns:
                self.truth_tree.heading(col, text=col)
                self.truth_tree.column(col, width=80, anchor=tk.CENTER)
                
            # Insert data with alternating colors
            for i, row in enumerate(table_data):
                values = [str(row[var]) for var in variables] + [str(row['result'])]
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.truth_tree.insert("", tk.END, values=values, tags=(tag,))
                
            # Configure tags for alternating colors
            self.truth_tree.tag_configure('evenrow', background='#2B2B2B')
            self.truth_tree.tag_configure('oddrow', background='#3B3B3B')
            
            self.update_status(f"Generated truth table with {len(table_data)} rows")
            
        except Exception as e:
            messagebox.showerror("Generation Error", f"Error generating truth table: {str(e)}")
            
    def export_truth_table(self):
        """Export truth table to CSV file"""
        if not self.truth_tree.get_children():
            messagebox.showwarning("Export Error", "No truth table to export")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                # Get column headers
                columns = self.truth_tree["columns"]
                
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns)
                    
                    # Write data
                    for item in self.truth_tree.get_children():
                        values = [self.truth_tree.item(item)['values'][i] for i in range(len(columns))]
                        writer.writerow(values)
                        
                self.update_status(f"Truth table exported to {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Truth table exported successfully to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting file: {str(e)}")
            
    def simplify_expression(self):
        """Simplify the logical expression"""
        expression = self.expression_var.get().strip()
        
        if not expression:
            messagebox.showwarning("Input Error", "Please enter a logical expression first")
            return
            
        try:
            # Validate expression first
            is_valid, message = self.parser.validate_expression(expression)
            if not is_valid:
                messagebox.showerror("Validation Error", f"Invalid expression: {message}")
                return
                
            # Simplify expression
            simplified, steps = self.simplifier.simplify(expression)
            
            # Display results
            self.display_simplification_results(expression, simplified, steps)
            self.update_status("Expression simplified successfully")
            
        except Exception as e:
            messagebox.showerror("Simplification Error", f"Error simplifying expression: {str(e)}")
            
    def display_simplification_results(self, original, simplified, steps):
        """Display simplification results in the UI"""
        # Original expression
        self.original_expr_text.configure(state="normal")
        self.original_expr_text.delete(1.0, tk.END)
        self.original_expr_text.insert(1.0, original)
        self.original_expr_text.configure(state="disabled")
        
        # Simplified expression
        self.simplified_expr_text.configure(state="normal")
        self.simplified_expr_text.delete(1.0, tk.END)
        self.simplified_expr_text.insert(1.0, simplified)
        self.simplified_expr_text.configure(state="disabled")
        
        # Steps
        self.steps_text.configure(state="normal")
        self.steps_text.delete(1.0, tk.END)
        
        if steps:
            for i, step in enumerate(steps, 1):
                self.steps_text.insert(tk.END, f"Step {i}: {step}\n\n")
        else:
            self.steps_text.insert(tk.END, "No simplification steps available or expression already simplified.")
            
        self.steps_text.configure(state="disabled")
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=message)