"""
Electricity utility tab implementation
Inherits from UtilityTab and adds electricity-specific fields
"""

from PyQt5.QtWidgets import QGridLayout, QLineEdit, QTextEdit, QGroupBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from base_utility_tab import UtilityTab
import data_lib
import os


class ElectricTab(UtilityTab):
    """Electricity utility tab with electricity-specific fields and improved layout"""
    
    def __init__(self):
        super().__init__(tab_type="electric")
    
    def add_specific_fields(self, layout):
        """Add electricity-specific fields to the data mapping section"""
        # Electricity usage group with improved grid layout
        electric_group = QGroupBox("⚡ Electricity Usage Settings")
        electric_layout = QGridLayout(electric_group)
        electric_layout.setVerticalSpacing(12)
        electric_layout.setHorizontalSpacing(16)
        
        # Electricity usage fields with consistent styling
        electric_fields = [
            ("Zużycie (kWh):", "zuzycie_kwh"),
            ("Stawka za kWh:", "stawka_kwh")
        ]
        
        for i, (label_text, field_name) in enumerate(electric_fields):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: 600; color: #495057;")
            label.setMinimumWidth(120)
            
            field = QLineEdit()
            field.setMinimumHeight(36)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            field.setPlaceholderText(f"Enter {label_text.lower().replace(':', '')}")
            setattr(self, field_name, field)
            
            electric_layout.addWidget(label, i, 0)
            electric_layout.addWidget(field, i, 1)
        
        # Set column stretch for responsive layout
        electric_layout.setColumnStretch(1, 1)
        
        layout.addWidget(electric_group)
        
        # Business information group (for formal invoices)
        business_group = QGroupBox("🏢 Business Information")
        business_layout = QGridLayout(business_group)
        business_layout.setVerticalSpacing(12)
        business_layout.setHorizontalSpacing(16)
        
        # Seller information
        sprzedawca_label = QLabel("Sprzedawca:")
        sprzedawca_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.sprzedawca = QTextEdit()
        self.sprzedawca.setMaximumHeight(80)
        self.sprzedawca.setMinimumHeight(60)
        self.sprzedawca.setPlaceholderText("Enter seller information...")
        self.sprzedawca.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(sprzedawca_label, 0, 0, Qt.AlignTop)
        business_layout.addWidget(self.sprzedawca, 0, 1)
        
        # Bank account
        bank_label = QLabel("Rachunek Bankowy:")
        bank_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.rachunek_bankowy = QLineEdit()
        self.rachunek_bankowy.setMinimumHeight(36)
        self.rachunek_bankowy.setPlaceholderText("Enter bank account number...")
        self.rachunek_bankowy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(bank_label, 1, 0)
        business_layout.addWidget(self.rachunek_bankowy, 1, 1)
        
        # Set column stretch
        business_layout.setColumnStretch(1, 1)
        
        layout.addWidget(business_group)
    
    def get_user_data_settings(self):
        """Get electricity-specific user data settings"""
        base_settings = super().get_user_data_settings()
        
        electric_settings = {
            "ZUZYCIE_KWH": self.zuzycie_kwh.text(),
            "STAWKA_KWH": self.stawka_kwh.text(),
        }
        
        # Merge with base settings
        base_settings.update(electric_settings)
        return base_settings
    
    def get_settings(self):
        """Get complete settings dictionary for electricity tab"""
        settings = super().get_settings()
        
        # Add seller and bank account to mail settings
        settings["mail_settings"]["SPRZEDAWCA"] = self.sprzedawca.toPlainText()
        settings["mail_settings"]["RACHUNEK_BANKOWY"] = self.rachunek_bankowy.text()
        
        return settings
    
    def save_specific_settings(self):
        """Save electricity-specific settings using QSettings"""
        # Save electricity usage fields
        self.settings.setValue("electric/zuzycie_kwh", self.zuzycie_kwh.text())
        self.settings.setValue("electric/stawka_kwh", self.stawka_kwh.text())
        
        # Save business information
        self.settings.setValue("electric/sprzedawca", self.sprzedawca.toPlainText())
        self.settings.setValue("electric/rachunek_bankowy", self.rachunek_bankowy.text())
    
    def load_specific_settings(self):
        """Load electricity-specific settings using QSettings"""
        # Load electricity usage fields
        self.zuzycie_kwh.setText(self.settings.value("electric/zuzycie_kwh", ""))
        self.stawka_kwh.setText(self.settings.value("electric/stawka_kwh", ""))
        
        # Load business information
        self.sprzedawca.setPlainText(self.settings.value("electric/sprzedawca", ""))
        self.rachunek_bankowy.setText(self.settings.value("electric/rachunek_bankowy", ""))
    
    def reset_specific_fields(self):
        """Reset electricity-specific fields to defaults"""
        # Clear electricity usage fields
        self.zuzycie_kwh.clear()
        self.stawka_kwh.clear()
        
        # Clear business information
        self.sprzedawca.clear()
        self.rachunek_bankowy.clear()
    
    def load_user_data_settings(self, user_data):
        """Load electricity-specific user data settings from legacy format"""
        super().load_user_data_settings(user_data)
        
        # Load electricity-specific fields if not already loaded from QSettings
        if not self.zuzycie_kwh.text():
            self.zuzycie_kwh.setText(user_data.get('ZUZYCIE_KWH', ''))
        if not self.stawka_kwh.text():
            self.stawka_kwh.setText(user_data.get('STAWKA_KWH', ''))
    
    def load_legacy_settings(self):
        """Load settings including seller and bank account info from legacy format"""
        super().load_legacy_settings()
        
        # Load additional mail settings if not already loaded from QSettings
        filename = 'data2.json'
        try:
            saved_data = data_lib.get_data(os.path.join(os.getcwd(), filename))
            
            if saved_data and 'mail_settings' in saved_data:
                mail_data = saved_data['mail_settings']
                if not self.sprzedawca.toPlainText():
                    self.sprzedawca.setPlainText(mail_data.get('SPRZEDAWCA', ''))
                if not self.rachunek_bankowy.text():
                    self.rachunek_bankowy.setText(mail_data.get('RACHUNEK_BANKOWY', ''))
        except Exception as e:
            print(f"Error loading legacy electric settings: {e}") 