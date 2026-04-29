"""Entry point for the Library Management System."""
import tkinter as tk
from tkinter import ttk
from database import DatabaseManager

# Import specific pages from the gui package
from gui.login import LoginPage
from gui.dashboard import DashboardPage
from gui.books import BooksPage
from gui.members import MembersPage
from gui.borrow import BorrowPage
from gui.reports import ReportsPage

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
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), background=COLORS['bg_primary'], foreground=COLORS['text_primary'])
        self.style.configure('Heading.TLabel', font=('Segoe UI', 14, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('Sidebar.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], font=('Segoe UI', 10))
        self.style.configure('Sidebar.Title.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], font=('Segoe UI', 12, 'bold'))
        self.style.configure('Card.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('Stat.TLabel', font=('Segoe UI', 11), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('StatValue.TLabel', font=('Segoe UI', 28, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.configure('Secondary.TLabel', foreground=COLORS['text_secondary'], background=COLORS['bg_primary'])
        
        self.style.configure('TButton', font=('Segoe UI', 10), background=COLORS['button_primary'], foreground=COLORS['text_primary'])
        self.style.map('TButton', background=[('active', COLORS['button_hover'])])
        
        self.style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), background=COLORS['button_primary'], foreground=COLORS['text_primary'])
        self.style.map('Primary.TButton', background=[('active', COLORS['button_hover'])])
        
        self.style.configure('Success.TButton', font=('Segoe UI', 10), background=COLORS['success'], foreground=COLORS['text_primary'])
        self.style.map('Success.TButton', background=[('active', '#16a34a')])
        
        self.style.configure('Danger.TButton', font=('Segoe UI', 10), background=COLORS['danger'], foreground=COLORS['text_primary'])
        self.style.map('Danger.TButton', background=[('active', '#dc2626')])
        
        self.style.configure('Sidebar.TButton', font=('Segoe UI', 10), background=COLORS['bg_secondary'], foreground=COLORS['text_primary'])
        self.style.map('Sidebar.TButton', background=[('active', COLORS['button_primary'])])
        
        self.style.configure('TEntry', fieldbackground=COLORS['input_bg'], background=COLORS['input_bg'], foreground=COLORS['text_primary'], borderwidth=1, relief='solid')
        self.style.configure('TCombobox', fieldbackground=COLORS['input_bg'], background=COLORS['input_bg'], foreground=COLORS['text_primary'], borderwidth=1)
        
        self.style.configure('Treeview', background=COLORS['bg_secondary'], foreground=COLORS['text_primary'], fieldbackground=COLORS['bg_secondary'], borderwidth=0)
        self.style.configure('Treeview.Heading', background=COLORS['button_primary'], foreground=COLORS['text_primary'], borderwidth=0)
        self.style.map('Treeview', background=[('selected', COLORS['button_primary'])])
        self.style.configure('Vertical.TScrollbar', background=COLORS['bg_secondary'], troughcolor=COLORS['bg_secondary'])


class MainApplication(tk.Tk):
    """Main application frame that handles routing between pages."""
    def __init__(self):
        super().__init__()
        
        self.title('Library Management System')
        self.geometry('1200x750')
        self.configure(bg=COLORS['bg_primary'])
        self.center_window()
        
        # Core modules initialized here to be shared across pages
        self.db = DatabaseManager()
        self.style_manager = StyleManager()
        
        # GUI Page Handlers
        self.page_dashboard = DashboardPage(self)
        self.page_books = BooksPage(self)
        self.page_members = MembersPage(self)
        self.page_borrow = BorrowPage(self)
        self.page_reports = ReportsPage(self)
        
        self.current_user = None
        self.current_role = None
        self.current_page = None
        
        self.create_main_layout()
        self.show_login()
    
    def center_window(self):
        """Centers main application to screen view"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 750) // 2
        self.geometry(f'1200x750+{x}+{y}')
    
    def create_main_layout(self):
        """Builds out the permanent container elements (sidebar & main content area)"""
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
        login_page = LoginPage(self.content, self.on_login)
        login_page.pack(fill=tk.BOTH, expand=True)
    
    def on_login(self, user, role):
        self.current_user = user
        self.current_role = role
        self.create_sidebar()
        self.page_dashboard.show()
    
    def create_sidebar(self):
        self.clear_sidebar()
        
        sidebar_inner = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        sidebar_inner.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        logo_frame = ttk.Frame(sidebar_inner, style='Sidebar.TFrame')
        logo_frame.pack(fill=tk.X, padx=15, pady=20)
        
        ttk.Label(logo_frame, text='📚 Library', style='Sidebar.Title.TLabel').pack(anchor=tk.W)
        ttk.Label(logo_frame, text=f'{self.current_role}', style='Secondary.TLabel').pack(anchor=tk.W)
        
        separator1 = ttk.Frame(sidebar_inner, style='Sidebar.TFrame', height=1)
        separator1.pack(fill=tk.X, padx=15, pady=10)
        
        nav_frame = ttk.Frame(sidebar_inner, style='Sidebar.TFrame')
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add links to UI page instances
        nav_items = [
            ('🏠 Dashboard', self.page_dashboard.show),
            ('📖 Books', self.page_books.show),
            ('👥 Members', self.page_members.show),
            ('📤 Borrow/Return', self.page_borrow.show),
            ('📊 Reports', self.page_reports.show),
        ]
        
        for icon_text, command in nav_items:
            btn = ttk.Button(nav_frame, text=icon_text, command=command, style='Sidebar.TButton', width=25)
            btn.pack(fill=tk.X, pady=5)
        
        separator2 = ttk.Frame(sidebar_inner, style='Sidebar.TFrame', height=1)
        separator2.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=10)
        
        logout_btn = ttk.Button(sidebar_inner, text='🚪 Logout', command=self.logout, style='Danger.TButton', width=27)
        logout_btn.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def clear_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.current_user = None
        self.current_role = None
        self.clear_sidebar()
        self.clear_content()
        self.show_login()

if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
