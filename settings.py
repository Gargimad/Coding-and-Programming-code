import tkinter as tk
from tkinter import messagebox

class SettingsPage:
    def __init__(self, parent, colors, dashboard_ref):
        """
        parent: the mainContainer frame from dashboard
        colors: dictionary of colors from dashboard
        dashboard_ref: reference to DashboardPage for callbacks if needed
        """
        self.parent = parent
        self.colors = colors
        self.dashboard = dashboard_ref

    def draw(self):
        """Draw the Settings page"""
        # Clear previous widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Settings", font=("Georgia", 26, "bold"),
                 bg=self.colors['bg'], fg=self.colors['darkText']).pack(anchor="w", padx=45, pady=(20, 10))

        # Example settings: Toggle notifications, change theme, manage account
        settings_frame = tk.Frame(self.parent, bg=self.colors['bg'])
        settings_frame.pack(fill="both", expand=True, padx=45, pady=20)

        # Notifications Toggle
        self.notifications_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="Enable Notifications",
            variable=self.notifications_var,
            bg=self.colors['bg'],
            fg=self.colors['darkText'],
            font=("Arial", 14)
        ).pack(anchor="w", pady=10)

        # Theme selection (placeholder, can expand later)
        tk.Label(settings_frame, text="Theme:", bg=self.colors['bg'], fg=self.colors['darkText'], font=("Arial", 14)).pack(anchor="w", pady=(20, 5))
        self.theme_var = tk.StringVar(value="Light")
        tk.OptionMenu(settings_frame, self.theme_var, "Light", "Dark").config(
            bg=self.colors['sidebar'],
            fg="white",
            font=("Arial", 12),
            relief="flat",
            width=10
        )
        theme_menu = tk.OptionMenu(settings_frame, self.theme_var, "Light", "Dark")
        theme_menu.config(bg=self.colors['sidebar'], fg="white", font=("Arial", 12), relief="flat", width=10)
        theme_menu.pack(anchor="w", pady=5)

        # Account actions
        tk.Label(settings_frame, text="Account", bg=self.colors['bg'], fg=self.colors['darkText'], font=("Arial", 14, "bold")).pack(anchor="w", pady=(30, 10))
        tk.Button(
            settings_frame,
            text="Change Password",
            bg=self.colors['sidebar'],
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.change_password
        ).pack(anchor="w", pady=5)

        tk.Button(
            settings_frame,
            text="Delete Account",
            bg="#E74C3C",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.delete_account
        ).pack(anchor="w", pady=5)

        # Save button (currently placeholder)
        tk.Button(
            settings_frame,
            text="Save Settings",
            bg=self.colors['card'],
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.save_settings
        ).pack(anchor="w", pady=(30, 10))

    # ------------------- Placeholder Actions -------------------
    def change_password(self):
        messagebox.showinfo("Change Password", "This feature will allow changing password (placeholder).")

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account? This cannot be undone.")
        if confirm:
            messagebox.showinfo("Account Deleted", "Account deletion placeholder executed.")

    def save_settings(self):
        notif = "enabled" if self.notifications_var.get() else "disabled"
        theme = self.theme_var.get()
        messagebox.showinfo("Settings Saved", f"Notifications: {notif}\nTheme: {theme}\n(Note: Placeholder actions)")
