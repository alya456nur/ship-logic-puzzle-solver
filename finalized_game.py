import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font

class ShipPuzzleSolver:
    def __init__(self):
        self.reset()
        self.clues = [
            "1. The Greek ship leaves at six and carries coffee.",
            "2. The ship in the middle has black chimney.",
            "3. The English ship leaves at nine.",
            "4. French ship with blue chimney is to the left of a ship that carries coffee.",
            "5. To the right of the ship carrying Cocoa is a ship going to Marseille.",
            "6. The Brazilian ship is heading for Manila.",
            "7. Next to the ship carrying rice is a ship with a green chimney.",
            "8. A ship going to Genoa leaves at five.",
            "9. The Spanish ship leaves at seven and is to the right of the sip going to Marseille.",
            "10. The ship with a red chimney goes to Hamburg.",
            "11. Next to the ship leaving at seven is a ship with white chimney.",
            "12. The ship on the border carries corn.",
            "13. The ship with a black chimney leaves at eight",
            "14. The ship carrying corn is anchored next to the ship carrying rice.",
            "15. The ship to Hamburg leaves at six."
        ]
        self.solution_found = False
        self.deduction_steps = []

    def reset(self):
        self.positions = {i: {
            'Nationality': None,
            'Departure Time': None,
            'Cargo': None,
            'Chimney': None,
            'Destination': None
        } for i in range(1, 6)}
        self.steps = []
        self.solution_found = False
        self.deduction_steps = []

    def apply_deduction(self, step, pos, attribute, value):
        self.positions[pos][attribute] = value
        self.steps.append(f"STEP {step}: {pos} = {value} ({attribute})")
        self.deduction_steps[-1]['assignments'].append((pos, attribute, value))

    def check_solution(self):
        try:
            # First, ensure all cells are filled
            for pos in self.positions:
                for attr, val in self.positions[pos].items():
                    if val is None or str(val).strip() == "":
                        return False  # Incomplete

            # Normalize all entries to lowercase strings for comparison
            norm = lambda x: str(x).strip().lower()

            # Greek ship leaves at six and carries coffee
            for ship in self.positions.values():
                if norm(ship['Nationality']) == 'greek':
                    if norm(ship['Departure Time']) != '6' or norm(ship['Cargo']) != 'coffee':
                        return False

            # Middle ship has black chimney
            if norm(self.positions[3]['Chimney']) != 'black':
                return False

            # English ship leaves at 9
            for ship in self.positions.values():
                if norm(ship['Nationality']) == 'english':
                    if norm(ship['Departure Time']) != '9':
                        return False

            # French ship with blue chimney is to the left of the ship that carries coffee
            french_pos = coffee_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Nationality']) == 'french':
                    if norm(ship['Chimney']) != 'blue':
                        return False
                    french_pos = pos
                if norm(ship['Cargo']) == 'coffee':
                    coffee_pos = pos
            if french_pos is None or coffee_pos is None or french_pos >= coffee_pos:
                return False

            # To the right of cocoa ship is a ship going to Marseille
            cocoa_pos = marseille_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Cargo']) == 'cocoa':
                    cocoa_pos = pos
                if norm(ship['Destination']) == 'marseille':
                    marseille_pos = pos
            if cocoa_pos is None or marseille_pos is None or marseille_pos != cocoa_pos + 1:
                return False

            # Brazilian ship is heading to Manila
            for ship in self.positions.values():
                if norm(ship['Nationality']) == 'brazilian':
                    if norm(ship['Destination']) != 'manila':
                        return False

            # Next to rice is green chimney
            rice_pos = green_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Cargo']) == 'rice':
                    rice_pos = pos
                if norm(ship['Chimney']) == 'green':
                    green_pos = pos
            if rice_pos is None or green_pos is None or abs(rice_pos - green_pos) != 1:
                return False

            # Genoa leaves at 5
            for ship in self.positions.values():
                if norm(ship['Destination']) == 'genoa':
                    if norm(ship['Departure Time']) != '5':
                        return False

            # Spanish ship leaves at 7 and is to the right of Marseille ship
            spanish_pos = marseille_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Nationality']) == 'spanish':
                    if norm(ship['Departure Time']) != '7':
                        return False
                    spanish_pos = pos
                if norm(ship['Destination']) == 'marseille':
                    marseille_pos = pos
            if spanish_pos is None or marseille_pos is None or spanish_pos <= marseille_pos:
                return False

            # Red chimney goes to Hamburg
            for ship in self.positions.values():
                if norm(ship['Chimney']) == 'red':
                    if norm(ship['Destination']) != 'hamburg':
                        return False

            # Next to ship leaving at 7 is white chimney
            seven_pos = white_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Departure Time']) == '7':
                    seven_pos = pos
                if norm(ship['Chimney']) == 'white':
                    white_pos = pos
            if seven_pos is None or white_pos is None or abs(seven_pos - white_pos) != 1:
                return False

            # Border ship (1 or 5) carries corn
            if not (norm(self.positions[1]['Cargo']) == 'corn' or norm(self.positions[5]['Cargo']) == 'corn'):
                return False

            # Black chimney leaves at 8
            for ship in self.positions.values():
                if norm(ship['Chimney']) == 'black':
                    if norm(ship['Departure Time']) != '8':
                        return False

            # Corn next to rice
            corn_pos = rice_pos = None
            for pos, ship in self.positions.items():
                if norm(ship['Cargo']) == 'corn':
                    corn_pos = pos
                if norm(ship['Cargo']) == 'rice':
                    rice_pos = pos
            if corn_pos is None or rice_pos is None or abs(corn_pos - rice_pos) != 1:
                return False

            # Hamburg leaves at 6
            for ship in self.positions.values():
                if norm(ship['Destination']) == 'hamburg':
                    if norm(ship['Departure Time']) != '6':
                        return False

            self.solution_found = True
            return True

        except Exception as e:
            print("Error during solution check:", e)
            return False


    def auto_solve(self):
        self.reset()
        steps = [
            ("Clues 1, 10, and 15: Greek ship leaves at 6 with coffee and red chimney to Hamburg", [
                (2, 'Nationality', 'Greek'),
                (2, 'Departure Time', 6),
                (2, 'Cargo', 'coffee'),
                (2, 'Destination', 'Hamburg'),
                (2, 'Chimney', 'red')
            ]),
            ("Clues 2 and 13: Middle ship has black chimney and leaves at 8", [
                (3, 'Chimney', 'black'),
                (3, 'Departure Time', 8)
            ]),
            ("Clues 12 and 14: Border ship carries corn next to rice", [
                (5, 'Cargo', 'corn'),
                (4, 'Cargo', 'rice')
            ]),
            ("Clues 4 and 8: French ship left of coffee carrier (Greek) and leaves at 5 to Genoa", [
                (1, 'Nationality', 'French'),
                (1, 'Chimney', 'blue'),
                (1, 'Departure Time', 5),
                (1, 'Destination', 'Genoa')
            ]),
            ("Clue 11: Ship leaving at 7 (Spanish) next to white chimney", [
                (4, 'Chimney', 'white')
            ]),
            ("Clues 7 and 9: Spanish ship leaves at 7 to Port Said, green chimney next to rice", [
                (5, 'Nationality', 'Spanish'),
                (5, 'Departure Time', 7),
                (5, 'Chimney', 'green'),
                (5, 'Destination', 'Said')
            ]),
            ("Clues 3 and 5: English ship leaves at 9, and cocoa left of Marseille", [
                (4, 'Nationality', 'English'),
                (4, 'Departure Time', 9),
                (4, 'Destination', 'Marseille')
            ]),
            ("Clue 6: Brazilian ship to Manila", [
                (3, 'Nationality', 'Brazilian'),
                (3, 'Cargo', 'cocoa'),
                (3, 'Destination', 'Manila')
            ]),
            ("Only tea cargo remains for position 1", [
                (1, 'Cargo', 'tea')
            ])
        ]
        for step_num, (reason, assignments) in enumerate(steps, start=1):
            self.deduction_steps.append({"reason": reason, "assignments": []})
            for pos, attr, value in assignments:
                self.apply_deduction(step_num, pos, attr, value)
        self.check_solution()

class ShipPuzzleUI:
    def __init__(self, root):
        self.root = root
        self.solver = ShipPuzzleSolver()
        self.current_clue_index = 0
        self.auto_index = 0
        
        # Configure root window
        root.title("Ship Logic Puzzle")
        root.configure(bg="#e0f7fa")
        root.geometry("900x600")
        
        # Define color scheme
        self.bg_color = "#e0f8fa"  # Light blue
        self.header_color = "#00838f"  # Teal
        self.button_color = "#4db6ac"  # Light teal
        self.button_hover = "#26a69a"  # Darker teal
        self.accent_color = "#ffab91"  # Salmon
        self.cell_color = "#b2ebf2"  # Light cyan
        self.highlight_color = "#ffcc80"  # Light orange
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", 
                            font=("Arial", 10, "bold"), 
                            background=self.button_color,
                            foreground="white",
                            padding=5)
        self.style.map("TButton",
                      background=[("active", self.button_hover)])
        
        self.home_screen()

    def home_screen(self):
        self.clear_screen()
        
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.header_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(0)
        
        tk.Label(header_frame, 
                text="Ship Logic Puzzle", 
                font=("Arial", 24, "bold"), 
                fg="white", 
                bg=self.header_color).pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Description
        desc = "Solve the ship puzzle by matching attributes to positions. Each ship has a unique combination of nationality, departure time, cargo, chimney color, and destination."
        tk.Label(content_frame, 
                text=desc, 
                wraplength=600,
                font=("Arial", 11), 
                bg=self.bg_color, 
                fg="#333333").pack(pady=20)
        
        self.style.configure("TButton", 
                    font=("Arial", 10, "bold"), 
                    background=self.button_color,
                    foreground="black",  # This sets the text color
                    padding=5)
        
        self.style.map("TButton",
                    foreground=[("active", "#13bce6")],  # Text color when hovered
                    background=[("active", self.button_hover)])
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.bg_color)
        button_frame.pack(pady=30)
        
        # Menu buttons
        buttons = [
            ("Manual Play", self.manual_play_screen),
            ("How to Solve", self.run_auto_solver),
            ("Exit", self.root.destroy)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.pack(pady=10, ipady=8)
            
        # Footer
        tk.Label(self.root, 
                text="Logic Puzzle Solver • © 2025", 
                font=("Arial", 9), 
                bg=self.bg_color, 
                fg="#666666").pack(side=tk.BOTTOM, pady=10)

    def manual_play_screen(self):
        self.clear_screen()
        self.entries = {}
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.header_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(0)
        
        tk.Label(header_frame, 
                text="Manual Play", 
                font=("Arial", 18, "bold"), 
                fg="white", 
                bg=self.header_color).pack(pady=15)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg=self.bg_color)
        nav_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Home button
        home_button = tk.Button(nav_frame, 
                            text="Home", 
                            command=self.home_screen,
                            bg=self.button_color, 
                            fg="white", 
                            relief=tk.FLAT,
                            font=("Arial", 9, "bold"),
                            activebackground=self.button_hover,  # Color when clicked
                            activeforeground="white")  # Text color when clicked

        # Pack the button
        home_button.pack(side=tk.LEFT)

        # Add hover effects
        home_button.bind("<Enter>", lambda e: home_button.config(bg=self.button_hover))
        home_button.bind("<Leave>", lambda e: home_button.config(bg=self.button_color))
        
        
        # The hint butto
        hint_button = tk.Button(
            nav_frame, 
            text="?", 
            width=3, 
            command=self.show_hint_popup,
            bg=self.accent_color,  # Normal background color (salmon: #ffab91)
            fg="white",            # Text color
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            activebackground="#ff8a65",  # Darker salmon when clicked
            activeforeground="white"     # Text color when clicked
        )

        # Pack the button
        hint_button.pack(side=tk.RIGHT)

        # Add hover effects - darken the salmon color slightly when hovering
        hint_button.bind("<Enter>", lambda e: hint_button.config(bg="#ff8a65"))  # Darker salmon
        hint_button.bind("<Leave>", lambda e: hint_button.config(bg=self.accent_color))  # Original color
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create the grid
        grid_frame = tk.Frame(main_frame, bg=self.bg_color)
        grid_frame.pack(pady=10)
        
        # Column headers (positions)
        attrs = ["Nationality", "Departure Time", "Cargo", "Chimney", "Destination"]
        for j in range(1, 6):
            tk.Label(grid_frame, 
                    text=f"Position {j}", 
                    font=("Arial", 10, "bold"), 
                    bg=self.header_color, 
                    fg="white",
                    width=15,
                    relief=tk.RAISED,
                    padx=5, pady=5).grid(row=0, column=j, padx=2, pady=2)
        
        # Row headers (attributes)
        for i, attr in enumerate(attrs):
            tk.Label(grid_frame, 
                    text=attr, 
                    font=("Arial", 10, "bold"), 
                    bg=self.header_color, 
                    fg="white",
                    width=15,
                    relief=tk.RAISED,
                    padx=5, pady=5).grid(row=i+1, column=0, padx=2, pady=2)
        
        # Create entry fields
        for j in range(1, 6):
            self.entries[j] = {}
            for i, attr in enumerate(attrs):
                entry = tk.Entry(grid_frame, width=15, font=("Arial", 10),
                                bg=self.cell_color, relief=tk.SUNKEN,
                                justify=tk.CENTER)
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                self.entries[j][attr] = entry
        
        # Action buttons
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Check Solution", command=self.check_solution).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reset Game", command=self.reset_game).pack(side=tk.LEFT, padx=10)

    def run_auto_solver(self):
        self.clear_screen()
        self.solver.auto_solve()
        self.auto_index = 0
        self.show_auto_step()

    def show_auto_step(self):
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.header_color, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(0)
        
        tk.Label(header_frame, 
                text="Step-by-Step Solution", 
                font=("Arial", 18, "bold"), 
                fg="white", 
                bg=self.header_color).pack(pady=15)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg=self.bg_color)
        nav_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(nav_frame, text="Home", command=self.home_screen,
                 bg=self.button_color, fg="white", relief=tk.FLAT,
                 font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Step information
        step_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        step_frame.pack(fill=tk.X, padx=10, pady=10)
        
        step_num = self.auto_index + 1
        total_steps = len(self.solver.deduction_steps)
        tk.Label(step_frame, 
                text=f"Step {step_num}/{total_steps}", 
                font=("Arial", 12, "bold"), 
                bg="#ffffff", 
                fg=self.header_color).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Label(step_frame, 
                text=self.solver.deduction_steps[self.auto_index]['reason'], 
                wraplength=700,
                font=("Arial", 11), 
                bg="#ffffff", 
                justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
        
        # Create the grid
        grid_frame = tk.Frame(main_frame, bg=self.bg_color)
        grid_frame.pack(pady=10)
        
        # Column headers (positions)
        attrs = ["Nationality", "Departure Time", "Cargo", "Chimney", "Destination"]
        for j in range(1, 6):
            tk.Label(grid_frame, 
                    text=f"Position {j}", 
                    font=("Arial", 10, "bold"), 
                    bg=self.header_color, 
                    fg="white",
                    width=15,
                    relief=tk.RAISED,
                    padx=5, pady=5).grid(row=0, column=j, padx=2, pady=2)
        
        # Row headers (attributes)
        for i, attr in enumerate(attrs):
            tk.Label(grid_frame, 
                    text=attr, 
                    font=("Arial", 10, "bold"), 
                    bg=self.header_color, 
                    fg="white",
                    width=15,
                    relief=tk.RAISED,
                    padx=5, pady=5).grid(row=i+1, column=0, padx=2, pady=2)
        
        # Get current assignments
        current_assignments = set()
        for i in range(self.auto_index + 1):
            for assignment in self.solver.deduction_steps[i]['assignments']:
                current_assignments.add((assignment[0], assignment[1]))
        
        # Display values with highlighting
        for j in range(1, 6):
            for i, attr in enumerate(attrs):
                if (j, attr) in current_assignments:
                    val = self.solver.positions[j][attr]
                    if val is None:
                        val = ""
                else:
                    val = ""
                
                # Highlight the current step's assignments
                bg_color = self.highlight_color if (j, attr) in [
                    (x[0], x[1]) for x in self.solver.deduction_steps[self.auto_index]['assignments']] else self.cell_color
                
                tk.Label(grid_frame, 
                        text=str(val), 
                        font=("Arial", 10),
                        bg=bg_color, 
                        fg="#000000",
                        width=15,
                        relief=tk.SUNKEN,
                        padx=5, pady=5).grid(row=i+1, column=j, padx=2, pady=2)
        
        # Navigation controls
        nav_frame = tk.Frame(main_frame, bg=self.bg_color)
        nav_frame.pack(pady=20)
        
        if self.auto_index > 0:
            ttk.Button(nav_frame, text="◀ Previous Step", 
                      command=lambda: self.navigate_auto(-1)).pack(side=tk.LEFT, padx=10)
        
        if self.auto_index < len(self.solver.deduction_steps) - 1:
            ttk.Button(nav_frame, text="Next Step ▶", 
                      command=lambda: self.navigate_auto(1)).pack(side=tk.LEFT, padx=10)
        else:
            ttk.Button(nav_frame, text="🎉 Puzzle Solved!", 
                      command=self.home_screen).pack(side=tk.LEFT, padx=10)

    def navigate_auto(self, delta):
        self.auto_index += delta
        self.show_auto_step()

    def show_hint_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Clue Helper")
        popup.geometry("500x200")
        popup.configure(bg="#e3f2fd")
        popup.resizable(False, False)
        
        # Center the popup
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        popup_x = main_x + (main_width - 500) // 2
        popup.geometry(f"+{popup_x}+{main_y + 100}")
        
        tk.Label(popup, 
                text="CLUE", 
                font=("Arial", 14, "bold"), 
                bg="#bbdefb", 
                fg="#0d47a1",
                width=50).pack(pady=(10, 5), fill=tk.X)
        
        clue_frame = tk.Frame(popup, bg="#e3f2fd")
        clue_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        clue_label = tk.Label(clue_frame, 
                            text=self.solver.clues[self.current_clue_index], 
                            wraplength=460,
                            font=("Arial", 11), 
                            bg="#e3f2fd", 
                            fg="#333333",
                            justify=tk.LEFT)
        clue_label.pack(pady=10)
        
        # Navigation controls
        nav_frame = tk.Frame(popup, bg="#e3f2fd")
        nav_frame.pack(pady=(0, 15))
        
        def prev():
            self.current_clue_index = (self.current_clue_index - 1) % len(self.solver.clues)
            clue_label.config(text=self.solver.clues[self.current_clue_index])
        
        def next():
            self.current_clue_index = (self.current_clue_index + 1) % len(self.solver.clues)
            clue_label.config(text=self.solver.clues[self.current_clue_index])
        
        ttk.Button(nav_frame, text="◀ Prev", width=8, command=prev).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Next ▶", width=8, command=next).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Close", width=8, command=popup.destroy).pack(side=tk.LEFT, padx=10)

    def check_solution(self):
        # Copy values from entry fields to solver's positions
        for pos in self.entries:
            for attr in self.entries[pos]:
                self.solver.positions[pos][attr] = self.entries[pos][attr].get().strip()

        if self.solver.check_solution():
            messagebox.showinfo("Success", "🎉 Congratulations! All clues satisfied!\nYour solution is correct!")
        else:
            messagebox.showwarning("Try Again", "❌ Solution doesn't satisfy all clues.\nCheck your answers and try again.")

    def reset_game(self):
        self.solver.reset()
        self.manual_play_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ShipPuzzleUI(root)
    root.mainloop()