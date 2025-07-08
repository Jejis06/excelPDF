"""
Water utility tab implementation
Inherits from UtilityTab and adds water-specific fields
"""

from PyQt5.QtWidgets import QGridLayout, QLineEdit, QTextEdit, QGroupBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from base_utility_tab import UtilityTab
import data_lib
import os


class WaterTab(UtilityTab):
    """Water utility tab with water-specific fields and improved layout"""
    
    def __init__(self):
        super().__init__(tab_type="water")
    
    def add_specific_fields(self, layout):
        """Add water-specific fields to the data mapping section"""
        # Water usage group with improved grid layout
        water_group = QGroupBox("💧 Water Usage Settings")
        water_layout = QGridLayout(water_group)
        water_layout.setVerticalSpacing(12)
        water_layout.setHorizontalSpacing(16)
        
        # Water usage fields with consistent styling
        water_fields = [
            ("Zużycie Wody Zimnej:", "zuzycie_zimnej"),
            ("Zużycie Wody Ciepłej:", "zuzycie_cieplej"),
            ("Stawka za Wodę Zimną:", "stawka_zimna"),
            ("Różnice Liczników:", "roznice_licznikow"),
            ("Koszt Stały Podgrzania:", "koszt_staly"),
            ("Stawka za Podgrzanie:", "stawka_podgrzanie")
        ]
        
        for i, (label_text, field_name) in enumerate(water_fields):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: 600; color: #495057;")
            label.setMinimumWidth(160)
            
            field = QLineEdit()
            field.setMinimumHeight(36)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            field.setPlaceholderText(f"Enter {label_text.lower().replace(':', '')}")
            setattr(self, field_name, field)
            
            row = i // 2
            col = (i % 2) * 2
            water_layout.addWidget(label, row, col)
            water_layout.addWidget(field, row, col + 1)
        
        # Set column stretch for responsive layout
        water_layout.setColumnStretch(1, 1)
        water_layout.setColumnStretch(3, 1)
        
        layout.addWidget(water_group)
        
        # Address and business information group
        business_group = QGroupBox("🏢 Business Information")
        business_layout = QGridLayout(business_group)
        business_layout.setVerticalSpacing(12)
        business_layout.setHorizontalSpacing(16)
        
        # Buyer information
        nabywca_label = QLabel("Nabywca:")
        nabywca_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.nabywca = QTextEdit()
        self.nabywca.setMaximumHeight(80)
        self.nabywca.setMinimumHeight(60)
        self.nabywca.setPlaceholderText("Enter buyer information...")
        self.nabywca.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(nabywca_label, 0, 0, Qt.AlignTop)
        business_layout.addWidget(self.nabywca, 0, 1)
        
        # Correspondence address
        adres_label = QLabel("Adres Korespondencyjny:")
        adres_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.adres_koresp = QTextEdit()
        self.adres_koresp.setMaximumHeight(80)
        self.adres_koresp.setMinimumHeight(60)
        self.adres_koresp.setPlaceholderText("Enter correspondence address...")
        self.adres_koresp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(adres_label, 1, 0, Qt.AlignTop)
        business_layout.addWidget(self.adres_koresp, 1, 1)
        
        # Seller information
        sprzedawca_label = QLabel("Sprzedawca:")
        sprzedawca_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.sprzedawca = QTextEdit()
        self.sprzedawca.setMaximumHeight(80)
        self.sprzedawca.setMinimumHeight(60)
        self.sprzedawca.setPlaceholderText("Enter seller information...")
        self.sprzedawca.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(sprzedawca_label, 2, 0, Qt.AlignTop)
        business_layout.addWidget(self.sprzedawca, 2, 1)
        
        # Bank account
        bank_label = QLabel("Rachunek Bankowy:")
        bank_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.rachunek_bankowy = QLineEdit()
        self.rachunek_bankowy.setMinimumHeight(36)
        self.rachunek_bankowy.setPlaceholderText("Enter bank account number...")
        self.rachunek_bankowy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        business_layout.addWidget(bank_label, 3, 0)
        business_layout.addWidget(self.rachunek_bankowy, 3, 1)
        
        # Set column stretch
        business_layout.setColumnStretch(1, 1)
        
        layout.addWidget(business_group)
    
    def get_user_data_settings(self):
        """Get water-specific user data settings"""
        base_settings = super().get_user_data_settings()
        
        water_settings = {
            "ZUZYCIE_WODY_ZIMNEJ": self.zuzycie_zimnej.text(),
            "ZUZYCIE_WODY_CIEPLEJ": self.zuzycie_cieplej.text(),
            "STAWKA_ZA_WODE_ZIMNA_I_SCIEKI": self.stawka_zimna.text(),
            "ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE": self.roznice_licznikow.text(),
            "KOSZT_STALY_PODGRZANIA": self.koszt_staly.text(),
            "STAWKA_ZA_PODGRZANIE_WODY": self.stawka_podgrzanie.text(),
            "NABYWCA": self.nabywca.toPlainText(),
            "ADRES_KORESPONDENCYJNY": self.adres_koresp.toPlainText(),
        }
        
        # Merge with base settings
        base_settings.update(water_settings)
        return base_settings
    
    def get_settings(self):
        """Get complete settings dictionary for water tab"""
        settings = super().get_settings()
        
        # Add seller and bank account to mail settings
        settings["mail_settings"]["SPRZEDAWCA"] = self.sprzedawca.toPlainText()
        settings["mail_settings"]["RACHUNEK_BANKOWY"] = self.rachunek_bankowy.text()
        
        return settings
    
    def save_specific_settings(self):
        """Save water-specific settings using QSettings"""
        # Save water usage fields
        self.settings.setValue("water/zuzycie_zimnej", self.zuzycie_zimnej.text())
        self.settings.setValue("water/zuzycie_cieplej", self.zuzycie_cieplej.text())
        self.settings.setValue("water/stawka_zimna", self.stawka_zimna.text())
        self.settings.setValue("water/roznice_licznikow", self.roznice_licznikow.text())
        self.settings.setValue("water/koszt_staly", self.koszt_staly.text())
        self.settings.setValue("water/stawka_podgrzanie", self.stawka_podgrzanie.text())
        
        # Save business information
        self.settings.setValue("water/nabywca", self.nabywca.toPlainText())
        self.settings.setValue("water/adres_koresp", self.adres_koresp.toPlainText())
        self.settings.setValue("water/sprzedawca", self.sprzedawca.toPlainText())
        self.settings.setValue("water/rachunek_bankowy", self.rachunek_bankowy.text())
    
    def load_specific_settings(self):
        """Load water-specific settings using QSettings"""
        # Load water usage fields
        self.zuzycie_zimnej.setText(self.settings.value("water/zuzycie_zimnej", ""))
        self.zuzycie_cieplej.setText(self.settings.value("water/zuzycie_cieplej", ""))
        self.stawka_zimna.setText(self.settings.value("water/stawka_zimna", ""))
        self.roznice_licznikow.setText(self.settings.value("water/roznice_licznikow", ""))
        self.koszt_staly.setText(self.settings.value("water/koszt_staly", ""))
        self.stawka_podgrzanie.setText(self.settings.value("water/stawka_podgrzanie", ""))
        
        # Load business information
        self.nabywca.setPlainText(self.settings.value("water/nabywca", ""))
        self.adres_koresp.setPlainText(self.settings.value("water/adres_koresp", ""))
        self.sprzedawca.setPlainText(self.settings.value("water/sprzedawca", ""))
        self.rachunek_bankowy.setText(self.settings.value("water/rachunek_bankowy", ""))
    
    def reset_specific_fields(self):
        """Reset water-specific fields to defaults"""
        # Clear water usage fields
        self.zuzycie_zimnej.clear()
        self.zuzycie_cieplej.clear()
        self.stawka_zimna.clear()
        self.roznice_licznikow.clear()
        self.koszt_staly.clear()
        self.stawka_podgrzanie.clear()
        
        # Clear business information
        self.nabywca.clear()
        self.adres_koresp.clear()
        self.sprzedawca.clear()
        self.rachunek_bankowy.clear()
    
    def load_user_data_settings(self, user_data):
        """Load water-specific user data settings from legacy format"""
        super().load_user_data_settings(user_data)
        
        # Load water-specific fields if not already loaded from QSettings
        if not self.zuzycie_zimnej.text():
            self.zuzycie_zimnej.setText(user_data.get('ZUZYCIE_WODY_ZIMNEJ', ''))
        if not self.zuzycie_cieplej.text():
            self.zuzycie_cieplej.setText(user_data.get('ZUZYCIE_WODY_CIEPLEJ', ''))
        if not self.stawka_zimna.text():
            self.stawka_zimna.setText(user_data.get('STAWKA_ZA_WODE_ZIMNA_I_SCIEKI', ''))
        if not self.roznice_licznikow.text():
            self.roznice_licznikow.setText(user_data.get('ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE', ''))
        if not self.koszt_staly.text():
            self.koszt_staly.setText(user_data.get('KOSZT_STALY_PODGRZANIA', ''))
        if not self.stawka_podgrzanie.text():
            self.stawka_podgrzanie.setText(user_data.get('STAWKA_ZA_PODGRZANIE_WODY', ''))
        if not self.nabywca.toPlainText():
            self.nabywca.setPlainText(user_data.get('NABYWCA', ''))
        if not self.adres_koresp.toPlainText():
            self.adres_koresp.setPlainText(user_data.get('ADRES_KORESPONDENCYJNY', ''))
    
    def load_legacy_settings(self):
        """Load settings including seller and bank account info from legacy format"""
        super().load_legacy_settings()
        
        # Load additional mail settings if not already loaded from QSettings
        filename = 'data.json'
        try:
            saved_data = data_lib.get_data(os.path.join(os.getcwd(), filename))
            
            if saved_data and 'mail_settings' in saved_data:
                mail_data = saved_data['mail_settings']
                if not self.sprzedawca.toPlainText():
                    self.sprzedawca.setPlainText(mail_data.get('SPRZEDAWCA', ''))
                if not self.rachunek_bankowy.text():
                    self.rachunek_bankowy.setText(mail_data.get('RACHUNEK_BANKOWY', ''))
        except Exception as e:
            print(f"Error loading legacy water settings: {e}") 