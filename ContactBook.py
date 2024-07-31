from PyQt5.QtWidgets import QApplication,QListWidgetItem ,QMainWindow, QWidget, QVBoxLayout,QListWidget ,QPushButton, QLabel, QFormLayout, QLineEdit, QDateTimeEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
from datetime import datetime
import json
import qdarkstyle
from tkinter import messagebox

class Contact:
    def __init__(self, name, phone, gender, email, added_time=None):
        self.name = name
        self.phone = phone
        self.gender = gender
        self.email = email
        self.added_time = added_time if added_time else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'gender': self.gender,
            'email': self.email,
            'added_time': self.added_time
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['name'], data['phone'], data['gender'], data['email'], data['added_time'])

class ContactBookApp(QMainWindow):
    def __init__(self):
        super(ContactBookApp, self).__init__()

        self.setWindowTitle('Contact Book')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        font = QFont('Arial', 20, QFont.Bold)

        self.title_label = QLabel('Welcome to the Contact Book', self)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        button_font = QFont('Arial', 12)

        self.add_button = QPushButton('Add Contact', self)
        self.add_button.setFont(button_font)
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.add_button.clicked.connect(self.open_add_contact_form)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton('Edit Contact', self)
        self.edit_button.setFont(button_font)
        self.edit_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;")
        self.edit_button.clicked.connect(self.open_list_contacts)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton('Delete Contact', self)
        self.delete_button.setFont(button_font)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.open_list_contacts_for_deletion)
        layout.addWidget(self.delete_button)

        self.search_button = QPushButton('Search Contact', self)
        self.search_button.setFont(button_font)
        self.search_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;")
        self.search_button.clicked.connect(self.open_search_form)
        layout.addWidget(self.search_button)

        self.list_button = QPushButton('List All Contacts', self)
        self.list_button.setFont(button_font)
        self.list_button.setStyleSheet("background-color: #9C27B0; color: white; padding: 10px; border-radius: 5px;")
        self.list_button.clicked.connect(self.display_contacts_list)
        layout.addWidget(self.list_button)

        self.contact_count_label = QLabel('Total Contacts: 0', self)
        self.contact_count_label.setFont(button_font)
        self.contact_count_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.contact_count_label)

        self.contacts = self.load_contacts()
        self.update_contact_count(len(self.contacts))

#------------------------------------------------------Add Contact section
    def open_add_contact_form(self):
        self.add_contact_form = QWidget()
        self.add_contact_form.setWindowTitle('Add Contact')
        self.add_contact_form.setGeometry(150, 150, 400, 300)
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.email_input = QLineEdit()
        self.date_time_input = QDateTimeEdit(datetime.now())
        self.date_time_input.setCalendarPopup(True)

        layout.addRow('Name:', self.name_input)
        layout.addRow('Phone:', self.phone_input)
        layout.addRow('Gender:', self.gender_input)
        layout.addRow('Email:', self.email_input)
        layout.addRow('Added Time:', self.date_time_input)

        add_button = QPushButton('Add')
        add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        add_button.clicked.connect(self.add_contact)
        layout.addWidget(add_button)

        self.add_contact_form.setLayout(layout)
        self.add_contact_form.show()

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        gender = self.gender_input.text()
        email = self.email_input.text()
        added_time = self.date_time_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone number are required")
            return

        new_contact = Contact(name, phone, gender, email, added_time)
        self.contacts.append(new_contact)
        self.save_contacts()
        self.update_contact_count(len(self.contacts))
        self.add_contact_form.close()

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as file:
                content = file.read().strip()
                if not content:
                    return []
                contacts_data = json.loads(content)
                return [Contact.from_dict(contact) for contact in contacts_data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error",f"Error loading contacts: {e}")
            return []

    def save_contacts(self):
        try:
            with open('contacts.json', 'w') as file:
                json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)
            messagebox.showinfo("Information", "Contacts saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving contacts: {e}")

    def update_contact_count(self, count):
        self.contact_count_label.setText(f'Total Contacts: {count}')

#--------------------------------------------Edit section

    def open_list_contacts(self):
        self.list_contacts_form = QWidget()
        self.list_contacts_form.setWindowTitle('List Contacts')
        self.list_contacts_form.setGeometry(150, 150, 400, 300)
        layout = QVBoxLayout()

        self.contact_list_widget = QListWidget()
        for contact in self.contacts:
            self.contact_list_widget.addItem(f"{contact.name} - {contact.phone}")

        self.contact_list_widget.itemClicked.connect(self.open_edit_contact_form)

        layout.addWidget(self.contact_list_widget)
        self.list_contacts_form.setLayout(layout)
        self.list_contacts_form.show()

    def open_edit_contact_form(self, item):
        contact_info = item.text().split(' - ')
        contact_name = contact_info[0]

        contact = next((c for c in self.contacts if c.name == contact_name), None)
        if not contact:
            messagebox.showwarning("Warning", "Contact not found")
            return

        self.edit_contact_form = QWidget()
        self.edit_contact_form.setWindowTitle('Edit Contact')
        self.edit_contact_form.setGeometry(150, 150, 400, 300)
        layout = QFormLayout()

        self.edit_name_input = QLineEdit(contact.name)
        self.edit_phone_input = QLineEdit(contact.phone)
        self.edit_gender_input = QLineEdit(contact.gender)
        self.edit_email_input = QLineEdit(contact.email)
        self.edit_date_time_input = QDateTimeEdit(datetime.strptime(contact.added_time, '%Y-%m-%d %H:%M:%S'))

        layout.addRow('Name:', self.edit_name_input)
        layout.addRow('Phone:', self.edit_phone_input)
        layout.addRow('Gender:', self.edit_gender_input)
        layout.addRow('Email:', self.edit_email_input)
        layout.addRow('Added Time:', self.edit_date_time_input)

        save_button = QPushButton('Save')
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        save_button.clicked.connect(lambda: self.save_edited_contact(contact))
        layout.addWidget(save_button)

        self.edit_contact_form.setLayout(layout)
        self.edit_contact_form.show()

    def save_edited_contact(self, old_contact):
        name = self.edit_name_input.text()
        phone = self.edit_phone_input.text()
        gender = self.edit_gender_input.text()
        email = self.edit_email_input.text()
        added_time = self.edit_date_time_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone number are required")
            return

        old_contact.name = name
        old_contact.phone = phone
        old_contact.gender = gender
        old_contact.email = email
        old_contact.added_time = added_time

        self.save_contacts()
        self.update_contact_count(len(self.contacts))
        self.edit_contact_form.close()
        self.open_list_contacts()

#----------------------------------------Delete Section

    def open_list_contacts_for_deletion(self):
        self.list_contacts_form = QWidget()
        self.list_contacts_form.setWindowTitle('List Contacts')
        self.list_contacts_form.setGeometry(150, 150, 400, 300)
        layout = QVBoxLayout()

        self.contact_list_widget = QListWidget()
        for contact in self.contacts:
            self.contact_list_widget.addItem(f"{contact.name} - {contact.phone}")

        self.contact_list_widget.itemClicked.connect(self.confirm_delete_contact)

        layout.addWidget(self.contact_list_widget)
        self.list_contacts_form.setLayout(layout)
        self.list_contacts_form.show()

    def confirm_delete_contact(self, item):
        contact_info = item.text().split(' - ')
        contact_name = contact_info[0]

        contact = next((c for c in self.contacts if c.name == contact_name), None)
        if not contact:
            messagebox.showwarning("Warning", "Contact not found")
            return

        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {contact_name}?")
        if response:
            self.delete_contact(contact)
            self.list_contacts_form.close()

    def delete_contact(self, contact_to_delete):
        self.contacts = [c for c in self.contacts if c != contact_to_delete]
        self.open_list_contacts_for_deletion()
        self.update_contact_count(len(self.contacts))

#--------------------------------------Search Section

    def open_search_form(self):
        self.search_form = QWidget()
        self.search_form.setWindowTitle('Search Contact')
        self.search_form.setGeometry(150, 150, 400, 300)
        layout = QFormLayout()

        self.search_name_input = QLineEdit()
        search_button = QPushButton('Search')
        search_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;")
        search_button.clicked.connect(self.perform_search)

        layout.addRow('Name:', self.search_name_input)
        layout.addWidget(search_button)

        self.search_form.setLayout(layout)
        self.search_form.show()

    def perform_search(self):
        search_name = self.search_name_input.text().strip()
        if not search_name:
            messagebox.showwarning("Warning", "Please enter a name to search")
            return

        matching_contacts = [contact for contact in self.contacts if search_name.lower() in contact.name.lower()]
        self.display_search_results(matching_contacts)
        self.search_form.close()

    def display_search_results(self, contacts):
        self.results_form = QWidget()
        self.results_form.setWindowTitle('Search Results')
        self.results_form.setGeometry(150, 150, 500, 400)
        layout = QVBoxLayout()

        if not contacts:
            no_result_label = QLabel("No contacts found")
            layout.addWidget(no_result_label)
        else:
            self.results_list_widget = QListWidget()
            for contact in contacts:
                item_text = f"Name: {contact.name}\nPhone: {contact.phone}\nGender: {contact.gender}\nEmail: {contact.email}\nAdded Time: {contact.added_time}"
                self.results_list_widget.addItem(item_text)

            self.results_list_widget.itemClicked.connect(self.open_contact_details)
            self.results_list_widget.setStyleSheet("""
                QListWidget {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #00141a;
                    padding: 10px;
                    font-size: 12px;
                }
                QListWidget::item {
                    margin-bottom: 10px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #002933;
                }
                QListWidget::item:selected {
                    background-color: #e0e0e0;
                }
            """)
            layout.addWidget(self.results_list_widget)

        self.results_form.setLayout(layout)
        self.results_form.show()

    def open_contact_details(self, item):
        contact_info = item.text().split('\n')
        contact_name = contact_info[0].split(': ')[1]

        contact = next((c for c in self.contacts if c.name == contact_name), None)
        if not contact:
            messagebox.showwarning("Warning", "Contact not found")
            return

        details = "\n".join(contact_info)
        details_widget = QLabel(details)
        details_widget.setStyleSheet(
            "padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #fff;font-size: 14px;font-weight: bold;")

        self.details_form = QWidget()
        self.details_form.setWindowTitle('Contact Details')
        self.details_form.setGeometry(150, 150, 400, 300)
        layout = QVBoxLayout()
        layout.addWidget(details_widget)

        close_button = QPushButton('Close')
        close_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        close_button.clicked.connect(self.details_form.close)
        layout.addWidget(close_button)

        self.details_form.setLayout(layout)
        self.details_form.show()

#------------------------------------------List section

    def display_contacts_list(self):
        self.list_form = QWidget()
        self.list_form.setWindowTitle('List All Contacts')
        self.list_form.setGeometry(150, 150, 500, 400)
        layout = QVBoxLayout()

        if not self.contacts:
            no_contacts_label = QLabel("No contacts available")
            layout.addWidget(no_contacts_label)
        else:
            self.contacts_list_widget = QListWidget()
            self.contacts_list_widget.setStyleSheet("""
                QListWidget {
                    border: 1px solid #333;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                    font-size: 12px;
                    color: #333;
                }
                QListWidget::item {
                    margin-bottom: 10px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #e0e0e0;
                    color: #000;
                    cursor: pointer;
                }
                QListWidget::item:selected {
                    background-color: #c1c1c1;
                }
            """)

            for contact in self.contacts:
                item_text = f"Name: {contact.name} | Phone: {contact.phone} | Added: {contact.added_time}"
                item = QListWidgetItem(item_text)
                self.contacts_list_widget.addItem(item)

            self.contacts_list_widget.itemClicked.connect(self.copy_to_clipboard)

            layout.addWidget(self.contacts_list_widget)

        close_button = QPushButton('Close')
        close_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        close_button.clicked.connect(self.list_form.close)
        layout.addWidget(close_button)

        self.list_form.setLayout(layout)
        self.list_form.show()

    def copy_to_clipboard(self, item):
        contact_info = item.text()
        phone_number = contact_info.split('|')[1].strip().split(': ')[1]

        clipboard = QApplication.clipboard()
        clipboard.setText(phone_number)

        messagebox.showinfo("Information", "Phone number copied to clipboard")


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
main_win = ContactBookApp()
main_win.show()
sys.exit(app.exec_())
