import tkinter as tk
from tkinter import ttk

class LogicGateSimulator:
    """
    A GUI-based simulator for the basic logic gates (AND, OR, NOT, XOR)
    using Python's Tkinter library.
    
    Includes a feature to display the full truth table for the selected gate,
    and visualizes the gate using its standard schematic symbol.
    """

    def __init__(self, root):
        self.root = root
        root.title("Digital Logic Gate Simulator with Truth Table (Basic Gates)")
        root.geometry("700x500") 
        root.configure(bg='#e0f2fe')

        # --- State Variables ---
        self.selected_gate = tk.StringVar(value="AND")
        self.input_a = tk.IntVar(value=0)
        self.input_b = tk.IntVar(value=0)
        self.output_y = tk.IntVar(value=0)

        # --- Gate Logic Dictionary ---
        self.logic_functions = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "NOT": lambda a, b: 1 - a, 
            "XOR": lambda a, b: a ^ b,
        }

        # --- Setup UI Components ---
        self.setup_styles()
        self.create_widgets()
        self.update_output() # Initial calculation

    def setup_styles(self):
        """Configure custom styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam') 
        
        style.configure('TFrame', background='#e0f2fe')
        style.configure('TLabel', background='#e0f2fe', font=('Inter', 12))
        style.configure('TButton', font=('Inter', 11, 'bold'), padding=10, 
                        background='#0284c7', foreground='white', relief='flat')
        style.map('TButton', background=[('active', '#075985')], relief=[('pressed', 'groove')])
        
        style.configure('Gate.TLabel', font=('Inter', 18, 'bold'), foreground='#052e16', background='#ccfbf1', padding=15, relief='raised')
        style.configure('Input.TLabel', font=('Inter', 14, 'bold'), foreground='#1e3a8a')
        style.configure('Output.TLabel', font=('Inter', 16, 'bold'), foreground='#be123c')
        
        # Style for the Truth Table Treeview
        style.configure("Treeview.Heading", font=('Inter', 12, 'bold'), background='#0284c7', foreground='white')
        style.configure("Treeview", font=('Inter', 11), rowheight=25, fieldbackground='#f0f9ff')


    def create_widgets(self):
        """Build the main layout of the application."""
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        # 1. Gate Selection and Information Frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=10, fill='x')

        ttk.Label(info_frame, text="Select Gate:", font=('Inter', 12, 'bold')).pack(side='left', padx=10)
        
        gate_options = ["AND", "OR", "NOT", "XOR"] 
        gate_menu = ttk.OptionMenu(info_frame, self.selected_gate, self.selected_gate.get(), 
                                   *gate_options, command=self.on_gate_change)
        gate_menu.pack(side='left', padx=10)
        
        ttk.Button(info_frame, text="Show Truth Table", command=self.show_truth_table).pack(side='left', padx=20)
        
        self.gate_display_label = ttk.Label(info_frame, textvariable=self.selected_gate, style='Gate.TLabel')
        self.gate_display_label.pack(side='right', padx=10)

        # 2. Simulator Area Frame (Inputs and Output)
        simulator_frame = ttk.Frame(main_frame)
        simulator_frame.pack(pady=20, fill='x', expand=False)
        
        # --- Input A Controls ---
        input_a_frame = ttk.Frame(simulator_frame, padding=10)
        input_a_frame.pack(side='left', padx=30, expand=True, fill='y')
        
        ttk.Label(input_a_frame, text="Input A:", style='Input.TLabel').pack(pady=5)
        self.label_a = ttk.Label(input_a_frame, textvariable=self.input_a, style='Input.TLabel', font=('Inter', 24, 'bold'))
        self.label_a.pack(pady=10)
        
        self.button_a = ttk.Button(input_a_frame, text="Toggle A (0 ⇌ 1)", command=lambda: self.toggle_input('A'))
        self.button_a.pack(pady=10)
        
        # --- Input B Controls ---
        input_b_frame = ttk.Frame(simulator_frame, padding=10)
        input_b_frame.pack(side='left', padx=30, expand=True, fill='y')

        ttk.Label(input_b_frame, text="Input B:", style='Input.TLabel').pack(pady=5)
        self.label_b = ttk.Label(input_b_frame, textvariable=self.input_b, style='Input.TLabel', font=('Inter', 24, 'bold'))
        self.label_b.pack(pady=10)
        
        self.button_b = ttk.Button(input_b_frame, text="Toggle B (0 ⇌ 1)", command=lambda: self.toggle_input('B'))
        self.button_b.pack(pady=10)

        # --- Output Y Display ---
        output_frame = ttk.Frame(simulator_frame, padding=10)
        output_frame.pack(side='right', padx=30, expand=True, fill='y')
        
        ttk.Label(output_frame, text="Output Y:", style='Output.TLabel').pack(pady=5)
        self.label_y = ttk.Label(output_frame, textvariable=self.output_y, style='Output.TLabel', font=('Inter', 36, 'bold'))
        self.label_y.pack(pady=10)

        # 3. Canvas for Schematic Visualization
        self.canvas = tk.Canvas(main_frame, height=150, bg='#fff', bd=2, relief='sunken')
        self.canvas.pack(pady=15, padx=10, fill='x', expand=True)
        self.canvas.bind('<Configure>', self.handle_resize)

        self.on_gate_change(self.selected_gate.get())

    def handle_resize(self, event):
        """Redraws the diagram when the canvas changes size."""
        self.draw_gate_diagram()

    def toggle_input(self, input_name):
        """Flips the value of the specified input (A or B) and recalculates."""
        if input_name == 'A':
            current_val = self.input_a.get()
            self.input_a.set(1 - current_val)
        elif input_name == 'B':
            current_val = self.input_b.get()
            self.input_b.set(1 - current_val)
        
        self.update_output()

    def on_gate_change(self, gate_name):
        """Called when a new gate is selected."""
        self.draw_gate_diagram()
        
        # Enable/Disable Input B based on NOT gate selection
        if gate_name == "NOT":
            self.button_b.state(['disabled'])
            self.input_b.set(0) # Ensure B is 0 for NOT gate
            self.label_b.configure(text="N/A")
        else:
            self.button_b.state(['!disabled'])
            self.label_b.configure(textvariable=self.input_b)
        
        self.update_output()

    def update_output(self):
        """
        Calculates the output based on current gate selection and inputs,
        then updates the display and diagram.
        """
        gate_func = self.logic_functions[self.selected_gate.get()]
        a = self.input_a.get()
        b = self.input_b.get()
        
        new_output = gate_func(a, b)
        self.output_y.set(new_output)
        
        self.draw_gate_diagram()

    def calculate_truth_table(self):
        """Generates the truth table data for the currently selected gate."""
        gate_name = self.selected_gate.get()
        func = self.logic_functions[gate_name]
        table_data = []

        if gate_name == "NOT":
            input_combinations = [(0,), (1,)]
            for a_val in input_combinations:
                output = func(a_val[0], 0) 
                table_data.append((a_val[0], 'N/A', output))
        else:
            input_combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]
            for a_val, b_val in input_combinations:
                output = func(a_val, b_val)
                table_data.append((a_val, b_val, output))
                
        return table_data

    def show_truth_table(self):
        """Creates and displays a new window with the truth table."""
        gate_name = self.selected_gate.get()
        table_data = self.calculate_truth_table()
        
        tt_window = tk.Toplevel(self.root)
        tt_window.title(f"{gate_name} Gate Truth Table")
        tt_window.configure(bg='#f0f9ff')
        tt_window.resizable(False, False)

        columns = ("#1", "#2", "#3")
        headings = ("Input A", "Input B", "Output Y")
        width_map = [100, 100, 100]

        tree = ttk.Treeview(tt_window, columns=columns, show='headings', height=len(table_data))
        tree.pack(padx=20, pady=20, fill='both', expand=True)

        for i, col in enumerate(columns):
            tree.heading(col, text=headings[i])
            tree.column(col, anchor='center', width=width_map[i])

        for row in table_data:
            match_a = row[0] == self.input_a.get()
            match_b = str(row[1]) == str(self.input_b.get()) or str(row[1]) == 'N/A'
            
            tag = 'highlight' if match_a and match_b else ''
            
            tree.insert('', tk.END, values=row, tags=(tag,))

        tree.tag_configure('highlight', background='#fff8e1', foreground='#616161')

        tt_window.update_idletasks()
        width = tt_window.winfo_width()
        height = tt_window.winfo_height()
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - width // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - height // 2
        tt_window.geometry(f'+{x}+{y}')

    def draw_gate_diagram(self):
        """Draws the standard schematic symbol of the current gate on the canvas."""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        
        # Dimensions
        GATE_BODY_WIDTH = 80 # Width of the main gate body
        GATE_BODY_HEIGHT = 60
        LINE_LENGTH = 45
        
        gate_name = self.selected_gate.get()
        output_val = self.output_y.get()
        input_a_val = self.input_a.get()
        input_b_val = self.input_b.get()

        # Wire Colors (Green for 1/True, Gray for 0/False)
        COLOR_HIGH = '#4ade80' 
        COLOR_LOW = '#9ca3af'  
        LINE_WIDTH = 3
        
        color_a = COLOR_HIGH if input_a_val == 1 else COLOR_LOW
        # Input B is considered LOW if NOT gate is selected (or if input_b is 0)
        color_b = COLOR_HIGH if input_b_val == 1 and gate_name != "NOT" else COLOR_LOW
        color_y = COLOR_HIGH if output_val == 1 else COLOR_LOW
        
        # Gate Drawing Parameters
        FILL_COLOR = '#a5f3fc'
        OUTLINE_COLOR = '#06b6d4'
        
        # Style for drawing the border/outline of shapes (arc, oval, polygon)
        SHAPE_OUTLINE_STYLE = {'outline': OUTLINE_COLOR, 'width': 2}
        # Style for drawing standalone lines (which use 'fill' for color)
        LINE_DRAW_STYLE = {'fill': OUTLINE_COLOR, 'width': 2}
        
        # Input reference point (start of the gate shape)
        x_start_gate = center_x - GATE_BODY_WIDTH // 2 
        y1 = center_y - GATE_BODY_HEIGHT // 2
        y2 = center_y + GATE_BODY_HEIGHT // 2
        
        # --- Drawing the specific gate symbol ---
        
        x_out_start = center_x + GATE_BODY_WIDTH // 2 # Default output start

        if gate_name == "AND":
            x_out_start = x_start_gate + GATE_BODY_WIDTH
            
            # 1. Back vertical line (Uses LINE_DRAW_STYLE, as create_line needs 'fill')
            self.canvas.create_line(x_start_gate, y1, x_start_gate, y2, **LINE_DRAW_STYLE)
            
            # 2. Semicircle front (D-shape) (Uses SHAPE_OUTLINE_STYLE, as create_arc needs 'outline')
            d_shape_box = (x_start_gate - GATE_BODY_HEIGHT/2, y1, x_start_gate + GATE_BODY_WIDTH, y2)
            self.canvas.create_arc(d_shape_box, start=270, extent=180, style=tk.ARC, **SHAPE_OUTLINE_STYLE)
            
            # 3. Fill the body with a simple rectangle approximation
            self.canvas.create_rectangle(x_start_gate, y1, x_start_gate + GATE_BODY_WIDTH, y2, fill=FILL_COLOR, outline='')
            
        elif gate_name == "OR" or gate_name == "XOR":
            # OR/XOR uses a complex arc shape. Using polygons and arcs for a reasonable representation.
            
            x_back_curve = x_start_gate - 15 # X for the deepest part of the back curve
            x_front_tip = x_start_gate + GATE_BODY_WIDTH - 5 # X for the output tip

            # 1. Back Arc (Input Curve) - Drawn as straight segments for simplicity (Uses LINE_DRAW_STYLE)
            self.canvas.create_line(x_start_gate, y1, x_start_gate+25, y1, **LINE_DRAW_STYLE)
            self.canvas.create_line(x_start_gate, y2, x_start_gate+25, y2, **LINE_DRAW_STYLE)
            
            # 2. Outer/Front Arc (Output Curve) (Uses SHAPE_OUTLINE_STYLE)
            # Two arcs form the front curve meeting at the tip
            self.canvas.create_arc(x_back_curve, y1, x_front_tip + 30, center_y, start=330, extent=30, style=tk.ARC, **SHAPE_OUTLINE_STYLE)
            self.canvas.create_arc(x_back_curve, center_y, x_front_tip + 30, y2, start=30, extent=30, style=tk.ARC, **SHAPE_OUTLINE_STYLE)
            
            # 3. Fill the body (Simplified polygon fill)
            self.canvas.create_polygon([x_start_gate, y1, x_start_gate + GATE_BODY_WIDTH - 20, y1, x_front_tip, center_y, x_start_gate + GATE_BODY_WIDTH - 20, y2, x_start_gate, y2], fill=FILL_COLOR, outline='')

            x_out_start = x_front_tip
            
            if gate_name == "XOR":
                # Add the XOR input curve (parallel curve) (Uses SHAPE_OUTLINE_STYLE)
                self.canvas.create_arc(x_start_gate - 25, y1, x_start_gate + 5, y2, 
                                       start=270, extent=180, style=tk.ARC, **SHAPE_OUTLINE_STYLE)
                                       
        elif gate_name == "NOT":
            x_tri_end = x_start_gate + 40 # End of the triangle body
            
            # 1. Triangle (Buffer) (Uses SHAPE_OUTLINE_STYLE)
            self.canvas.create_polygon(x_start_gate, center_y, # Input Point
                                       x_tri_end, y1,         # Top Point
                                       x_tri_end, y2,         # Bottom Point
                                       fill=FILL_COLOR, **SHAPE_OUTLINE_STYLE)
                                       
            # 2. Inverter Bubble
            BUBBLE_RADIUS = 5
            self.canvas.create_oval(x_tri_end, center_y - BUBBLE_RADIUS, 
                                    x_tri_end + BUBBLE_RADIUS * 2, center_y + BUBBLE_RADIUS, 
                                    outline=OUTLINE_COLOR, width=2, fill='white')
            
            x_out_start = x_tri_end + BUBBLE_RADIUS * 2
        
        
        # --- 4. Draw Wires and Labels ---

        # Input A Line and Label
        if gate_name == "NOT":
            y_a = center_y
        else:
            y_a = center_y - GATE_BODY_HEIGHT/4 

        self.canvas.create_line(x_start_gate - LINE_LENGTH, y_a, x_start_gate, y_a, fill=color_a, width=LINE_WIDTH, tags="wire_a")
        self.canvas.create_text(x_start_gate - LINE_LENGTH - 10, y_a, anchor='e', text=f"A ({input_a_val})", font=('Inter', 12, 'bold'), fill=color_a)
        
        # Input B Line and Label (only for 2-input gates)
        if gate_name != "NOT":
            y_b = center_y + GATE_BODY_HEIGHT/4
            self.canvas.create_line(x_start_gate - LINE_LENGTH, y_b, x_start_gate, y_b, fill=color_b, width=LINE_WIDTH, tags="wire_b")
            self.canvas.create_text(x_start_gate - LINE_LENGTH - 10, y_b, anchor='e', text=f"B ({input_b_val})", font=('Inter', 12, 'bold'), fill=color_b)
        else:
            y_b = center_y + GATE_BODY_HEIGHT/4 
            self.canvas.create_text(x_start_gate - LINE_LENGTH - 10, y_b, anchor='e', text="B (N/A)", font=('Inter', 12), fill='#9ca3af')
            
        # Output Y Line and Label
        self.canvas.create_line(x_out_start, center_y, x_out_start + LINE_LENGTH, center_y, fill=color_y, width=LINE_WIDTH, tags="wire_y")
        self.canvas.create_text(x_out_start + LINE_LENGTH + 10, center_y, anchor='w', text=f"Y ({output_val})", font=('Inter', 14, 'bold'), fill=color_y)

if __name__ == '__main__':
    # Initialize the main Tkinter window
    root = tk.Tk()
    
    # Create an instance of the simulator application
    app = LogicGateSimulator(root)
    
    # Start the Tkinter event loop
    root.mainloop()