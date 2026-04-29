"""Book borrowing and returning visualization."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Shared UI COLORS
COLORS = { 'bg_primary': '#1e1e2e' }

class BorrowPage:
    def __init__(self, app):
        self.app = app
        
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'borrow'
        
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
        ttk.Label(title_frame, text='Borrow & Return', style='Title.TLabel').pack(anchor=tk.W)
        
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        borrow_frame = ttk.Frame(notebook, style='Content.TFrame')
        notebook.add(borrow_frame, text='📤 Borrow Books')
        
        return_frame = ttk.Frame(notebook, style='Content.TFrame')
        notebook.add(return_frame, text='📥 Return Books')
        
        self.create_borrow_tab(borrow_frame)
        self.create_return_tab(return_frame)
    
    def create_borrow_tab(self, parent):
        form_frame = ttk.Frame(parent, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Book ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        book_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=book_id_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Member ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        member_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=member_id_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Days to Borrow', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        days_var = tk.StringVar(value='14')
        ttk.Entry(form_frame, textvariable=days_var).pack(fill=tk.X, pady=(0, 20))
        
        def borrow():
            book_id = book_id_var.get().strip()
            member_id = member_id_var.get().strip()
            days = days_var.get().strip()
            
            if not all([book_id, member_id, days]):
                messagebox.showerror('Error', 'All fields required')
                return
            
            try:
                book_id = int(book_id)
                member_id = int(member_id)
                days = int(days)
            except ValueError:
                messagebox.showerror('Error', 'IDs and days must be numbers')
                return
            
            book = self.app.db.fetch_one("SELECT * FROM books WHERE id=?", (book_id,))
            member = self.app.db.fetch_one("SELECT * FROM members WHERE id=?", (member_id,))
            
            if not book:
                messagebox.showerror('Error', 'Book not found')
                return
            if not member:
                messagebox.showerror('Error', 'Member not found')
                return
            if book[4] <= 0:
                messagebox.showerror('Error', 'No stock available')
                return
            
            borrow_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            
            self.app.db.execute_query("INSERT INTO borrows (book_id, member_id, borrow_date, due_date) VALUES (?, ?, ?, ?)",
                                (book_id, member_id, borrow_date, due_date))
            self.app.db.execute_query("UPDATE books SET quantity = quantity - 1 WHERE id=?", (book_id,))
            
            messagebox.showinfo('Success', 'Book borrowed successfully')
            book_id_var.set('')
            member_id_var.set('')
            days_var.set('14')
            self.show()
        
        ttk.Button(form_frame, text='Borrow Book', command=borrow, style='Success.TButton').pack(fill=tk.X, pady=10)
        
        active_borrows = self.app.db.fetch_all("SELECT b.id, bk.title, m.name, b.due_date FROM borrows b JOIN books bk ON b.book_id = bk.id JOIN members m ON b.member_id = m.id WHERE b.return_date IS NULL")
        
        ttk.Label(form_frame, text='Active Borrows', style='Heading.TLabel').pack(anchor=tk.W, pady=(30, 10))
        
        for borrow_data in active_borrows[:5]:
            text = f"📖 {borrow_data[1]} - {borrow_data[2]} (Due: {borrow_data[3]})"
            ttk.Label(form_frame, text=text, style='Secondary.TLabel').pack(anchor=tk.W, pady=3)
    
    def create_return_tab(self, parent):
        form_frame = ttk.Frame(parent, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Borrow ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        borrow_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=borrow_id_var).pack(fill=tk.X, pady=(0, 20))
        
        def return_book():
            borrow_id = borrow_id_var.get().strip()
            
            if not borrow_id:
                messagebox.showerror('Error', 'Borrow ID required')
                return
            
            try:
                borrow_id = int(borrow_id)
            except ValueError:
                messagebox.showerror('Error', 'Borrow ID must be a number')
                return
            
            borrow_record = self.app.db.fetch_one("SELECT * FROM borrows WHERE id=? AND return_date IS NULL", (borrow_id,))
            
            if not borrow_record:
                messagebox.showerror('Error', 'Borrow record not found')
                return
            
            return_date = datetime.now().strftime("%Y-%m-%d")
            self.app.db.execute_query("UPDATE borrows SET return_date=? WHERE id=?", (return_date, borrow_id))
            self.app.db.execute_query("UPDATE books SET quantity = quantity + 1 WHERE id=?", (borrow_record[1],))
            
            messagebox.showinfo('Success', 'Book returned successfully')
            borrow_id_var.set('')
            self.show()
        
        ttk.Button(form_frame, text='Return Book', command=return_book, style='Success.TButton').pack(fill=tk.X, pady=10)
        
        pending_returns = self.app.db.fetch_all("SELECT b.id, bk.title, m.name, b.due_date FROM borrows b JOIN books bk ON b.book_id = bk.id JOIN members m ON b.member_id = m.id WHERE b.return_date IS NULL")
        
        ttk.Label(form_frame, text='Pending Returns', style='Heading.TLabel').pack(anchor=tk.W, pady=(30, 10))
        
        for record in pending_returns[:5]:
            text = f"📤 ID: {record[0]} - {record[1]} by {record[2]} (Due: {record[3]})"
            ttk.Label(form_frame, text=text, style='Secondary.TLabel').pack(anchor=tk.W, pady=3)
