"""Database Reporting and statistics visualization page."""
import tkinter as tk
from tkinter import ttk

# Shared UI COLORS
COLORS = {
    'bg_primary': '#1e1e2e', 'button_primary': '#4f46e5',
    'button_hover': '#6366f1', 'success': '#22c55e', 'warning': '#f59e0b',
}

class ReportsPage:
    def __init__(self, app):
        self.app = app
        
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'reports'
        
        canvas = tk.Canvas(self.app.content, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.app.content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Content.TFrame')
        
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        title_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        ttk.Label(title_frame, text='Reports', style='Title.TLabel').pack(anchor=tk.W)
        
        total_books = self.app.db.fetch_one("SELECT SUM(quantity) FROM books")[0] or 0
        borrowed_books = len(self.app.db.fetch_all("SELECT * FROM borrows WHERE return_date IS NULL"))
        available_books = total_books - borrowed_books
        total_members = len(self.app.db.fetch_all("SELECT * FROM members"))
        returned_books = len(self.app.db.fetch_all("SELECT * FROM borrows WHERE return_date IS NOT NULL"))
        
        reports_data = [
            ('📚 Total Books in Library', total_books, COLORS['button_primary']),
            ('✅ Available Books', available_books, COLORS['success']),
            ('📤 Currently Borrowed', borrowed_books, COLORS['warning']),
            ('📥 Books Returned', returned_books, COLORS['button_hover']),
            ('👥 Total Members', total_members, COLORS['button_primary']),
        ]
        
        for i in range(0, len(reports_data), 2):
            row_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
            row_frame.pack(fill=tk.X, padx=30, pady=10)
            
            for j in range(2):
                if i + j < len(reports_data):
                    title, value, color = reports_data[i + j]
                    self.create_stat_card(row_frame, title, value, color)
                    
    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=color, height=120, width=250)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        card.pack_propagate(False)
        
        ttk.Label(card, text=title, style='Stat.TLabel', background=color, foreground='white').pack(pady=(15, 5))
        ttk.Label(card, text=str(value), style='StatValue.TLabel', background=color, foreground='white').pack(pady=5)
