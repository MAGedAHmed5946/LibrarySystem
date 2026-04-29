"""Application starting dashboard dashboard visualization module."""
import tkinter as tk
from tkinter import ttk

# Shared UI COLORS
COLORS = {
<<<<<<< HEAD
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
    'info': '#0ea5e9',
    'input_bg': '#3b3b52',
    'border': '#4a4a62'
=======
    'bg_primary': '#1e1e2e', 'button_primary': '#4f46e5',
    'button_hover': '#6366f1', 'success': '#22c55e', 'warning': '#f59e0b',
>>>>>>> Esraa_Borrow
}

class DashboardPage:
    def __init__(self, app):
        self.app = app
        
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'dashboard'
        
<<<<<<< HEAD
        # Main Canvas and Scrollable Frame
=======
>>>>>>> Esraa_Borrow
        canvas = tk.Canvas(self.app.content, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.app.content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Content.TFrame')
        
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
<<<<<<< HEAD
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=canvas.winfo_width())
        
        # Ensure the frame expands to fill canvas width dynamically
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        canvas.bind('<Configure>', _on_canvas_configure)
        
=======
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
>>>>>>> Esraa_Borrow
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
<<<<<<< HEAD
        # Welcome / Title Section
        title_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        title_frame.pack(fill=tk.X, padx=40, pady=(40, 20))
        
        ttk.Label(title_frame, text='Dashboard Overview', font=('Segoe UI', 28, 'bold'), background=COLORS['bg_primary'], foreground=COLORS['text_primary']).pack(anchor=tk.W)
        ttk.Label(title_frame, text='Welcome back! Here is what is happening in your library today.', font=('Segoe UI', 12), background=COLORS['bg_primary'], foreground=COLORS['text_secondary']).pack(anchor=tk.W, pady=(5, 0))
        
        # Stats Section
        stats_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        stats_frame.pack(fill=tk.X, padx=35, pady=10)
=======
        title_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        title_frame.pack(fill=tk.X, padx=30, pady=20)
        ttk.Label(title_frame, text='Dashboard', style='Title.TLabel').pack(anchor=tk.W)
        
        stats_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        stats_frame.pack(fill=tk.X, padx=30, pady=10)
>>>>>>> Esraa_Borrow
        
        total_books = self.app.db.fetch_one("SELECT SUM(quantity) FROM books")[0] or 0
        borrowed_books = len(self.app.db.fetch_all("SELECT * FROM borrows WHERE return_date IS NULL"))
        available_books = total_books - borrowed_books
        total_members = len(self.app.db.fetch_all("SELECT * FROM members"))
        
        stats = [
<<<<<<< HEAD
            ('Total Books', total_books, COLORS['button_primary'], '📚'),
            ('Available', available_books, COLORS['success'], '✅'),
            ('Borrowed', borrowed_books, COLORS['warning'], '📤'),
            ('Members', total_members, COLORS['info'], '👥')
        ]
        
        # Grid layout for stat cards
        stats_container = ttk.Frame(stats_frame, style='Content.TFrame')
        stats_container.pack(fill=tk.X)
        
        # Create a responsive 2x2 grid or just a row if enough space
        for i in range(0, len(stats), 2):
            row_frame = ttk.Frame(stats_container, style='Content.TFrame')
            row_frame.pack(fill=tk.X, pady=10)
            
            for j in range(2):
                if i + j < len(stats):
                    stat_name, stat_value, color, icon = stats[i + j]
                    self.create_stat_card(row_frame, stat_name, stat_value, color, icon)
        
        # Recent Activity Section
        recent_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_secondary'], padx=30, pady=25)
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(30, 40))
        
        # Activity Header
        header_frame = tk.Frame(recent_frame, bg=COLORS['bg_secondary'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text='Recent Borrows', font=('Segoe UI', 16, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary']).pack(side=tk.LEFT)
        
        activity_data = self.app.db.fetch_all("""
            SELECT b.title, m.name, br.borrow_date 
=======
            ('📚 Total Books', total_books, COLORS['button_primary']),
            ('✅ Available', available_books, COLORS['success']),
            ('📤 Borrowed', borrowed_books, COLORS['warning']),
            ('👥 Members', total_members, COLORS['button_hover'])
        ]
        
        for i in range(0, len(stats), 2):
            row_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
            row_frame.pack(fill=tk.X, padx=30, pady=10)
            
            for j in range(2):
                if i + j < len(stats):
                    stat_name, stat_value, color = stats[i + j]
                    self.create_stat_card(row_frame, stat_name, stat_value, color)
        
        recent_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        ttk.Label(recent_frame, text='Recent Activity', style='Heading.TLabel').pack(anchor=tk.W, pady=10)
        
        activity_data = self.app.db.fetch_all("""
            SELECT 'Borrow' as type, b.title, m.name, br.borrow_date 
>>>>>>> Esraa_Borrow
            FROM borrows br
            JOIN books b ON br.book_id = b.id
            JOIN members m ON br.member_id = m.id
            WHERE br.return_date IS NULL
            ORDER BY br.borrow_date DESC LIMIT 5
        """)
        
        if activity_data:
<<<<<<< HEAD
            for title, member, date in activity_data:
                # Individual Activity Row
                row = tk.Frame(recent_frame, bg=COLORS['bg_tertiary'])
                row.pack(fill=tk.X, pady=6)
                
                # Add a subtle left border to the row
                border = tk.Frame(row, bg=COLORS['warning'], width=4)
                border.pack(side=tk.LEFT, fill=tk.Y)
                
                # Left side: Icon & Title
                left_frame = tk.Frame(row, bg=COLORS['bg_tertiary'])
                left_frame.pack(side=tk.LEFT, padx=(15, 10), pady=12)
                
                ttk.Label(left_frame, text="📖", font=('Segoe UI', 14), background=COLORS['bg_tertiary']).pack(side=tk.LEFT)
                ttk.Label(left_frame, text=title, font=('Segoe UI', 11, 'bold'), background=COLORS['bg_tertiary'], foreground=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
                
                # Middle side: Member
                middle_frame = tk.Frame(row, bg=COLORS['bg_tertiary'])
                middle_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                ttk.Label(middle_frame, text=f"borrowed by {member}", font=('Segoe UI', 10), background=COLORS['bg_tertiary'], foreground=COLORS['text_secondary']).pack(side=tk.LEFT, padx=10)
                
                # Right side: Date
                ttk.Label(row, text=date, font=('Segoe UI', 10), background=COLORS['bg_tertiary'], foreground=COLORS['text_secondary']).pack(side=tk.RIGHT, padx=20)
        else:
            empty_frame = tk.Frame(recent_frame, bg=COLORS['bg_tertiary'])
            empty_frame.pack(fill=tk.X, pady=6)
            ttk.Label(empty_frame, text='No recent activity to show', font=('Segoe UI', 11), background=COLORS['bg_tertiary'], foreground=COLORS['text_secondary']).pack(pady=20)
    
    def create_stat_card(self, parent, title, value, color, icon):
        card = tk.Frame(parent, bg=COLORS['bg_secondary'], height=130)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        card.pack_propagate(False)
        
        # Top color accent
        accent = tk.Frame(card, bg=color, height=4)
        accent.pack(side=tk.TOP, fill=tk.X)
        
        # Content container
        content = tk.Frame(card, bg=COLORS['bg_secondary'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Header (Icon + Title)
        header = tk.Frame(content, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X)
        
        ttk.Label(header, text=icon, font=('Segoe UI', 14), background=COLORS['bg_secondary']).pack(side=tk.LEFT)
        ttk.Label(header, text=title, font=('Segoe UI', 12, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(8, 0))
        
        # Value
        ttk.Label(content, text=str(value), font=('Segoe UI', 36, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['text_primary']).pack(anchor=tk.W, pady=(10, 0))
=======
            for activity in activity_data:
                activity_text = f"📤 {activity[1]} borrowed by {activity[2]} on {activity[3]}"
                ttk.Label(recent_frame, text=activity_text, style='Secondary.TLabel').pack(anchor=tk.W, pady=5)
        else:
            ttk.Label(recent_frame, text='No recent activity', style='Secondary.TLabel').pack(anchor=tk.W, pady=5)
    
    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=color, height=120, width=250)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        card.pack_propagate(False)
        
        ttk.Label(card, text=title, style='Stat.TLabel', background=color, foreground='white').pack(pady=(15, 5))
        ttk.Label(card, text=str(value), style='StatValue.TLabel', background=color, foreground='white').pack(pady=5)
>>>>>>> Esraa_Borrow
