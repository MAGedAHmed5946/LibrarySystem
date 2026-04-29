"""Login page structure module."""
import tkinter as tk
from tkinter import ttk, messagebox

# Shared UI COLORS
COLORS = {
    'bg_primary': '#1e1e2e', 'bg_secondary': '#2a2a3c',
    'button_primary': '#4f46e5', 'button_hover': '#6366f1',
    'text_primary': '#ffffff', 'text_secondary': '#b0b0c0',
    'input_bg': '#3b3b52'
}

class LoginPage(tk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.callback = callback
        self.create_widgets()
    
    def create_widgets(self):
        container = ttk.Frame(self, style='Content.TFrame')
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=500)
        
        title_label = ttk.Label(container, text='📚 Library System', style='Title.TLabel')
        title_label.pack(pady=40)
        
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        ttk.Label(form_frame, text='Username', style='Heading.TLabel').pack(anchor=tk.W, pady=(20, 5))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var)
        username_entry.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(form_frame, text='Password', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, show='•')
        password_entry.pack(fill=tk.X, pady=(0, 30))
        
        login_btn = ttk.Button(form_frame, text='Login', command=self.login, style='Primary.TButton')
        login_btn.pack(fill=tk.X, pady=10)
        
        info_frame = ttk.Frame(form_frame, style='Card.TFrame')
        info_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(info_frame, text='Demo Credentials:', style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        ttk.Label(info_frame, text='Admin: admin / admin123', style='Secondary.TLabel').pack(anchor=tk.W)
        ttk.Label(info_frame, text='Staff: staff / staff123', style='Secondary.TLabel').pack(anchor=tk.W)
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all fields')
            return
        
        if username == 'admin' and password == 'admin123':
            self.callback('admin', 'Admin')
        elif username == 'staff' and password == 'staff123':
            self.callback('staff', 'Staff')
        else:
            messagebox.showerror('Error', 'Invalid credentials')
            self.password_var.set('')
