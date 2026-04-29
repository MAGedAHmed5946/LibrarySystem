"""Books CRUD operation visualization."""
import tkinter as tk
from tkinter import ttk, messagebox

# Shared UI COLORS
COLORS = { 'bg_primary': '#1e1e2e' }

class BooksPage:
    def __init__(self, app):
        self.app = app
        
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'books'
        
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
        ttk.Label(title_frame, text='Books Management', style='Title.TLabel').pack(side=tk.LEFT, anchor=tk.W)
        
        button_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        button_frame.pack(fill=tk.X, padx=30, pady=10)
        
        ttk.Button(button_frame, text='➕ Add Book', command=self.add_book_dialog, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='✏️ Edit Book', command=self.edit_book_dialog, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='🗑️ Delete Book', command=self.delete_book_dialog, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        columns = ('ID', 'Title', 'Author', 'Category', 'Quantity')
        tree = ttk.Treeview(table_frame, columns=columns, height=20)
        tree.column('#0', width=0, stretch=tk.NO)
        
        for col in columns:
            tree.column(col, anchor=tk.CENTER, width=180)
            tree.heading(col, text=col)
        
        books = self.app.db.fetch_all("SELECT * FROM books")
        for book in books:
            tree.insert(parent='', index='end', values=book)
        
        scrollbar_tree = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar_tree.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

    def add_book_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Add Book')
        dialog.geometry('500x450')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Title', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Author', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=author_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Category', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=category_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Quantity', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        quantity_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=quantity_var).pack(fill=tk.X, pady=(0, 20))
        
        def save():
            title = title_var.get().strip()
            author = author_var.get().strip()
            category = category_var.get().strip()
            quantity = quantity_var.get().strip()
            
            if not all([title, author, category, quantity]):
                messagebox.showerror('Error', 'All fields required')
                return
            
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showerror('Error', 'Quantity must be positive')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Quantity must be a number')
                return
            
            self.app.db.execute_query("INSERT INTO books (title, author, category, quantity) VALUES (?, ?, ?, ?)",
                                (title, author, category, quantity))
            messagebox.showinfo('Success', 'Book added successfully')
            dialog.destroy()
            self.show()
        
        ttk.Button(form_frame, text='Add Book', command=save, style='Success.TButton').pack(fill=tk.X, pady=10)

    def edit_book_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Edit Book')
        dialog.geometry('500x500')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Book ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        book_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=book_id_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Title', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Author', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=author_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Category', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=category_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Quantity', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        quantity_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=quantity_var).pack(fill=tk.X, pady=(0, 20))
        
        def update():
            book_id = book_id_var.get().strip()
            title = title_var.get().strip()
            author = author_var.get().strip()
            category = category_var.get().strip()
            quantity = quantity_var.get().strip()
            
            if not all([book_id, title, author, category, quantity]):
                messagebox.showerror('Error', 'All fields required')
                return
            
            try:
                book_id = int(book_id)
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showerror('Error', 'Quantity must be positive')
                    return
            except ValueError:
                messagebox.showerror('Error', 'ID and Quantity must be numbers')
                return
            
            self.app.db.execute_query("UPDATE books SET title=?, author=?, category=?, quantity=? WHERE id=?",
                                (title, author, category, quantity, book_id))
            messagebox.showinfo('Success', 'Book updated successfully')
            dialog.destroy()
            self.show()
        
        ttk.Button(form_frame, text='Update Book', command=update, style='Primary.TButton').pack(fill=tk.X, pady=10)

    def delete_book_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Delete Book')
        dialog.geometry('400x200')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Book ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        book_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=book_id_var).pack(fill=tk.X, pady=(0, 20))
        
        def delete():
            book_id = book_id_var.get().strip()
            
            if not book_id:
                messagebox.showerror('Error', 'Book ID required')
                return
            
            try:
                book_id = int(book_id)
            except ValueError:
                messagebox.showerror('Error', 'Book ID must be a number')
                return
            
            if messagebox.askyesno('Confirm', 'Delete this book?'):
                self.app.db.execute_query("DELETE FROM books WHERE id=?", (book_id,))
                messagebox.showinfo('Success', 'Book deleted successfully')
                dialog.destroy()
                self.show()
        
        ttk.Button(form_frame, text='Delete Book', command=delete, style='Danger.TButton').pack(fill=tk.X, pady=11)
