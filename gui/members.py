"""Members CRUD operation visualization."""
import tkinter as tk
from tkinter import ttk, messagebox
import re

# Shared UI COLORS
COLORS = { 'bg_primary': '#1e1e2e' }

class MembersPage:
    def __init__(self, app):
        self.app = app
        
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'members'
        
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
        ttk.Label(title_frame, text='Members Management', style='Title.TLabel').pack(anchor=tk.W)
        
        button_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        button_frame.pack(fill=tk.X, padx=30, pady=10)
        
        ttk.Button(button_frame, text='➕ Add Member', command=self.add_member_dialog, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='✏️ Edit Member', command=self.edit_member_dialog, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='🗑️ Delete Member', command=self.delete_member_dialog, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(scrollable_frame, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        columns = ('ID', 'Name', 'Phone', 'Email')
        tree = ttk.Treeview(table_frame, columns=columns, height=20)
        tree.column('#0', width=0, stretch=tk.NO)
        
        for col in columns:
            tree.column(col, anchor=tk.CENTER, width=250)
            tree.heading(col, text=col)
        
        members = self.app.db.fetch_all("SELECT * FROM members")
        for member in members:
            tree.insert(parent='', index='end', values=member)
        
        scrollbar_tree = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar_tree.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

    def add_member_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Add Member')
        dialog.geometry('500x400')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Name', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Phone', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=phone_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Email', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=email_var).pack(fill=tk.X, pady=(0, 20))
        
        def save():
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            
            if not all([name, phone, email]):
                messagebox.showerror('Error', 'All fields required')
                return
            
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror('Error', 'Invalid email format')
                return
            
            self.app.db.execute_query("INSERT INTO members (name, phone, email) VALUES (?, ?, ?)",
                                (name, phone, email))
            messagebox.showinfo('Success', 'Member added successfully')
            dialog.destroy()
            self.show()
        
        ttk.Button(form_frame, text='Add Member', command=save, style='Success.TButton').pack(fill=tk.X, pady=10)

    def edit_member_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Edit Member')
        dialog.geometry('500x450')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Member ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        member_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=member_id_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Name', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Phone', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=phone_var).pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text='Email', style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=email_var).pack(fill=tk.X, pady=(0, 20))
        
        def update():
            member_id = member_id_var.get().strip()
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            
            if not all([member_id, name, phone, email]):
                messagebox.showerror('Error', 'All fields required')
                return
            
            try:
                member_id = int(member_id)
            except ValueError:
                messagebox.showerror('Error', 'Member ID must be a number')
                return
            
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror('Error', 'Invalid email format')
                return
            
            self.app.db.execute_query("UPDATE members SET name=?, phone=?, email=? WHERE id=?",
                                (name, phone, email, member_id))
            messagebox.showinfo('Success', 'Member updated successfully')
            dialog.destroy()
            self.show()
        
        ttk.Button(form_frame, text='Update Member', command=update, style='Primary.TButton').pack(fill=tk.X, pady=10)

    def delete_member_dialog(self):
        dialog = tk.Toplevel(self.app)
        dialog.title('Delete Member')
        dialog.geometry('400x200')
        dialog.configure(bg=COLORS['bg_primary'])
        
        form_frame = ttk.Frame(dialog, style='Content.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text='Member ID', style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        member_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=member_id_var).pack(fill=tk.X, pady=(0, 20))
        
        def delete():
            member_id = member_id_var.get().strip()
            
            if not member_id:
                messagebox.showerror('Error', 'Member ID required')
                return
            
            try:
                member_id = int(member_id)
            except ValueError:
                messagebox.showerror('Error', 'Member ID must be a number')
                return
            
            if messagebox.askyesno('Confirm', 'Delete this member?'):
                self.app.db.execute_query("DELETE FROM members WHERE id=?", (member_id,))
                messagebox.showinfo('Success', 'Member deleted successfully')
                dialog.destroy()
                self.show()
        
        ttk.Button(form_frame, text='Delete Member', command=delete, style='Danger.TButton').pack(fill=tk.X, pady=10)
