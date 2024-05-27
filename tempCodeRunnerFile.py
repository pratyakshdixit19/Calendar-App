import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
from tkcalendar import Calendar
from PIL import Image, ImageTk
import sqlite3
import datetime
import csv
import os

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar and Reminder App")
        self.root.geometry("700x800")
        self.root.configure(bg='#2c3e50')

        self.setup_styles()

        self.header_frame = tk.Frame(root, bg='#2c3e50')
        self.header_frame.pack(pady=10)

        self.main_frame = tk.Frame(root, bg='#2c3e50')
        self.main_frame.pack(pady=10)

        self.footer_frame = tk.Frame(root, bg='#2c3e50')
        self.footer_frame.pack(pady=10)

        self.title_label = tk.Label(self.header_frame, text="My Calendar and Reminder App", font=('Helvetica', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        self.title_label.pack(pady=10)

        self.calendar = Calendar(self.main_frame, selectmode='day', date_pattern='y-mm-dd', background='white', foreground='black', headersbackground='#16a085', headersforeground='white', bordercolor='#1abc9c')
        self.calendar.pack(pady=10)

        self.event_title = tk.Entry(self.main_frame, width=40, font=('Helvetica', 12), fg='#2c3e50', bd=2, relief='solid')
        self.event_title.pack(pady=5)
        self.event_title.insert(0, "Event Title")
        self.event_title.bind("<FocusIn>", lambda args: self.event_title.delete('0', 'end'))

        self.event_description = tk.Entry(self.main_frame, width=40, font=('Helvetica', 12), fg='#2c3e50', bd=2, relief='solid')
        self.event_description.pack(pady=5)
        self.event_description.insert(0, "Event Description")
        self.event_description.bind("<FocusIn>", lambda args: self.event_description.delete('0', 'end'))

        self.event_category = tk.Entry(self.main_frame, width=40, font=('Helvetica', 12), fg='#2c3e50', bd=2, relief='solid')
        self.event_category.pack(pady=5)
        self.event_category.insert(0, "Event Category")
        self.event_category.bind("<FocusIn>", lambda args: self.event_category.delete('0', 'end'))

        self.load_button_images()
        self.create_buttons()

        self.setup_database()
        self.check_reminders()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10, relief='flat', background='#1abc9c', foreground='white')
        self.style.map('TButton', background=[('active', '#16a085')], foreground=[('active', 'white')])
        self.style.configure('TLabel', font=('Helvetica', 12), padding=10, background='#34495e', foreground='#ecf0f1')
        self.style.configure('TEntry', font=('Helvetica', 12), padding=10, relief='solid')

    def load_button_images(self):
        self.button_images = {}
        try:
            self.button_images = {
                'add_event': ImageTk.PhotoImage(Image.open('add_event.png').resize((40, 40))),
                'view_events': ImageTk.PhotoImage(Image.open('view_events.png').resize((40, 40))),
                'add_reminder': ImageTk.PhotoImage(Image.open('add_reminder.png').resize((40, 40))),
                'delete_event': ImageTk.PhotoImage(Image.open('delete_event.png').resize((40, 40))),
                'delete_reminder': ImageTk.PhotoImage(Image.open('delete_reminder.png').resize((40, 40))),
                'search_event': ImageTk.PhotoImage(Image.open('search_event.png').resize((40, 40))),
                'export_events': ImageTk.PhotoImage(Image.open('export_events.png').resize((40, 40))),
                'import_events': ImageTk.PhotoImage(Image.open('import_events.png').resize((40, 40))),
                'edit_event': ImageTk.PhotoImage(Image.open('edit_event.png').resize((40, 40)))
            }
        except Exception as e:
            print(f"Error loading images: {e}")
            # Use placeholder text if images are not found
            self.button_images = {key: None for key in ['add_event', 'view_events', 'add_reminder', 'delete_event', 'delete_reminder', 'search_event', 'export_events', 'import_events', 'edit_event']}

    def create_buttons(self):
        self.add_event_button = ttk.Button(self.footer_frame, text="Add Event", command=self.add_event, image=self.button_images['add_event'], compound=tk.LEFT, style='TButton')
        self.add_event_button.pack(side=tk.LEFT, padx=10)

        self.view_events_button = ttk.Button(self.footer_frame, text="View Events", command=self.view_events, image=self.button_images['view_events'], compound=tk.LEFT, style='TButton')
        self.view_events_button.pack(side=tk.LEFT, padx=10)

        self.add_reminder_button = ttk.Button(self.footer_frame, text="Add Reminder", command=self.add_reminder, image=self.button_images['add_reminder'], compound=tk.LEFT, style='TButton')
        self.add_reminder_button.pack(side=tk.LEFT, padx=10)

        self.delete_event_button = ttk.Button(self.footer_frame, text="Delete Event", command=self.delete_event, image=self.button_images['delete_event'], compound=tk.LEFT, style='TButton')
        self.delete_event_button.pack(side=tk.LEFT, padx=10)

        self.delete_reminder_button = ttk.Button(self.footer_frame, text="Delete Reminder", command=self.delete_reminder, image=self.button_images['delete_reminder'], compound=tk.LEFT, style='TButton')
        self.delete_reminder_button.pack(side=tk.LEFT, padx=10)

        self.search_event_button = ttk.Button(self.footer_frame, text="Search Event", command=self.search_event, image=self.button_images['search_event'], compound=tk.LEFT, style='TButton')
        self.search_event_button.pack(side=tk.LEFT, padx=10)

        self.export_events_button = ttk.Button(self.footer_frame, text="Export Events", command=self.export_events, image=self.button_images['export_events'], compound=tk.LEFT, style='TButton')
        self.export_events_button.pack(side=tk.LEFT, padx=10)

        self.import_events_button = ttk.Button(self.footer_frame, text="Import Events", command=self.import_events, image=self.button_images['import_events'], compound=tk.LEFT, style='TButton')
        self.import_events_button.pack(side=tk.LEFT, padx=10)

        self.edit_event_button = ttk.Button(self.footer_frame, text="Edit Event", command=self.edit_event, image=self.button_images['edit_event'], compound=tk.LEFT, style='TButton')
        self.edit_event_button.pack(side=tk.LEFT, padx=10)

    def setup_database(self):
        conn = sqlite3.connect('calendar_app.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS events
                     (id INTEGER PRIMARY KEY, date TEXT, title TEXT, description TEXT, category TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS reminders
                     (id INTEGER PRIMARY KEY, event_id INTEGER, reminder_time TEXT,
                      FOREIGN KEY (event_id) REFERENCES events (id))''')
        conn.commit()
        conn.close()

    def add_event(self):
        date = self.calendar.get_date()
        title = self.event_title.get()
        description = self.event_description.get()

        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("INSERT INTO events (date, title, description) VALUES (?, ?, ?)", (date, title, description))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Event added successfully!")
        except Exception as e:
            print(f"Error adding event: {e}")
            messagebox.showerror("Error", "Failed to add event")

    def view_events(self):
        date = self.calendar.get_date()
        
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT * FROM events WHERE date=?", (date,))
            events = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error viewing events: {e}")
            messagebox.showerror("Error", "Failed to retrieve events")
            return

        event_list = ""
        for event in events:
            event_list += f"ID: {event[0]} - Title: {event[2]}\nDescription: {event[3]}\nCategory: {event[4]}\n\n"

        if event_list:
            messagebox.showinfo(f"Events on {date}", event_list)
        else:
            messagebox.showinfo(f"No Events", f"No events found on {date}")

    def add_reminder(self):
        date = self.calendar.get_date()
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT id, title FROM events WHERE date=?", (date,))
            events = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error retrieving events for reminder: {e}")
            messagebox.showerror("Error", "Failed to retrieve events for reminder")
            return

        if events:
            event_titles = [f"{event[0]}: {event[1]}" for event in events]
            selected_event = simpledialog.askstring("Select Event", "Enter event ID and title:\n" + "\n".join(event_titles))

            if selected_event:
                try:
                    event_id = int(selected_event.split(":")[0])
                    reminder_time = simpledialog.askstring("Reminder Time", "Enter reminder time (YYYY-MM-DD HH:MM:SS):")
                    
                    conn = sqlite3.connect('calendar_app.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO reminders (event_id, reminder_time) VALUES (?, ?)", (event_id, reminder_time))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Reminder added successfully!")
                except Exception as e:
                    print(f"Error adding reminder: {e}")
                    messagebox.showerror("Error", "Failed to add reminder")
        else:
            messagebox.showinfo("No Events", "No events found on this date")

    def delete_event(self):
        date = self.calendar.get_date()
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT id, title FROM events WHERE date=?", (date,))
            events = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error retrieving events for deletion: {e}")
            messagebox.showerror("Error", "Failed to retrieve events for deletion")
            return

        if events:
            event_titles = [f"{event[0]}: {event[1]}" for event in events]
            selected_event = simpledialog.askstring("Delete Event", "Enter event ID and title to delete:\n" + "\n".join(event_titles))

            if selected_event:
                try:
                    event_id = int(selected_event.split(":")[0])
                    
                    conn = sqlite3.connect('calendar_app.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM events WHERE id=?", (event_id,))
                    c.execute("DELETE FROM reminders WHERE event_id=?", (event_id,))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Event and associated reminders deleted successfully!")
                except Exception as e:
                    print(f"Error deleting event: {e}")
                    messagebox.showerror("Error", "Failed to delete event")
        else:
            messagebox.showinfo("No Events", "No events found on this date")

    def delete_reminder(self):
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT r.id, e.title, r.reminder_time FROM reminders r JOIN events e ON r.event_id = e.id")
            reminders = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error retrieving reminders for deletion: {e}")
            messagebox.showerror("Error", "Failed to retrieve reminders for deletion")
            return

        if reminders:
            reminder_list = [f"{reminder[0]}: {reminder[1]} at {reminder[2]}" for reminder in reminders]
            selected_reminder = simpledialog.askstring("Delete Reminder", "Enter reminder ID and event title to delete:\n" + "\n".join(reminder_list))

            if selected_reminder:
                try:
                    reminder_id = int(selected_reminder.split(":")[0])
                    
                    conn = sqlite3.connect('calendar_app.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Reminder deleted successfully!")
                except Exception as e:
                    print(f"Error deleting reminder: {e}")
                    messagebox.showerror("Error", "Failed to delete reminder")
        else:
            messagebox.showinfo("No Reminders", "No reminders found")

    def search_event(self):
        search_query = simpledialog.askstring("Search Event", "Enter event title or description to search:")
        
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT * FROM events WHERE title LIKE ? OR description LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
            events = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error searching events: {e}")
            messagebox.showerror("Error", "Failed to search events")
            return

        event_list = ""
        for event in events:
            event_list += f"ID: {event[0]} - Title: {event[2]}\nDescription: {event[3]}\nDate: {event[1]}\nCategory: {event[4]}\n\n"

        if event_list:
            messagebox.showinfo(f"Search Results", event_list)
        else:
            messagebox.showinfo(f"No Events", f"No events found matching '{search_query}'")

    def export_events(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if file_path:
            try:
                conn = sqlite3.connect('calendar_app.db')
                c = conn.cursor()
                c.execute("SELECT * FROM events")
                events = c.fetchall()
                conn.close()

                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Date', 'Title', 'Description', 'Category'])
                    writer.writerows(events)

                messagebox.showinfo("Success", "Events exported successfully!")
            except Exception as e:
                print(f"Error exporting events: {e}")
                messagebox.showerror("Error", "Failed to export events")

    def import_events(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
        if file_path:
            try:
                conn = sqlite3.connect('calendar_app.db')
                c = conn.cursor()
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row
                    for row in reader:
                        c.execute("INSERT INTO events (id, date, title, description, category) VALUES (?, ?, ?, ?, ?)", row)
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Events imported successfully!")
            except Exception as e:
                print(f"Error importing events: {e}")
                messagebox.showerror("Error", "Failed to import events")

    def edit_event(self):
        date = self.calendar.get_date()
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT id, title, description, category FROM events WHERE date=?", (date,))
            events = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error retrieving events for editing: {e}")
            messagebox.showerror("Error", "Failed to retrieve events for editing")
            return

        if events:
            event_list = [f"{event[0]}: {event[1]}" for event in events]
            selected_event = simpledialog.askstring("Edit Event", "Enter event ID and title to edit:\n" + "\n".join(event_list))

            if selected_event:
                try:
                    event_id = int(selected_event.split(":")[0])
                    conn = sqlite3.connect('calendar_app.db')
                    c = conn.cursor()
                    c.execute("SELECT * FROM events WHERE id=?", (event_id,))
                    event = c.fetchone()
                    conn.close()

                    if event:
                        new_title = simpledialog.askstring("Edit Event", "Edit title:", initialvalue=event[2])
                        new_description = simpledialog.askstring("Edit Event", "Edit description:", initialvalue=event[3])
                        new_category = simpledialog.askstring("Edit Event", "Edit category:", initialvalue=event[4])

                        conn = sqlite3.connect('calendar_app.db')
                        c = conn.cursor()
                        c.execute("UPDATE events SET title=?, description=?, category=? WHERE id=?", (new_title, new_description, new_category, event_id))
                        conn.commit()
                        conn.close()

                        messagebox.showinfo("Success", "Event updated successfully!")
                except Exception as e:
                    print(f"Error editing event: {e}")
                    messagebox.showerror("Error", "Failed to edit event")
        else:
            messagebox.showinfo("No Events", "No events found on this date")

    def check_reminders(self):
        now = datetime.datetime.now()
        try:
            conn = sqlite3.connect('calendar_app.db')
            c = conn.cursor()
            c.execute("SELECT e.title, r.reminder_time FROM reminders r JOIN events e ON r.event_id = e.id")
            reminders = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error checking reminders: {e}")
            return

        for reminder in reminders:
            reminder_time = datetime.datetime.strptime(reminder[1], "%Y-%m-%d %H:%M:%S")
            if now > reminder_time:
                messagebox.showinfo("Reminder", f"Reminder for event: {reminder[0]}")

        self.root.after(60000, self.check_reminders)  # Check reminders every 60 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
