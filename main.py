"""Entry point for the Library Management System."""
import tkinter as tk
from tkinter import ttk, messagebox
import sys

try:
    from database import DatabaseManager
    from gui.login import LoginPage
    from gui.dashboard import DashboardPage
    from gui.books import BooksPage
    from gui.members import MembersPage
    from gui.borrow import BorrowPage
    from gui.reports import ReportsPage
except ImportError as e:
    print(f"Error: Missing required modules! {e}")

COLORS = {
    'bg_primary': '#1e1e2e',
    'bg_secondary': '#2a2a3c',
    'bg_tertiary': '#3b3b52',
    'button_primary': '#4f46e5',
    'button_hover': '#6366f1',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0c0',
    'success': '#22c55e',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'input_bg': '#3b3b52',
    'border': '#4a4a62'
}

FONT_FAMILY = 'Ubuntu' if sys.platform == 'linux' else 'Segoe UI'

class StyleManager:
    """Handles global TTK styles."""
    def __init__(self):
        self.style = ttk.Style()
        self.configure_theme()
    
    def configure_theme(self):
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background=COLORS['bg_primary'])
        self.style.configure('Sidebar.TFrame', background=COLORS['bg_secondary'])
        self.style.configure('Content.TFrame', background=COLORS['bg_primary'])
        self.style.configure('Card.TFrame', background=COLORS['bg_secondary'], relief='flat')
        
        self.style.configure('TLabel', background=COLORS['bg_primary'], foreground=COLORS['text_primary'])
        self.style.configure('Title.TLabel', font=(FONT_FAMILY, 24, 'bold'), background=COLORS['bg_primary'], foreground=COLORS['text_primary'])
        self.style.configure('Heading.TLabel', font=(FONT_FAMILY, 14, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('Sidebar.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], font=(FONT_FAMILY, 10))
        self.style.configure('Sidebar.Title.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], font=(FONT_FAMILY, 12, 'bold'))
        self.style.configure('Card.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('StatValue.TLabel', font=(FONT_FAMILY, 28, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        
        self.style.configure('TButton', font=(FONT_FAMILY, 10), background=COLORS['button_primary'], foreground=COLORS['text_primary'])
        self.style.map('TButton', background=[('active', COLORS['button_hover'])])
        
        self.style.configure('Sidebar.TButton', font=(FONT_FAMILY, 10), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.map('Sidebar.TButton', background=[('active', COLORS['button_primary'])])
        
        self.style.configure('Danger.TButton', font=(FONT_FAMILY, 10), background=COLORS['danger'], foreground=COLORS['text_primary'])
        self.style.map('Danger.TButton', background=[('active', '#dc2626')])

        self.style.configure('Treeview', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], fieldbackground=COLORS['bg_secondary'])
        self.style.configure('Treeview.Heading', background=COLORS['button_primary'], foreground=COLORS['text_primary'])


class MainApplication(tk.Tk):
    """Main application frame that handles routing between pages."""
    def __init__(self):
        super().__init__()
        
        self.title('Library Management System')
        self.geometry('1200x750')
        self.configure(bg=COLORS['bg_primary'])
        self.center_window()
        
        try:
            self.db = DatabaseManager()
        except NameError:
            print("Warning: DatabaseManager not found. Ensure database.py exists.")
            self.db = None
            
        self.style_manager = StyleManager()
        
        try:
            self.page_dashboard = DashboardPage(self)
            self.page_books = BooksPage(self)
            self.page_members = MembersPage(self)
            self.page_borrow = BorrowPage(self)
            self.page_reports = ReportsPage(self)
        except NameError as e:
            print(f"GUI components loading error: {e}")
        
        self.current_user = None
        self.current_role = None
        
        self.create_main_layout()
        self.show_login()
    
    def center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 1200) // 2
        y = (sh - 750) // 2
        self.geometry(f'1200x750+{x}+{y}')
    
    def create_main_layout(self):
        self.main_frame = ttk.Frame(self, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.sidebar = ttk.Frame(self.main_frame, style='Sidebar.TFrame', width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        self.content = ttk.Frame(self.main_frame, style='Content.TFrame')
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def show_login(self):
        self.clear_sidebar()
        self.clear_content()
        try:
            login_page = LoginPage(self.content, self.on_login)
            login_page.pack(fill=tk.BOTH, expand=True)
        except NameError:
            ttk.Label(self.content, text="LoginPage missing!", style='Title.TLabel').pack(pady=50)
    
    def on_login(self, user, role):
        self.current_user = user
        self.current_role = role
        self.create_sidebar()
        self.page_dashboard.show()
    
    def create_sidebar(self):
        self.clear_sidebar()
        sidebar_inner = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        sidebar_inner.pack(fill=tk.BOTH, expand=True)
        
        logo_frame = ttk.Frame(sidebar_inner, style='Sidebar.TFrame')
        logo_frame.pack(fill=tk.X, padx=15, pady=20)
        ttk.Label(logo_frame, text='📚 Library', style='Sidebar.Title.TLabel').pack(anchor=tk.W)
        ttk.Label(logo_frame, text=f'{self.current_role}', foreground=COLORS['text_secondary'], background=COLORS['bg_secondary']).pack(anchor=tk.W)
        
        nav_items = [
            ('🏠 Dashboard', self.page_dashboard.show),
            ('📖 Books', self.page_books.show),
            ('👥 Members', self.page_members.show),
            ('📤 Borrow/Return', self.page_borrow.show),
            ('📊 Reports', self.page_reports.show),
        ]
        
        for text, cmd in nav_items:
            ttk.Button(sidebar_inner, text=text, command=cmd, style='Sidebar.TButton').pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(sidebar_inner, text='🚪 Logout', command=self.logout, style='Danger.TButton').pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
    
    def clear_content(self):
        for w in self.content.winfo_children(): w.destroy()
        
    def clear_sidebar(self):
        for w in self.sidebar.winfo_children(): w.destroy()

    def logout(self):
        self.current_user = None
        self.current_role = None
        self.show_login()

if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()