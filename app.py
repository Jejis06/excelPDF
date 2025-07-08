# -*- coding: utf-8 -*-
"""
Modern Utility Bills Application
Generates and sends water and electricity bills based on Excel data
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QVBoxLayout, 
                             QWidget, QAction, QMenuBar, QSizePolicy, QStyleFactory,
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer
import data_lib
import PyQt5
import os
import sys

# Import our new modern tab classes
from water_tab import WaterTab
from electric_tab import ElectricTab


def apply_modern_style(app):
    """Apply modern styling to the application"""
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Modern color palette
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(245, 245, 245))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(33, 37, 41))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(248, 249, 250))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(33, 37, 41))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(248, 249, 250))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(33, 37, 41))
    palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(220, 53, 69))
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(0, 123, 255))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 123, 255))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)


class ModernMainWindow(QMainWindow):
    """Modern main window with responsive design and auto-save"""
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupMenuBar()
        self.setupAutoSave()
        
    def setupUI(self):
        """Setup the main window UI"""
        self.setWindowTitle("Rozliczenia - Utility Bills Manager")
        self.setMinimumSize(1400, 900)  # Increased minimum size for better layout
        
        # Set window icon (if available)
        try:
            self.setWindowIcon(QtGui.QIcon('icon.svg'))
        except:
            pass
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget for main sections
        self.main_tabs = QTabWidget()
        self.main_tabs.setTabPosition(QTabWidget.North)
        self.main_tabs.setMovable(False)
        self.main_tabs.setDocumentMode(True)
        
        # Apply modern tab styling
        self.main_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #c0c4c7;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #c0c4c7;
                border-bottom: none;
                padding: 16px 32px;
                margin-right: 2px;
                font-weight: 600;
                font-size: 15px;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #007bff;
                color: #007bff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e9ecef;
            }
        """)
        
        # Create water tab
        self.water_tab = WaterTab()
        self.main_tabs.addTab(self.water_tab, "💧 Water Bills")
        
        # Create electricity tab
        self.electric_tab = ElectricTab()
        self.main_tabs.addTab(self.electric_tab, "⚡ Electricity Bills")
        
        # Set size policy for responsive design
        self.main_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout.addWidget(self.main_tabs)
        
        # Status bar with better styling
        self.statusBar().showMessage("Ready - Application loaded successfully")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                padding: 6px 12px;
                font-size: 12px;
                color: #6c757d;
            }
        """)
    
    def setupAutoSave(self):
        """Setup auto-save timer to periodically save settings"""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_settings)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
    
    def auto_save_settings(self):
        """Auto-save settings for both tabs"""
        try:
            self.water_tab.save_settings()
            self.electric_tab.save_settings()
            # Update status bar to show last save time
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            self.statusBar().showMessage(f"Settings auto-saved at {current_time}")
        except Exception as e:
            print(f"Auto-save error: {e}")
    
    def setupMenuBar(self):
        """Setup the menu bar with improved organization"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #343a40;
                color: white;
                padding: 6px;
                font-weight: 500;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 10px 16px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #495057;
            }
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 4px 0px;
            }
            QMenu::item {
                padding: 8px 16px;
                color: #495057;
            }
            QMenu::item:selected {
                background-color: #007bff;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #dee2e6;
                margin: 4px 0px;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        # Import Excel action
        import_action = QAction('📂 &Import Excel File...', self)
        import_action.setShortcut('Ctrl+O')
        import_action.setStatusTip('Import Excel file for processing')
        import_action.triggered.connect(self.import_excel_file)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Save settings action
        save_action = QAction('💾 &Save Settings', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save current settings')
        save_action.triggered.connect(self.manual_save_settings)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('🚪 E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        # Reset to defaults action
        reset_action = QAction('🔄 &Reset to Defaults', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.setStatusTip('Reset all settings to default values')
        reset_action.triggered.connect(self.reset_to_defaults)
        edit_menu.addAction(reset_action)
        
        edit_menu.addSeparator()
        
        # Reset current tab action
        reset_tab_action = QAction('🔄 Reset Current &Tab', self)
        reset_tab_action.setShortcut('Ctrl+Shift+R')
        reset_tab_action.setStatusTip('Reset current tab settings to defaults')
        reset_tab_action.triggered.connect(self.reset_current_tab)
        edit_menu.addAction(reset_tab_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        # Switch tabs actions
        switch_water_action = QAction('💧 Switch to &Water', self)
        switch_water_action.setShortcut('Ctrl+1')
        switch_water_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(0))
        view_menu.addAction(switch_water_action)
        
        switch_electric_action = QAction('⚡ Switch to &Electricity', self)
        switch_electric_action.setShortcut('Ctrl+2')
        switch_electric_action.triggered.connect(lambda: self.main_tabs.setCurrentIndex(1))
        view_menu.addAction(switch_electric_action)
        
        view_menu.addSeparator()
        
        # Scale submenu
        scale_menu = view_menu.addMenu('🔍 &Scale')
        
        scale_options = [
            ('50%', 0.5),
            ('75%', 0.75),
            ('100%', 1.0),
            ('125%', 1.25),
            ('150%', 1.5),
            ('200%', 2.0)
        ]
        
        for name, factor in scale_options:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=factor: self.set_scale(f))
            scale_menu.addAction(action)
        
        # Tools menu
        tools_menu = menubar.addMenu('&Tools')
        
        # Generate PDFs action
        generate_action = QAction('📄 &Generate PDFs', self)
        generate_action.setShortcut('Ctrl+G')
        generate_action.setStatusTip('Generate PDF bills for current tab')
        generate_action.triggered.connect(self.generate_pdfs_current_tab)
        tools_menu.addAction(generate_action)
        
        # Send emails action
        send_action = QAction('📧 &Send Emails', self)
        send_action.setShortcut('Ctrl+E')
        send_action.setStatusTip('Send emails for current tab')
        send_action.triggered.connect(self.send_emails_current_tab)
        tools_menu.addAction(send_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        # User guide action
        guide_action = QAction('📖 &User Guide', self)
        guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(guide_action)
        
        # About action
        about_action = QAction('ℹ️ &About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def import_excel_file(self):
        """Import Excel file to current tab"""
        current_tab = self.main_tabs.currentWidget()
        if hasattr(current_tab, 'file_widget'):
            current_tab.file_widget.browse_file()
            self.statusBar().showMessage("Excel file selection opened")
    
    def manual_save_settings(self):
        """Manually save settings for both tabs"""
        try:
            self.water_tab.save_settings()
            self.electric_tab.save_settings()
            QMessageBox.information(self, "Settings Saved", "All settings have been saved successfully.")
            self.statusBar().showMessage("Settings saved manually")
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Error saving settings: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, 
            "Reset All Settings", 
            "Are you sure you want to reset ALL settings in both tabs to their default values?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.water_tab.reset_to_defaults()
            self.electric_tab.reset_to_defaults()
            self.statusBar().showMessage("All settings reset to defaults")
    
    def reset_current_tab(self):
        """Reset current tab to defaults"""
        current_tab = self.main_tabs.currentWidget()
        tab_name = self.main_tabs.tabText(self.main_tabs.currentIndex())
        
        reply = QMessageBox.question(
            self, 
            "Reset Tab Settings", 
            f"Are you sure you want to reset all settings in the {tab_name} tab to their default values?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            current_tab.reset_to_defaults()
            self.statusBar().showMessage(f"{tab_name} settings reset to defaults")
    
    def generate_pdfs_current_tab(self):
        """Generate PDFs for current tab"""
        current_tab = self.main_tabs.currentWidget()
        current_tab.generate_pdfs()
        self.statusBar().showMessage("PDF generation initiated")
    
    def send_emails_current_tab(self):
        """Send emails for current tab"""
        current_tab = self.main_tabs.currentWidget()
        current_tab.send_emails()
        self.statusBar().showMessage("Email sending initiated")
    
    def set_scale(self, scale_factor):
        """Set application scale factor"""
        os.environ["QT_SCALE_FACTOR"] = str(scale_factor)
        QMessageBox.information(
            self, 
            "Scale Changed", 
            f"Scale set to {int(scale_factor * 100)}%.\n\nRestart the application to apply changes."
        )
        self.statusBar().showMessage(f"Scale set to {int(scale_factor * 100)}% (restart required)")
    
    def show_user_guide(self):
        """Show user guide dialog"""
        QMessageBox.information(
            self,
            "User Guide",
            """
            <h3>📖 Utility Bills Manager - User Guide</h3>
            
            <h4>🚀 Getting Started:</h4>
            <p><b>1.</b> Import Excel files using File → Import Excel File (Ctrl+O)</p>
            <p><b>2.</b> Configure email settings in the Email Settings section</p>
            <p><b>3.</b> Set up data mapping fields for your Excel structure</p>
            <p><b>4.</b> Select billing period using the date selectors</p>
            <p><b>5.</b> Generate PDFs and send emails</p>
            
            <h4>⚡ Quick Actions:</h4>
            <p><b>Ctrl+1/2:</b> Switch between Water/Electricity tabs</p>
            <p><b>Ctrl+G:</b> Generate PDFs for current tab</p>
            <p><b>Ctrl+E:</b> Send emails for current tab</p>
            <p><b>Ctrl+S:</b> Save settings manually</p>
            <p><b>Ctrl+R:</b> Reset all settings to defaults</p>
            
            <h4>💾 Auto-Save:</h4>
            <p>Settings are automatically saved every 30 seconds and when you close the application.</p>
            
            <h4>🔄 Reset Options:</h4>
            <p><b>Reset to Defaults:</b> Clears all saved settings</p>
            <p><b>Reset Current Tab:</b> Clears only the active tab's settings</p>
            """
        )
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Rozliczenia",
            """
            <h3>💧⚡ Utility Bills Manager v2.0</h3>
            <p>A modern, professional application for generating and sending utility bills based on Excel data.</p>
            
            <p><b>✨ Key Features:</b></p>
            <ul>
                <li>🏢 Water and electricity bill generation</li>
                <li>📊 Excel data import and processing</li>
                <li>📧 Rich email composition and sending</li>
                <li>📄 PDF generation and management</li>
                <li>🎨 Modern, responsive interface</li>
                <li>💾 Persistent settings with auto-save</li>
                <li>🔄 Easy reset and configuration options</li>
            </ul>
            
            <p><b>🛠️ Built with:</b> PyQt5, Python</p>
            <p><b>📅 Updated:</b> 2024</p>
            
            <p style="color: #007bff;"><i>Designed for efficiency and ease of use.</i></p>
            """
        )
    
    def closeEvent(self, event):
        """Handle application close event with final settings save"""
        try:
            # Stop auto-save timer
            self.auto_save_timer.stop()
            
            # Final save of settings
            self.water_tab.save_settings()
            self.electric_tab.save_settings()
            
            # Also save to legacy JSON format for backward compatibility
            try:
                water_settings = self.water_tab.get_settings()
                electric_settings = self.electric_tab.get_settings()
                
                data_lib.save_data('data.json', water_settings)
                data_lib.save_data('data2.json', electric_settings)
            except Exception as e:
                print(f"Error saving legacy settings: {e}")
            
            self.statusBar().showMessage("Settings saved successfully")
        except Exception as e:
            print(f"Error saving settings on close: {e}")
        
        event.accept()


def main():
    """Main application entry point"""
    # Enable high DPI scaling
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    # Set auto screen scale factor
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "2")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Rozliczenia")
    app.setApplicationDisplayName("Utility Bills Manager")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Utility Bills")
    
    # Apply modern styling
    apply_modern_style(app)
    
    # Load custom stylesheet
    try:
        with open('styles.qss', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass  # Stylesheet is optional
    
    # Create and show main window
    window = ModernMainWindow()
    window.show()
    
    # Center window on screen
    screen = app.desktop().screenGeometry()
    window.move(
        (screen.width() - window.width()) // 2,
        (screen.height() - window.height()) // 2
    )
    
    # Start event loop
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass


if __name__ == "__main__":
    main()
