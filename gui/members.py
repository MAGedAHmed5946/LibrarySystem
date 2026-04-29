import tkinter as tk
from tkinter import ttk, messagebox
import re

COLORS = {'bg_primary': '#1e1e2e'}


class MembersPage:
    def __init__(self, app):
        self.app = app
        self.tree = None

    # ---------------- UI ----------------
    def show(self):
        self.app.clear_content()
        self.app.current_page = 'members'

        style = ttk.Style()
        style.map("Treeview",
                  background=[("selected", "#44475a"), ("active", COLORS['bg_primary'])],
                  foreground=[("selected", "white"), ("active", "white")])

        frame = tk.Frame(self.app.content, bg=COLORS['bg_primary'])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Members Management",
                  style='Title.TLabel').pack(anchor="w", pady=10)

        # ---------------- Search ----------------
        search_var = tk.StringVar()

        search_frame = tk.Frame(frame, bg=COLORS['bg_primary'])
        search_frame.pack(fill="x", pady=5)

        tk.Entry(search_frame, textvariable=search_var, width=40).pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search",
                   command=lambda: self.search(search_var.get())).pack(side="left", padx=5)

        ttk.Button(search_frame, text="Reset",
                   command=self.load_data).pack(side="left", padx=5)

        # ---------------- Buttons ----------------
        btn_frame = tk.Frame(frame, bg=COLORS['bg_primary'])
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(btn_frame, text='➕ Add Member',
                   command=self.add_member,
                   style='Success.TButton').pack(side="left", padx=5)

        ttk.Button(btn_frame, text='✏️ Edit Member',
                   command=self.edit_member,
                   style='Primary.TButton').pack(side="left", padx=5)

        ttk.Button(btn_frame, text='🗑️ Delete Member',
                   command=self.delete_member,
                   style='Danger.TButton').pack(side="left", padx=5)

        # ---------------- Table ----------------
        table_frame = tk.Frame(frame, bg=COLORS['bg_primary'])
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Phone", "Email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Columns + Sorting
        for col in columns:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, anchor="center", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Double click edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_data()

    # ---------------- DATA ----------------
    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        members = self.app.db.fetch_all("SELECT * FROM members")
        for m in members:
            self.tree.insert("", "end", values=m)

    # ---------------- SEARCH ----------------
    def search(self, keyword):
        self.tree.delete(*self.tree.get_children())

        query = """
        SELECT * FROM members
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        """
        like = f"%{keyword}%"
        results = self.app.db.fetch_all(query, (like, like, like))

        for r in results:
            self.tree.insert("", "end", values=r)

    # ---------------- SELECT ----------------
    def get_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a member first")
            return None
        return self.tree.item(selected)["values"]

    # ---------------- DOUBLE CLICK EDIT ----------------
    def on_double_click(self, event):
        data = self.get_selected()
        if not data:
            return
        self.open_edit_dialog(data)

    # ---------------- FORM ----------------
    def form_dialog(self, title, data=None):
        dialog = tk.Toplevel(self.app)
        dialog.title(title)
        dialog.configure(bg=COLORS['bg_primary'])

        frame = tk.Frame(dialog, bg=COLORS['bg_primary'])
        frame.pack(padx=20, pady=20)

        labels = ["Name", "Phone", "Email"]
        vars = []

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            var = tk.StringVar(value=data[i+1] if data else "")
            ttk.Entry(frame, textvariable=var).grid(row=i, column=1, pady=5)
            vars.append(var)

        return dialog, vars

    # ---------------- ADD ----------------
    def add_member(self):
        dialog, vars = self.form_dialog("Add Member")

        def save():
            name, phone, email = [v.get().strip() for v in vars]

            if not all([name, phone, email]):
                messagebox.showerror("Error", "All fields required")
                return

            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror("Error", "Invalid email")
                return

            self.app.db.execute_query(
                "INSERT INTO members (name, phone, email) VALUES (?, ?, ?)",
                (name, phone, email)
            )

            dialog.destroy()
            self.load_data()

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    # ---------------- EDIT ----------------
    def edit_member(self):
        data = self.get_selected()
        if data:
            self.open_edit_dialog(data)

    def open_edit_dialog(self, data):
        dialog, vars = self.form_dialog("Edit Member", data)

        def update():
            name, phone, email = [v.get().strip() for v in vars]

            self.app.db.execute_query(
                "UPDATE members SET name=?, phone=?, email=? WHERE id=?",
                (name, phone, email, data[0])
            )

            dialog.destroy()
            self.load_data()

        ttk.Button(dialog, text="Update", command=update).pack(pady=10)

    # ---------------- DELETE ----------------
    def delete_member(self):
        data = self.get_selected()
        if not data:
            return

        if messagebox.askyesno("Confirm", "Delete this member?"):
            self.app.db.execute_query(
                "DELETE FROM members WHERE id=?", (data[0],)
            )
            self.load_data()