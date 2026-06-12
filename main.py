import sys
import sqlite3
from PyQt6.QtCore import Qt 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QFormLayout, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Management")
        self.resize(1000, 800)
        
        self.central_widget = QWidget() # سويلي نافذه واخزنها في متغير اسمه central_widget
        self.setCentralWidget(self.central_widget) # هذا الامر يخلي النافذه الي انشأناها في المتغير central_widget تكون النافذه الرئيسية للبرنامج
        
        layout = QVBoxLayout() # حاويه للعناصر في النافذه الرئيسيه
        self.add_client_btn = QPushButton("Client Manager") # انشاء زر جديد
        self.add_client_btn.clicked.connect(self.open_add_client) # من تضغط على زر يربطها بعملية فتح النافذه الفرعيه
        self.add_client_btn.setStyleSheet("background-color: #5699C2; color: white; font-size: 50px; padding: 10px; border-radius: 25px;")
        layout.addWidget(self.add_client_btn)
        self.central_widget.setLayout(layout)

    def open_add_client(self): # داله للعمل على فتح النافذه الفرعيه
        self.add_window = AddClientWindow() # اضف النافذه الفرعيه الى المتغير self.add_window
        self.add_window.show() # اظهر النافذه الفرعيه
    

class AddClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Client")
        self.resize(1000, 800)
        
        # الاتصال بقاعدة البيانات
        self.conn = sqlite3.connect("clients.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            working_hours TEXT,
            monthly_salary TEXT
        )
        """)
        self.conn.commit()

        main_layout = QVBoxLayout() # حاويه للعناصر
        form_layout = QFormLayout() # مخطط النموذج لخانات الإدخال
        
        self.name_input = QLineEdit() 
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.working_hours_input = QLineEdit()
        self.monthly_salary_input = QLineEdit()
        
        self.name_input.setMaximumWidth(600)
        self.phone_input.setMaximumWidth(600) 
        self.email_input.setMaximumWidth(600) 
        self.working_hours_input.setMaximumWidth(600) 
        self.monthly_salary_input.setMaximumWidth(600) 

        # ربط زر Enter في الكيبورد بحفظ البيانات مباشرة
        self.name_input.returnPressed.connect(self.add_client_to_table)
        self.phone_input.returnPressed.connect(self.add_client_to_table)
        self.email_input.returnPressed.connect(self.add_client_to_table)
        self.working_hours_input.returnPressed.connect(self.add_client_to_table)
        self.monthly_salary_input.returnPressed.connect(self.add_client_to_table)

        form_layout.addRow(QLabel("Name of the client:"), self.name_input)
        form_layout.addRow(QLabel("Phone number:"), self.phone_input)
        form_layout.addRow(QLabel("Email address:"), self.email_input)
        form_layout.addRow(QLabel("Working Hours:"), self.working_hours_input)
        form_layout.addRow(QLabel("Monthly Salary:"), self.monthly_salary_input)

        main_layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.setMaximumWidth(75)
        self.save_button.clicked.connect(self.add_client_to_table)
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white; ")
        buttons_layout.addWidget(self.save_button)
        
        self.delete_button = QPushButton("Delete Client")
        self.delete_button.setMaximumWidth(150)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        self.delete_button.clicked.connect(self.delete_client_from_table)
        buttons_layout.addWidget(self.delete_button)
        
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Client Name", "Phone Number", "Email Address", "Working Hours", "Monthly Salary"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
      
        self.load_clients()

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def load_clients(self):
        self.table.setRowCount(0)
        self.cursor.execute("""
        SELECT id, name, phone, email, working_hours, monthly_salary
        FROM clients
        """)

        for id, name, phone, email, working_hours, monthly_salary in self.cursor.fetchall():
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.ItemDataRole.UserRole, id)

            self.table.setItem(row_count, 0, name_item)
            self.table.setItem(row_count, 1, QTableWidgetItem(phone))
            self.table.setItem(row_count, 2, QTableWidgetItem(email))
            self.table.setItem(row_count, 3, QTableWidgetItem(working_hours))
            self.table.setItem(row_count, 4, QTableWidgetItem(monthly_salary))

    def add_client_to_table(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        working_hours = self.working_hours_input.text()
        monthly_salary = self.monthly_salary_input.text()

        if name.strip() != "" and phone.strip() != "" and email.strip() != "" and working_hours.strip() != "" and monthly_salary.strip() != "":
            self.cursor.execute("""
            INSERT INTO clients (name, phone, email, working_hours, monthly_salary)
            VALUES (?, ?, ?, ?, ?)
            """, (name, phone, email, working_hours, monthly_salary))
            self.conn.commit()
            
            inserted_id = self.cursor.lastrowid

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            
            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.ItemDataRole.UserRole, inserted_id)
            
            self.table.setItem(row_count, 0, name_item)
            self.table.setItem(row_count, 1, QTableWidgetItem(phone))
            self.table.setItem(row_count, 2, QTableWidgetItem(email))
            self.table.setItem(row_count, 3, QTableWidgetItem(working_hours))
            self.table.setItem(row_count, 4, QTableWidgetItem(monthly_salary))

            self.name_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.working_hours_input.clear()
            self.monthly_salary_input.clear()
            self.name_input.setFocus()

    def delete_client_from_table(self): 
        current_row = self.table.currentRow()

        if current_row > -1:
            client_id = self.table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
            self.cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            self.conn.commit()
            self.table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a client from the table to delete.")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())