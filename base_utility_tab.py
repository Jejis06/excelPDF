"""
Base class for utility tabs (Water and Electricity)
Provides shared functionality and modern UI components with live PDF tracking
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, 
                             QGroupBox, QLabel, QLineEdit, QTextEdit, QPushButton, 
                             QDateEdit, QFileDialog, QSplitter, QTableView, QTabWidget,
                             QPlainTextEdit, QToolBar, QInputDialog, QSizePolicy, QSpacerItem,
                             QScrollArea, QFrame, QMessageBox, QListWidget, QListWidgetItem,
                             QMenu, QAction, QCheckBox, QProgressBar)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QFontMetrics, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QSettings, QDate, QThread, QUrl
from PyQt5.QtGui import QDesktopServices
import data_lib
import os
import threading
import subprocess
import platform
from datetime import datetime


class PDFStatus:
    """PDF status constants"""
    PENDING = "pending"
    GENERATING = "generating"
    SUCCESS = "success"
    FAILED = "failed"
    SENDING = "sending"
    SENT = "sent"
    SEND_FAILED = "send_failed"


class PDFItem:
    """PDF item data structure"""
    def __init__(self, filename, recipient=None, status=PDFStatus.PENDING):
        self.filename = filename
        self.recipient = recipient or ""
        self.status = status
        self.error_message = ""
        self.timestamp = datetime.now()
        self.full_path = ""


class PDFGenerationThread(QThread):
    """Thread for PDF generation with progress signals"""
    pdf_started = pyqtSignal(str, str)  # filename, recipient
    pdf_completed = pyqtSignal(str, str, str)  # filename, recipient, full_path
    pdf_failed = pyqtSignal(str, str, str)  # filename, recipient, error
    generation_finished = pyqtSignal(list)  # list of generated files
    log_message = pyqtSignal(str)  # log messages from data_lib
    
    def __init__(self, settings, date_start, date_end):
        super().__init__()
        self.settings = settings
        self.date_start = date_start
        self.date_end = date_end
    
    def run(self):
        """Generate PDFs with progress updates"""
        try:
            dane = data_lib.Data(self.settings)
            users = dane.users
            generated_files = []
            
            # Generate PDFs for all users
            for user, user_data in users.items():
                recipient = user_data.get('MAIL', user)
                
                # Determine the file prefix based on user data
                if "STAWKA_KWH" in user_data and "ZUZYCIE_KWH" in user_data:
                    filename = f"PRAD_{user}.pdf"
                elif "SPRZEDAWCA" in user_data and "RACHUNEK_BANKOWY" in user_data:
                    filename = f"WODA_FORMAL_{user}.pdf"
                else:
                    filename = f"WODA_{user}.pdf"
                
                self.pdf_started.emit(filename, recipient)
            
            # Generate all PDFs at once (as data_lib does)
            with data_lib.Capturing() as output:
                try:
                    files = dane.generate_pdfs(self.date_start, self.date_end)
                    generated_files = files
                    
                    # Emit completion signals for successful files
                    for file_info in files:
                        user = file_info['user']
                        recipient = file_info['mail']
                        full_path = os.path.abspath(file_info['pdf_path'])
                        filename = os.path.basename(full_path)
                        
                        self.pdf_completed.emit(filename, recipient, full_path)
                    
                    # Emit log messages
                    for log_line in output:
                        self.log_message.emit(log_line)
                        
                        # Check for failed PDFs in the output
                        if "Failed to convert html to pdf" in log_line:
                            parts = log_line.split("|")
                            if len(parts) >= 3:
                                user = parts[1].strip()
                                recipient = parts[2].strip()
                                error = parts[0].split(":")[1].strip() if ":" in parts[0] else "Unknown error"
                                
                                # Determine filename for failed PDF
                                user_data = users.get(user, {})
                                if "STAWKA_KWH" in user_data and "ZUZYCIE_KWH" in user_data:
                                    filename = f"PRAD_{user}.pdf"
                                elif "SPRZEDAWCA" in user_data and "RACHUNEK_BANKOWY" in user_data:
                                    filename = f"WODA_FORMAL_{user}.pdf"
                                else:
                                    filename = f"WODA_{user}.pdf"
                                
                                self.pdf_failed.emit(filename, recipient, error)
                
                except Exception as e:
                    # If generation fails completely, emit failure for all pending users
                    for user, user_data in users.items():
                        recipient = user_data.get('MAIL', user)
                        if "STAWKA_KWH" in user_data and "ZUZYCIE_KWH" in user_data:
                            filename = f"PRAD_{user}.pdf"
                        elif "SPRZEDAWCA" in user_data and "RACHUNEK_BANKOWY" in user_data:
                            filename = f"WODA_FORMAL_{user}.pdf"
                        else:
                            filename = f"WODA_{user}.pdf"
                        
                        self.pdf_failed.emit(filename, recipient, str(e))
                    
                    raise e
            
            self.generation_finished.emit(generated_files)
            
        except Exception as e:
            self.pdf_failed.emit("", "", f"Generation process failed: {str(e)}")


class EmailSendingThread(QThread):
    """Thread for email sending with progress signals"""
    email_started = pyqtSignal(str, str)  # filename, recipient
    email_sent = pyqtSignal(str, str)  # filename, recipient
    email_failed = pyqtSignal(str, str, str)  # filename, recipient, error
    sending_finished = pyqtSignal()
    log_message = pyqtSignal(str)  # log messages from email sending
    
    def __init__(self, files, to_email, credentials_file, subject, message):
        super().__init__()
        self.files = files
        self.to_email = to_email
        self.credentials_file = credentials_file
        self.subject = subject
        self.message = message
    
    def run(self):
        """Send emails with concise progress updates"""
        try:
            self.log_message.emit(f"📧 Starting email sending for {len(self.files)} files")
            
            # Emit started signals for all files
            for file_info in self.files:
                filename = os.path.basename(file_info['pdf_path'])
                recipient = file_info['mail']
                self.email_started.emit(filename, recipient)
            
            # Send emails one by one for better error tracking
            successful_sends = []
            failed_sends = []
            
            for i, file_info in enumerate(self.files, 1):
                filename = os.path.basename(file_info['pdf_path'])
                recipient = file_info['mail']
                
                try:
                    self.log_message.emit(f"📤 Sending {i}/{len(self.files)}: {filename} → {recipient}")
                    
                    # Send individual email
                    import mail_module
                    mail_module.send_email_pdf_figs(
                        file_info['pdf_path'],      # path_to_pdf
                        self.subject,               # subject
                        self.message,               # message
                        file_info['mail'],          # destination (recipient)
                        self.to_email,              # mail (sender)
                        self.credentials_file,      # credentials_file_path
                        f"ROZL_{file_info['user']}.pdf"  # pdf_filename
                    )
                    
                    # Success
                    self.email_sent.emit(filename, recipient)
                    successful_sends.append(filename)
                    self.log_message.emit(f"✅ {filename} sent successfully")
                    
                except Exception as e:
                    # Failure - log the full error for debugging
                    full_error = str(e)
                    error_msg = self._extract_error_message(full_error)
                    self.email_failed.emit(filename, recipient, error_msg)
                    failed_sends.append((filename, error_msg))
                    self.log_message.emit(f"❌ {filename} failed: {error_msg}")
                    
                    # Log full error for debugging if it's an OAuth/SMTP issue
                    if any(keyword in full_error.lower() for keyword in ["oauth", "credential", "token", "smtp", "authentication", "server"]):
                        self.log_message.emit(f"🔍 Full error details: {full_error}")
                        if "oauth" in full_error.lower() or "credential" in full_error.lower():
                            self.log_message.emit("💡 This appears to be an OAuth setup issue. Try deleting token.pickle and re-authenticating.")
                        elif "smtp" in full_error.lower() or "server" in full_error.lower():
                            self.log_message.emit("💡 This appears to be an SMTP server issue. Check your OAuth scope and Gmail API settings.")
            
            # Summary
            self.log_message.emit(f"📊 Results: {len(successful_sends)} sent, {len(failed_sends)} failed")
            
            if failed_sends:
                self.log_message.emit("❌ Failed emails:")
                for filename, error in failed_sends:
                    self.log_message.emit(f"   • {filename}: {error}")
            
            self.sending_finished.emit()
            
        except Exception as e:
            self.log_message.emit(f"💥 Email sending failed: {self._extract_error_message(str(e))}")
            
            # Mark all files as failed
            for file_info in self.files:
                filename = os.path.basename(file_info['pdf_path'])
                recipient = file_info['mail']
                self.email_failed.emit(filename, recipient, str(e))
    
    def _extract_error_message(self, error_str):
        """Extract a concise error message from exception string"""
        # Common error patterns and their simplified versions
        error_patterns = [
            ("Failed to obtain OAuth 2.0 credentials", "OAuth setup required - check credentials.json"),
            ("No access token available", "OAuth token expired - re-authentication needed"),
            ("Gmail SMTP authentication failed", "OAuth/SMTP authentication failed - check scope"),
            ("Invalid credentials file format", "Invalid credentials.json file"),
            ("Credentials file not found", "credentials.json file missing"),
            ("File not found", "PDF file not found"),
            ("SMTP error", "Gmail SMTP server error - check OAuth setup"),
            ("SMTPAuthenticationError", "Gmail authentication failed - wrong scope or token"),
            ("ConnectionError", "Network connection failed"),
            ("TimeoutError", "Request timed out"),
            ("Permission denied", "OAuth permission denied"),
            ("invalid_grant", "OAuth tokens expired - delete token.pickle"),
            ("400 Bad Request", "Invalid OAuth request"),
            ("401 Unauthorized", "OAuth authentication failed"),
            ("403 Forbidden", "OAuth permission denied"),
            ("535", "Gmail authentication failed - check OAuth scope"),
            ("534", "Gmail authentication failed - app not verified"),
        ]
        
        error_lower = error_str.lower()
        
        for pattern, simplified in error_patterns:
            if pattern.lower() in error_lower:
                return simplified
        
        # If no pattern matches, return first sentence or first 100 chars
        if '. ' in error_str:
            return error_str.split('. ')[0]
        elif len(error_str) > 100:
            return error_str[:97] + "..."
        else:
            return error_str


def create_status_icon(status):
    """Create a colored icon for PDF status"""
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    if status == PDFStatus.PENDING:
        painter.setBrush(QColor("#6c757d"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(6, 11, "⏳")
    elif status == PDFStatus.GENERATING:
        painter.setBrush(QColor("#007bff"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(6, 11, "⚙")
    elif status == PDFStatus.SUCCESS:
        painter.setBrush(QColor("#28a745"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(5, 11, "✓")
    elif status == PDFStatus.FAILED:
        painter.setBrush(QColor("#dc3545"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(6, 11, "✗")
    elif status == PDFStatus.SENDING:
        painter.setBrush(QColor("#ffc107"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("black"))
        painter.drawText(5, 11, "📧")
    elif status == PDFStatus.SENT:
        painter.setBrush(QColor("#17a2b8"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(5, 11, "📨")
    elif status == PDFStatus.SEND_FAILED:
        painter.setBrush(QColor("#fd7e14"))
        painter.drawEllipse(2, 2, 12, 12)
        painter.setPen(QColor("white"))
        painter.drawText(6, 11, "❗")
    
    painter.end()
    return QIcon(pixmap)


class PDFListWidget(QListWidget):
    """Enhanced list widget for PDF tracking with context menu"""
    
    # Add signal for retry email operations
    retry_email_requested = pyqtSignal(list)  # list of pdf_items to retry
    
    def __init__(self):
        super().__init__()
        self.pdf_items = {}  # filename -> PDFItem
        self.setupUI()
        self.setupContextMenu()
    
    def setupUI(self):
        """Setup the PDF list widget"""
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemDoubleClicked.connect(self.open_pdf)
        
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                selection-background-color: #007bff;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
            }
        """)
    
    def setupContextMenu(self):
        """Setup context menu for PDF items"""
        self.context_menu = QMenu(self)
        
        # Open PDF action
        self.open_action = QAction("📂 Open PDF", self)
        self.open_action.triggered.connect(self.open_pdf)
        self.context_menu.addAction(self.open_action)
        
        # Open folder action
        self.folder_action = QAction("📁 Open Containing Folder", self)
        self.folder_action.triggered.connect(self.open_folder)
        self.context_menu.addAction(self.folder_action)
        
        self.context_menu.addSeparator()
        
        # Retry generation action
        self.retry_generation_action = QAction("🔄 Retry Generation", self)
        self.retry_generation_action.triggered.connect(self.retry_generation)
        self.context_menu.addAction(self.retry_generation_action)
        
        # Retry email action
        self.retry_email_action = QAction("📧 Retry Email", self)
        self.retry_email_action.triggered.connect(self.retry_email)
        self.context_menu.addAction(self.retry_email_action)
        
        self.context_menu.addSeparator()
        
        # Remove action
        self.remove_action = QAction("🗑️ Remove from List", self)
        self.remove_action.triggered.connect(self.remove_selected)
        self.context_menu.addAction(self.remove_action)
    
    def add_pdf_item(self, pdf_item):
        """Add a new PDF item to the list"""
        # Initialize selection state
        pdf_item.selected = True
        self.pdf_items[pdf_item.filename] = pdf_item
        
        # Create list widget item
        item = QListWidgetItem()
        item.setData(Qt.UserRole, pdf_item.filename)
        
        # Create checkbox widget
        checkbox = QCheckBox()
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(lambda state, fname=pdf_item.filename: self.update_selection(fname, state))
        
        # Create custom widget for the item
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Add checkbox
        layout.addWidget(checkbox)
        
        # Store checkbox reference for easy access
        widget.checkbox = checkbox
        widget.pdf_filename = pdf_item.filename  # Store filename reference
        
        # Add status and info
        self.update_item_display(item, pdf_item, widget, layout)
        
        # Add to list
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
    
    def update_item_display(self, item, pdf_item, widget, layout):
        """Update the visual display of a PDF item"""
        # Clear existing widgets (except checkbox at index 0)
        while layout.count() > 1:
            child = layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()
        
        # Status icon
        status_label = QLabel()
        status_label.setPixmap(create_status_icon(pdf_item.status).pixmap(16, 16))
        layout.addWidget(status_label)
        
        # PDF info
        info_label = QLabel(f"{pdf_item.filename}")
        if pdf_item.recipient:
            info_label.setText(f"{pdf_item.filename}\n📧 {pdf_item.recipient}")
        
        info_label.setStyleSheet("font-weight: 500; color: #495057;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Timestamp
        time_label = QLabel(pdf_item.timestamp.strftime("%H:%M:%S"))
        time_label.setStyleSheet("font-size: 11px; color: #6c757d;")
        layout.addWidget(time_label)
        
        # Set tooltip for errors
        if pdf_item.error_message:
            widget.setToolTip(f"Error: {pdf_item.error_message}")
        else:
            widget.setToolTip("")
        
        # Ensure checkbox state matches PDF item selection and reconnect signal
        if hasattr(widget, 'checkbox') and hasattr(pdf_item, 'selected'):
            # Disconnect old signal
            try:
                widget.checkbox.stateChanged.disconnect()
            except:
                pass
            
            # Set state
            widget.checkbox.setChecked(pdf_item.selected)
            
            # Reconnect signal
            filename = getattr(widget, 'pdf_filename', pdf_item.filename)
            widget.checkbox.stateChanged.connect(
                lambda state, fname=filename: self.update_selection(fname, state)
            )
    
    def update_pdf_status(self, filename, status, error_message="", full_path=""):
        """Update the status of a PDF item"""
        if filename in self.pdf_items:
            pdf_item = self.pdf_items[filename]
            
            # Preserve the current selection state
            current_selection = getattr(pdf_item, 'selected', True)
            
            pdf_item.status = status
            pdf_item.error_message = error_message
            if full_path:
                pdf_item.full_path = full_path
            
            # Restore selection state
            pdf_item.selected = current_selection
            
            # Find and update the corresponding list item
            for i in range(self.count()):
                item = self.item(i)
                if item.data(Qt.UserRole) == filename:
                    widget = self.itemWidget(item)
                    layout = widget.layout()
                    self.update_item_display(item, pdf_item, widget, layout)
                    break
            

    
    def update_selection(self, filename, state):
        """Update selection state for a PDF item"""
        if filename in self.pdf_items:
            self.pdf_items[filename].selected = state == Qt.Checked
            
            # Update the parent's select all checkbox if needed
            self.update_select_all_state()
    
    def update_select_all_state(self):
        """Update the select all checkbox based on individual selections"""
        if not self.pdf_items:
            return
            
        selected_count = sum(1 for item in self.pdf_items.values() if getattr(item, 'selected', False))
        total_count = len(self.pdf_items)
        
        # Find the parent's select all checkbox through the parent widget hierarchy
        parent = self.parent()
        while parent:
            select_all_checkbox = getattr(parent, 'select_all_checkbox', None)
            if select_all_checkbox:
                select_all_checkbox.blockSignals(True)
                if selected_count == 0:
                    select_all_checkbox.setCheckState(Qt.Unchecked)
                elif selected_count == total_count:
                    select_all_checkbox.setCheckState(Qt.Checked)
                else:
                    select_all_checkbox.setCheckState(Qt.PartiallyChecked)
                select_all_checkbox.blockSignals(False)
                break
            parent = parent.parent()
    
    def get_selected_items(self):
        """Get list of selected PDF items"""
        selected = []
        for filename, pdf_item in self.pdf_items.items():
            if hasattr(pdf_item, 'selected') and pdf_item.selected:
                selected.append(pdf_item)
        return selected
    
    def show_context_menu(self, position):
        """Show context menu at position with dynamic options based on PDF status"""
        item = self.itemAt(position)
        if item:
            filename = item.data(Qt.UserRole)
            pdf_item = self.pdf_items.get(filename)
            
            if pdf_item:
                # Enable/disable actions based on PDF status
                has_file = pdf_item.full_path and os.path.exists(pdf_item.full_path)
                
                # File operations only available if PDF exists
                self.open_action.setEnabled(has_file)
                self.folder_action.setEnabled(has_file)
                
                # Retry generation for failed generation
                self.retry_generation_action.setEnabled(pdf_item.status == PDFStatus.FAILED)
                
                # Retry email for successful PDFs that failed to send or haven't been sent
                can_retry_email = (pdf_item.status in [PDFStatus.SUCCESS, PDFStatus.SEND_FAILED] 
                                  and has_file and pdf_item.recipient)
                self.retry_email_action.setEnabled(can_retry_email)
                
                # Update action text based on status
                if pdf_item.status == PDFStatus.SEND_FAILED:
                    self.retry_email_action.setText("📧 Retry Failed Email")
                elif pdf_item.status == PDFStatus.SUCCESS:
                    self.retry_email_action.setText("📧 Send Email")
                else:
                    self.retry_email_action.setText("📧 Retry Email")
                
            self.context_menu.exec_(self.mapToGlobal(position))
    
    def open_pdf(self):
        """Open selected PDF in default viewer"""
        current_item = self.currentItem()
        if current_item:
            filename = current_item.data(Qt.UserRole)
            if filename in self.pdf_items:
                pdf_item = self.pdf_items[filename]
                if pdf_item.full_path and os.path.exists(pdf_item.full_path):
                    QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_item.full_path))
                else:
                    QMessageBox.warning(self, "File Not Found", f"PDF file not found: {pdf_item.filename}")
    
    def open_folder(self):
        """Open folder containing the PDF"""
        current_item = self.currentItem()
        if current_item:
            filename = current_item.data(Qt.UserRole)
            if filename in self.pdf_items:
                pdf_item = self.pdf_items[filename]
                if pdf_item.full_path and os.path.exists(pdf_item.full_path):
                    folder_path = os.path.dirname(pdf_item.full_path)
                    QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
    
    def retry_generation(self):
        """Retry generation for selected items"""
        # This would trigger a retry signal that the parent can handle
        selected_items = self.selectedItems()
        if selected_items:
            # For now, just reset status to pending
            for item in selected_items:
                filename = item.data(Qt.UserRole)
                self.update_pdf_status(filename, PDFStatus.PENDING)
    
    def retry_email(self):
        """Retry email sending for selected items"""
        selected_items = self.selectedItems()
        retry_items = []
        
        for item in selected_items:
            filename = item.data(Qt.UserRole)
            if filename in self.pdf_items:
                pdf_item = self.pdf_items[filename]
                # Only retry if PDF exists and has recipient
                if (pdf_item.status in [PDFStatus.SUCCESS, PDFStatus.SEND_FAILED] 
                    and pdf_item.full_path and os.path.exists(pdf_item.full_path)
                    and pdf_item.recipient):
                    retry_items.append(pdf_item)
        
        if retry_items:
            # Reset status to SUCCESS so they can be processed by send_emails
            for pdf_item in retry_items:
                pdf_item.status = PDFStatus.SUCCESS
                pdf_item.selected = True  # Ensure they're selected for sending
                # Update display
                self.update_pdf_status(pdf_item.filename, PDFStatus.SUCCESS, "", pdf_item.full_path)
            
            # Emit signal to parent to handle email retry
            self.retry_email_requested.emit(retry_items)
        else:
            QMessageBox.information(
                self,
                "No Items to Retry",
                "No valid items selected for email retry.\n\n"
                "Items must:\n"
                "• Be successfully generated PDFs\n"
                "• Have valid file paths\n"
                "• Have recipient email addresses"
            )
    
    def remove_selected(self):
        """Remove selected items from the list"""
        selected_items = self.selectedItems()
        for item in selected_items:
            filename = item.data(Qt.UserRole)
            if filename in self.pdf_items:
                del self.pdf_items[filename]
            self.takeItem(self.row(item))
    
    def clear_all(self):
        """Clear all items from the list"""
        self.clear()
        self.pdf_items.clear()
    
    def remove_failed(self):
        """Remove only failed items"""
        items_to_remove = []
        for i in range(self.count()):
            item = self.item(i)
            filename = item.data(Qt.UserRole)
            if filename in self.pdf_items:
                pdf_item = self.pdf_items[filename]
                if pdf_item.status in [PDFStatus.FAILED, PDFStatus.SEND_FAILED]:
                    items_to_remove.append((i, filename))
        
        # Remove in reverse order to maintain indices
        for i, filename in reversed(items_to_remove):
            del self.pdf_items[filename]
            self.takeItem(i)


class ModernEmailWidget(QGroupBox):
    """Modern email composition widget with improved layout and labels"""
    
    def __init__(self, title="Email Settings"):
        super().__init__(title)
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 24, 20, 20)
        
        # Email form layout with clear labels
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setVerticalSpacing(12)
        form_layout.setHorizontalSpacing(16)
        
        # To field
        to_label = QLabel("To:")
        to_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.to_field = QLineEdit()
        self.to_field.setPlaceholderText("recipient@example.com")
        self.to_field.setMinimumHeight(36)
        self.to_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow(to_label, self.to_field)
        
        # Credentials file field with file picker
        credentials_label = QLabel("Credentials:")
        credentials_label.setStyleSheet("font-weight: 600; color: #495057;")
        
        # Create horizontal layout for file picker
        credentials_layout = QHBoxLayout()
        credentials_layout.setSpacing(8)
        
        self.credentials_field = QLineEdit()
        self.credentials_field.setPlaceholderText("Select credentials.json file")
        self.credentials_field.setMinimumHeight(36)
        self.credentials_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        credentials_layout.addWidget(self.credentials_field)
        
        # Browse button for file picker
        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.setMinimumHeight(36)
        self.browse_btn.setMinimumWidth(80)
        self.browse_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_credentials_file)
        credentials_layout.addWidget(self.browse_btn)
        
        # Help button
        self.help_btn = QPushButton("❓ Help")
        self.help_btn.setMinimumHeight(36)
        self.help_btn.setMinimumWidth(70)
        self.help_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
        """)
        self.help_btn.clicked.connect(self.show_oauth_help)
        credentials_layout.addWidget(self.help_btn)
        
        # Logout button
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setToolTip("Clear OAuth tokens and logout from Gmail")
        self.logout_btn.setMinimumHeight(36)
        self.logout_btn.setMinimumWidth(80)
        self.logout_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                font-size: 12px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.logout_btn.clicked.connect(self.logout_gmail)
        credentials_layout.addWidget(self.logout_btn)
        
        # Create container widget for the layout
        credentials_widget = QWidget()
        credentials_widget.setLayout(credentials_layout)
        form_layout.addRow(credentials_label, credentials_widget)
        
        # Subject field
        subject_label = QLabel("Subject:")
        subject_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.subject_field = QLineEdit()
        self.subject_field.setPlaceholderText("Email subject")
        self.subject_field.setMinimumHeight(36)
        self.subject_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow(subject_label, self.subject_field)
        
        layout.addLayout(form_layout)
        
        # Message body section with clear label
        body_label = QLabel("Body:")
        body_label.setStyleSheet("font-weight: 600; color: #495057; margin-top: 8px;")
        layout.addWidget(body_label)
        
        # Toolbar for text formatting
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("""
            QToolBar { 
                border: 1px solid #dee2e6; 
                background: #f8f9fa; 
                spacing: 3px;
                padding: 6px;
                border-radius: 4px;
                margin-bottom: 4px;
            }
            QToolBar QToolButton { 
                padding: 6px 10px; 
                border: 1px solid transparent;
                border-radius: 3px;
                font-weight: 500;
                min-width: 24px;
            }
            QToolBar QToolButton:hover { 
                background: #e9ecef; 
                border: 1px solid #adb5bd;
            }
        """)
        
        # Add formatting actions
        bold_action = self.toolbar.addAction("B")
        bold_action.setToolTip("Bold (Ctrl+B)")
        italic_action = self.toolbar.addAction("I") 
        italic_action.setToolTip("Italic (Ctrl+I)")
        underline_action = self.toolbar.addAction("U")
        underline_action.setToolTip("Underline (Ctrl+U)")
        self.toolbar.addSeparator()
        list_action = self.toolbar.addAction("•")
        list_action.setToolTip("Insert List")
        link_action = self.toolbar.addAction("🔗")
        link_action.setToolTip("Insert Link")
        
        layout.addWidget(self.toolbar)
        
        # Message body - expandable and flexible height
        self.message_body = QTextEdit()
        self.message_body.setPlaceholderText("Type your message here...")
        self.message_body.setMinimumHeight(150)
        self.message_body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.message_body.setAcceptRichText(True)
        layout.addWidget(self.message_body)
        
        # Connect toolbar actions
        self.toolbar.actionTriggered.connect(self.handle_formatting)
    
    def handle_formatting(self, action):
        """Handle text formatting actions"""
        text = action.text()
        if text == "B":
            fmt = self.message_body.currentCharFormat()
            fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
            self.message_body.setCurrentCharFormat(fmt)
        elif text == "I":
            fmt = self.message_body.currentCharFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            self.message_body.setCurrentCharFormat(fmt)
        elif text == "U":
            fmt = self.message_body.currentCharFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            self.message_body.setCurrentCharFormat(fmt)
        elif text == "•":
            cursor = self.message_body.textCursor()
            cursor.insertList(QtGui.QTextListFormat.ListDisc)
        elif text == "🔗":
            cursor = self.message_body.textCursor()
            url, ok = QInputDialog.getText(self, "Insert Link", "URL:")
            if ok and url:
                cursor.insertHtml(f'<a href="{url}">{url}</a>')

    def browse_credentials_file(self):
        """Open file dialog to select credentials.json file"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JSON files (*.json);;All files (*.*)")
        file_dialog.setWindowTitle("Select Google OAuth 2.0 Credentials File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                credentials_path = selected_files[0]
                self.credentials_field.setText(credentials_path)
                
                # Test the credentials file
                self.test_credentials_file(credentials_path)
    
    def test_credentials_file(self, credentials_path):
        """Test if the selected credentials file is valid"""
        try:
            import mail_module
            success, email, error = mail_module.test_oauth_setup(credentials_path)
            
            if success:
                QMessageBox.information(
                    self,
                    "✅ Credentials Valid",
                    f"OAuth 2.0 credentials are valid!\n\nUser: {email}\n\nYou're ready to send emails securely."
                )
            else:
                QMessageBox.warning(
                    self,
                    "⚠️ Credentials Issue",
                    f"There's an issue with the credentials file:\n\n{error}\n\nPlease check the file and try again."
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "❌ Test Failed",
                f"Could not test credentials file:\n\n{str(e)}"
            )
    
    def show_oauth_help(self):
        """Show OAuth 2.0 setup instructions"""
        try:
            import mail_module
            instructions = mail_module.get_oauth_setup_instructions()
            
            # Create a message box with custom size
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("🔐 Gmail OAuth 2.0 Setup Instructions")
            msg_box.setText("Follow these steps to set up secure Gmail authentication:")
            msg_box.setDetailedText(instructions)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStandardButtons(QMessageBox.Ok)
            
            # Make the dialog larger to show more text
            msg_box.setStyleSheet("""
                QMessageBox {
                    min-width: 600px;
                    min-height: 400px;
                }
                QMessageBox QTextEdit {
                    min-width: 800px;
                    min-height: 500px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 12px;
                }
            """)
            
            msg_box.exec_()
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Help Error",
                f"Could not load help instructions:\n\n{str(e)}"
            )

    def logout_gmail(self):
        """Logout from Gmail by clearing OAuth tokens"""
        try:
            import os
            
            # Ask for confirmation
            reply = QMessageBox.question(
                self,
                "🚪 Logout from Gmail",
                "Are you sure you want to logout from Gmail?\n\n"
                "This will:\n"
                "• Clear your stored OAuth tokens\n"
                "• Require re-authentication for future email sending\n"
                "• Allow you to login with a different Gmail account",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Get the credentials file path to determine token location
                credentials_path = self.credentials_field.text()
                if credentials_path:
                    credentials_dir = os.path.dirname(credentials_path)
                    token_file = os.path.join(credentials_dir, 'token.pickle')
                else:
                    # Default token location
                    token_file = 'token.pickle'
                
                # Delete token file if it exists
                if os.path.exists(token_file):
                    os.remove(token_file)
                    QMessageBox.information(
                        self,
                        "✅ Logout Successful",
                        f"Successfully logged out from Gmail!\n\n"
                        f"• Deleted token file: {os.path.basename(token_file)}\n"
                        f"• Next email send will require re-authentication\n"
                        f"• You can now login with a different Gmail account"
                    )
                else:
                    QMessageBox.information(
                        self,
                        "ℹ️ Already Logged Out",
                        "No active Gmail session found.\n\n"
                        "You are already logged out or haven't authenticated yet."
                    )
                    
        except Exception as e:
            QMessageBox.warning(
                self,
                "❌ Logout Error",
                f"Could not logout from Gmail:\n\n{str(e)}\n\n"
                f"You may need to manually delete the token.pickle file."
            )

    def get_email_data(self):
        """Get email data as dictionary"""
        return {
            'to': self.to_field.text(),
            'credentials_file': self.credentials_field.text(),
            'subject': self.subject_field.text(),
            'message': self.message_body.toPlainText()
        }
    
    def set_email_data(self, data):
        """Set email data from dictionary"""
        self.to_field.setText(data.get('to', ''))
        self.credentials_field.setText(data.get('credentials_file', ''))
        self.subject_field.setText(data.get('subject', ''))
        self.message_body.setPlainText(data.get('message', ''))


class FileInputWidget(QGroupBox):
    """Modern file input widget with improved path handling and tooltips"""
    
    def __init__(self, title="Excel File Settings"):
        super().__init__(title)
        self.full_path = ""
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 24, 20, 20)
        
        # File path section with responsive layout
        file_layout = QHBoxLayout()
        file_layout.setSpacing(12)
        
        file_label = QLabel("Excel File:")
        file_label.setStyleSheet("font-weight: 600; color: #495057;")
        file_label.setMinimumWidth(90)
        file_layout.addWidget(file_label)
        
        # File path field that expands with window
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select an Excel file...")
        self.file_path.setMinimumHeight(36)
        self.file_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.file_path.textChanged.connect(self.update_display_path)
        file_layout.addWidget(self.file_path)
        
        # Browse button with fixed width
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setMinimumHeight(36)
        self.browse_button.setMinimumWidth(100)
        self.browse_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_button)
        
        layout.addLayout(file_layout)
        
        # Range settings with improved spacing
        range_layout = QGridLayout()
        range_layout.setVerticalSpacing(12)
        range_layout.setHorizontalSpacing(16)
        
        # Range start
        range_start_label = QLabel("Range Start:")
        range_start_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.range_start = QLineEdit()
        self.range_start.setPlaceholderText("A1")
        self.range_start.setMinimumHeight(36)
        self.range_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        range_layout.addWidget(range_start_label, 0, 0)
        range_layout.addWidget(self.range_start, 0, 1)
        
        # Range end
        range_end_label = QLabel("Range End:")
        range_end_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.range_end = QLineEdit()
        self.range_end.setPlaceholderText("Z100")
        self.range_end.setMinimumHeight(36)
        self.range_end.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        range_layout.addWidget(range_end_label, 1, 0)
        range_layout.addWidget(self.range_end, 1, 1)
        
        # Set column stretch
        range_layout.setColumnStretch(1, 1)
        
        layout.addLayout(range_layout)
    
    def update_display_path(self):
        """Update the display path with ellipsis for long paths"""
        path = self.file_path.text()
        if path:
            self.full_path = path
            # Truncate path if too long
            font_metrics = QFontMetrics(self.file_path.font())
            available_width = self.file_path.width() - 20  # Account for padding
            
            if font_metrics.horizontalAdvance(path) > available_width:
                # Show ellipsis for long paths
                filename = os.path.basename(path)
                dirname = os.path.dirname(path)
                if len(dirname) > 20:
                    truncated = "..." + dirname[-17:] + "/" + filename
                    self.file_path.setToolTip(f"Full path: {path}")
                else:
                    self.file_path.setToolTip(f"Full path: {path}")
            else:
                self.file_path.setToolTip("")
    
    def browse_file(self):
        """Open file dialog to select Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Excel File", 
            "", 
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_path:
            self.file_path.setText(file_path)
            self.full_path = file_path
    
    def get_file_data(self):
        """Get file data as dictionary"""
        return {
            'filename': self.full_path or self.file_path.text(),
            'rangeStart': self.range_start.text(),
            'rangeEnd': self.range_end.text()
        }
    
    def set_file_data(self, data):
        """Set file data from dictionary"""
        path = data.get('filename', '')
        self.file_path.setText(path)
        self.full_path = path
        self.range_start.setText(data.get('rangeStart', ''))
        self.range_end.setText(data.get('rangeEnd', ''))


class UtilityTab(QWidget):
    """Base class for utility tabs with improved layouts, persistent settings, and live PDF tracking"""
    
    def __init__(self, tab_type="water"):
        super().__init__()
        self.tab_type = tab_type
        self.files = None
        self.settings = QSettings("UtilityBills", f"UtilityTab_{tab_type}")
        self.pdf_generation_thread = None
        self.email_sending_thread = None
        self.setupUI()
        self.load_settings()
    
    def setupUI(self):
        """Setup the modern UI layout with improved spacing and responsiveness"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scrollable area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        # Create tab widget for sections
        self.section_tabs = QTabWidget()
        self.section_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.section_tabs)
        
        # Main section tab
        main_tab = QWidget()
        self.section_tabs.addTab(main_tab, "Configuration")
        
        # Data viewer tab
        data_tab = QWidget()
        self.section_tabs.addTab(data_tab, "Data Viewer")
        
        self.setup_main_tab(main_tab)
        self.setup_data_tab(data_tab)
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Connect tab change event
        self.section_tabs.currentChanged.connect(self.on_tab_changed)
    
    def setup_main_tab(self, tab_widget):
        """Setup the main configuration tab with improved layout"""
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Create horizontal splitter for better space utilization
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(splitter)
        
        # Left panel - Email and File settings
        left_panel = QWidget()
        left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(0, 0, 8, 0)
        
        # Email widget
        self.email_widget = ModernEmailWidget("📧 Email Settings")
        self.email_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.email_widget)
        
        # File widget
        self.file_widget = FileInputWidget("📁 Excel File Settings")
        self.file_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        left_layout.addWidget(self.file_widget)
        
        # Add stretch to push email widget to expand
        left_layout.addStretch()
        splitter.addWidget(left_panel)
        
        # Right panel - Data settings and specific fields
        right_panel = QWidget()
        right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(8, 0, 0, 0)
        
        # Data settings group
        self.data_group = QGroupBox("📊 Data Mapping & Settings")
        self.data_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setup_data_fields(self.data_group)
        right_layout.addWidget(self.data_group)
        
        # Add stretch
        right_layout.addStretch()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (45% left, 55% right)
        splitter.setSizes([450, 550])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        # Action buttons section
        self.setup_action_buttons(layout)
        
        # Output section
        self.setup_output_section(layout)
    
    def setup_data_fields(self, group_widget):
        """Setup data mapping fields with improved spacing"""
        layout = QVBoxLayout(group_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 24, 20, 20)
        
        # Common fields with improved grid layout
        common_group = QGroupBox("Common Settings")
        common_layout = QGridLayout(common_group)
        common_layout.setVerticalSpacing(12)
        common_layout.setHorizontalSpacing(16)
        
        # Create form fields with consistent styling
        fields = [
            ("Lokator:", "lokator_field"),
            ("Lokal Użytkowy:", "lokal_field"), 
            ("Mail Column:", "mail_field")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: 600; color: #495057;")
            label.setMinimumWidth(120)
            
            field = QLineEdit()
            field.setMinimumHeight(36)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            setattr(self, field_name, field)
            
            common_layout.addWidget(label, i, 0)
            common_layout.addWidget(field, i, 1)
        
        # Set column stretch
        common_layout.setColumnStretch(1, 1)
        
        layout.addWidget(common_group)
        
        # Additional fields will be added by subclasses
        self.add_specific_fields(layout)
    
    def add_specific_fields(self, layout):
        """Add tab-specific fields - to be overridden in subclasses"""
        pass
    
    def setup_action_buttons(self, layout):
        """Setup action buttons with improved layout and spacing"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        # Period selection group
        period_group = QGroupBox("📅 Billing Period")
        period_layout = QHBoxLayout(period_group)
        period_layout.setSpacing(12)
        period_layout.setContentsMargins(16, 16, 16, 16)
        
        period_layout.addWidget(QLabel("From:"))
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setMinimumHeight(36)
        self.date_start.setDate(QDate.currentDate().addMonths(-1))
        self.date_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        period_layout.addWidget(self.date_start)
        
        period_layout.addWidget(QLabel("To:"))
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setMinimumHeight(36)
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        period_layout.addWidget(self.date_end)
        
        button_layout.addWidget(period_group)
        
        # Action buttons group
        button_group = QGroupBox("⚡ Actions")
        action_layout = QHBoxLayout(button_group)
        action_layout.setSpacing(12)
        action_layout.setContentsMargins(16, 16, 16, 16)
        
        self.generate_btn = QPushButton("📄 Generate PDFs")
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.setMinimumWidth(140)
        self.generate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_pdfs)
        action_layout.addWidget(self.generate_btn)
        
        self.send_btn = QPushButton("📧 Send Emails")
        self.send_btn.setMinimumHeight(40)
        self.send_btn.setMinimumWidth(140)
        self.send_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.send_btn.clicked.connect(self.send_emails)
        action_layout.addWidget(self.send_btn)
        
        # Reset button
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.setMinimumWidth(140)
        self.reset_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
            QPushButton:pressed {
                background-color: #4e555b;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        action_layout.addWidget(self.reset_btn)
        
        button_layout.addWidget(button_group)
        
        layout.addWidget(button_container)
    
    def setup_output_section(self, layout):
        """Setup output/log section with PDF list and improved styling"""
        # Create horizontal splitter for output and PDF list
        output_splitter = QSplitter(Qt.Horizontal)
        output_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        output_splitter.setMaximumHeight(300)
        
        # Output log section
        output_group = QGroupBox("📋 Output Log")
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(16, 16, 16, 16)
        
        self.output_text = QPlainTextEdit()
        self.output_text.setMaximumHeight(220)
        self.output_text.setMinimumHeight(150)
        self.output_text.setPlaceholderText("Operation logs will appear here...")
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-family: "Monaco", "SF Mono", "Courier New", monospace;
                font-size: 12px;
                color: #495057;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        output_layout.addWidget(self.output_text)
        output_splitter.addWidget(output_group)
        
        # PDF list section
        pdf_group = QGroupBox("📄 Generated PDFs")
        pdf_layout = QVBoxLayout(pdf_group)
        pdf_layout.setContentsMargins(16, 16, 16, 16)
        
        # PDF list controls
        pdf_controls = QHBoxLayout()
        pdf_controls.setSpacing(8)
        
        self.clear_all_btn = QPushButton("🗑️ Clear All")
        self.clear_all_btn.setMinimumHeight(32)
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_pdf_list)
        pdf_controls.addWidget(self.clear_all_btn)
        
        self.remove_failed_btn = QPushButton("❌ Remove Failed")
        self.remove_failed_btn.setMinimumHeight(32)
        self.remove_failed_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.remove_failed_btn.clicked.connect(self.remove_failed_pdfs)
        pdf_controls.addWidget(self.remove_failed_btn)
        
        # Retry failed emails button
        self.retry_failed_btn = QPushButton("🔄 Retry Failed Emails")
        self.retry_failed_btn.setMinimumHeight(32)
        self.retry_failed_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e56305;
            }
        """)
        self.retry_failed_btn.clicked.connect(self.retry_failed_emails)
        pdf_controls.addWidget(self.retry_failed_btn)
        
        pdf_controls.addStretch()
        
        # Select all checkbox
        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.setStyleSheet("font-weight: 500; color: #495057;")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        pdf_controls.addWidget(self.select_all_checkbox)
        
        pdf_layout.addLayout(pdf_controls)
        
        # PDF list widget
        self.pdf_list = PDFListWidget()
        self.pdf_list.setMaximumHeight(180)
        self.pdf_list.setMinimumHeight(150)
        
        # Connect retry email signal
        self.pdf_list.retry_email_requested.connect(self.on_retry_email_requested)
        
        pdf_layout.addWidget(self.pdf_list)
        
        output_splitter.addWidget(pdf_group)
        
        # Set splitter proportions (60% output, 40% PDF list)
        output_splitter.setSizes([600, 400])
        
        layout.addWidget(output_splitter)
    
    def setup_data_tab(self, tab_widget):
        """Setup data viewer tab with improved layout"""
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header with refresh button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        header_label = QLabel("📊 Imported Excel Data")
        header_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #495057;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.setMinimumHeight(36)
        refresh_btn.clicked.connect(self.populate_data_table)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Data table
        self.data_table = QTableView()
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableView.SelectRows)
        self.data_table.setStyleSheet("""
            QTableView {
                gridline-color: #dee2e6;
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                selection-background-color: #007bff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.data_table)
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        if self.section_tabs.tabText(index) == "Data Viewer":
            self.populate_data_table()
    
    def populate_data_table(self):
        """Populate data table with Excel data"""
        try:
            settings = self.get_settings()
            dane = data_lib.Data(settings)
            users = dane.users
            
            if not users:
                self.output_text.appendPlainText("ℹ️ No data loaded. Please check file settings.")
                return
            
            headers = list(next(iter(users.values())).keys())
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(headers)
            
            for user, data in users.items():
                row = [QStandardItem(str(data.get(h, ""))) for h in headers]
                model.appendRow(row)
            
            self.data_table.setModel(model)
            self.data_table.resizeColumnsToContents()
            
            self.output_text.appendPlainText(f"✅ Loaded {len(users)} records from Excel file")
            
        except Exception as e:
            self.output_text.appendPlainText(f"❌ Error loading data: {str(e)}")
    
    def save_settings(self):
        """Save current settings using QSettings"""
        # Save email settings
        email_data = self.email_widget.get_email_data()
        self.settings.setValue("email/to", email_data['to'])
        self.settings.setValue("email/credentials_file", email_data['credentials_file'])
        self.settings.setValue("email/subject", email_data['subject'])
        self.settings.setValue("email/message", email_data['message'])
        
        # Save file settings
        file_data = self.file_widget.get_file_data()
        self.settings.setValue("file/filename", file_data['filename'])
        self.settings.setValue("file/rangeStart", file_data['rangeStart'])
        self.settings.setValue("file/rangeEnd", file_data['rangeEnd'])
        
        # Save dates
        self.settings.setValue("dates/start", self.date_start.date())
        self.settings.setValue("dates/end", self.date_end.date())
        
        # Save common fields
        self.settings.setValue("data/lokator", self.lokator_field.text())
        self.settings.setValue("data/lokal", self.lokal_field.text())
        self.settings.setValue("data/mail", self.mail_field.text())
        
        # Save tab-specific settings
        self.save_specific_settings()
    
    def save_specific_settings(self):
        """Save tab-specific settings - to be overridden in subclasses"""
        pass
    
    def reset_to_defaults(self):
        """Reset all fields to default values"""
        reply = QMessageBox.question(
            self, 
            "Reset to Defaults", 
            "Are you sure you want to reset all fields to their default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear QSettings
            self.settings.clear()
            
            # Reset UI fields to defaults
            self.email_widget.set_email_data({})
            self.file_widget.set_file_data({})
            self.lokator_field.clear()
            self.lokal_field.clear()
            self.mail_field.clear()
            self.date_start.setDate(QDate.currentDate().addMonths(-1))
            self.date_end.setDate(QDate.currentDate())
            
            # Reset tab-specific fields
            self.reset_specific_fields()
            
            self.output_text.appendPlainText("🔄 All settings reset to defaults")
    
    def reset_specific_fields(self):
        """Reset tab-specific fields - to be overridden in subclasses"""
        pass
    
    def get_settings(self):
        """Get settings dictionary - to be overridden in subclasses"""
        file_data = self.file_widget.get_file_data()
        email_data = self.email_widget.get_email_data()
        
        return {
            "data_settings": file_data,
            "user_data_settings": self.get_user_data_settings(),
            "mail_settings": {
                "ROOT_MAIL": email_data['to'],
                "AUTH": email_data['credentials_file'],
                "SUBJECT": email_data['subject'],
                "CONTENT": email_data['message'],
                "SPRZEDAWCA": "",
                "RACHUNEK_BANKOWY": ""
            }
        }
    
    def get_user_data_settings(self):
        """Get user data settings - to be overridden in subclasses"""
        return {
            "LOKATOR": self.lokator_field.text(),
            "LOKAL_URZYTKOWY": self.lokal_field.text(),
            "MAIL": self.mail_field.text(),
        }
    
    def load_settings(self):
        """Load settings using QSettings"""
        # Load email settings
        email_data = {
            'to': self.settings.value("email/to", ""),
            'credentials_file': self.settings.value("email/credentials_file", ""),
            'subject': self.settings.value("email/subject", ""),
            'message': self.settings.value("email/message", "")
        }
        self.email_widget.set_email_data(email_data)
        
        # Load file settings
        file_data = {
            'filename': self.settings.value("file/filename", ""),
            'rangeStart': self.settings.value("file/rangeStart", ""),
            'rangeEnd': self.settings.value("file/rangeEnd", "")
        }
        self.file_widget.set_file_data(file_data)
        
        # Load dates
        start_date = self.settings.value("dates/start")
        end_date = self.settings.value("dates/end")
        if start_date:
            self.date_start.setDate(start_date)
        if end_date:
            self.date_end.setDate(end_date)
        
        # Load common fields
        self.lokator_field.setText(self.settings.value("data/lokator", ""))
        self.lokal_field.setText(self.settings.value("data/lokal", ""))
        self.mail_field.setText(self.settings.value("data/mail", ""))
        
        # Load tab-specific settings
        self.load_specific_settings()
        
        # Also try to load from legacy JSON files for backward compatibility
        self.load_legacy_settings()
    
    def load_specific_settings(self):
        """Load tab-specific settings - to be overridden in subclasses"""
        pass
    
    def load_legacy_settings(self):
        """Load settings from legacy JSON files for backward compatibility"""
        filename = f'data{"2" if self.tab_type == "electric" else ""}.json'
        try:
            saved_data = data_lib.get_data(os.path.join(os.getcwd(), filename))
            
            if saved_data is None:
                return
            
            # Load file settings if not already loaded from QSettings
            if 'data_settings' in saved_data and not self.file_widget.file_path.text():
                self.file_widget.set_file_data(saved_data['data_settings'])
            
            # Load email settings if not already loaded from QSettings
            if 'mail_settings' in saved_data and not self.email_widget.to_field.text():
                mail_data = saved_data['mail_settings']
                email_data = {
                    'to': mail_data.get('ROOT_MAIL', ''),
                    'credentials_file': mail_data.get('AUTH', ''),
                    'subject': mail_data.get('SUBJECT', ''),
                    'message': mail_data.get('CONTENT', '')
                }
                self.email_widget.set_email_data(email_data)
            
            # Load user data settings if not already loaded
            if 'user_data_settings' in saved_data and not self.lokator_field.text():
                self.load_user_data_settings(saved_data['user_data_settings'])
        except Exception as e:
            print(f"Error loading legacy settings: {e}")
    
    def load_user_data_settings(self, user_data):
        """Load user data settings - to be overridden in subclasses"""
        self.lokator_field.setText(user_data.get('LOKATOR', ''))
        self.lokal_field.setText(user_data.get('LOKAL_URZYTKOWY', ''))
        self.mail_field.setText(user_data.get('MAIL', ''))
    
    def closeEvent(self, event):
        """Save settings and cleanup threads when tab is closed"""
        self.save_settings()
        
        # Wait for threads to finish
        if self.pdf_generation_thread and self.pdf_generation_thread.isRunning():
            self.pdf_generation_thread.quit()
            self.pdf_generation_thread.wait(3000)  # Wait up to 3 seconds
        
        if self.email_sending_thread and self.email_sending_thread.isRunning():
            self.email_sending_thread.quit()
            self.email_sending_thread.wait(3000)  # Wait up to 3 seconds
        
        event.accept()
    
    def clear_pdf_list(self):
        """Clear all PDFs from the list"""
        self.pdf_list.clear_all()
        self.output_text.appendPlainText("🗑️ PDF list cleared")
    
    def remove_failed_pdfs(self):
        """Remove failed PDFs from the list"""
        self.pdf_list.remove_failed()
        self.output_text.appendPlainText("❌ Failed PDFs removed from list")
    
    def toggle_select_all(self, state):
        """Toggle select all PDFs"""
        checked = state == Qt.Checked
        
        # Update the PDF items selection state
        for filename, pdf_item in self.pdf_list.pdf_items.items():
            pdf_item.selected = checked
        
        # Update the visual checkboxes
        for i in range(self.pdf_list.count()):
            item = self.pdf_list.item(i)
            widget = self.pdf_list.itemWidget(item)
            if widget and hasattr(widget, 'checkbox'):
                # Temporarily disconnect to avoid signal loops
                widget.checkbox.blockSignals(True)
                widget.checkbox.setChecked(checked)
                widget.checkbox.blockSignals(False)
        

    
    def generate_pdfs(self):
        """Generate PDFs using threaded approach with live updates"""
        try:
            if self.pdf_generation_thread and self.pdf_generation_thread.isRunning():
                self.output_text.appendPlainText("⚠️ PDF generation already in progress...")
                return
            
            self.output_text.appendPlainText("🔄 [STARTING PDF GENERATION...]")
            
            # Disable generate button during operation
            self.generate_btn.setEnabled(False)
            self.generate_btn.setText("⚙️ Generating...")
            
            settings = self.get_settings()
            date_start = self.date_start.date().toPyDate().strftime("%d.%m.%Y")
            date_end = self.date_end.date().toPyDate().strftime("%d.%m.%Y")
            
            # Create and start PDF generation thread
            self.pdf_generation_thread = PDFGenerationThread(settings, date_start, date_end)
            
            # Connect signals
            self.pdf_generation_thread.pdf_started.connect(self.on_pdf_started)
            self.pdf_generation_thread.pdf_completed.connect(self.on_pdf_completed)
            self.pdf_generation_thread.pdf_failed.connect(self.on_pdf_failed)
            self.pdf_generation_thread.generation_finished.connect(self.on_generation_finished)
            self.pdf_generation_thread.log_message.connect(self.on_log_message)
            
            self.pdf_generation_thread.start()
            
        except Exception as e:
            self.output_text.appendPlainText(f"❌ Error starting PDF generation: {str(e)}")
            self.generate_btn.setEnabled(True)
            self.generate_btn.setText("📄 Generate PDFs")
    
    def send_emails(self):
        """Send emails using threaded approach with concise logging"""
        try:
            if not self.pdf_list.pdf_items:
                self.output_text.appendPlainText("⚠️ No PDFs available for sending")
                return
            
            if self.email_sending_thread and self.email_sending_thread.isRunning():
                self.output_text.appendPlainText("⚠️ Email sending already in progress")
                return
            
            # Disable send button during operation
            self.send_btn.setEnabled(False)
            self.send_btn.setText("📤 Sending...")
            
            # Get and validate email configuration
            email_data = self.email_widget.get_email_data()
            
            if not email_data['to']:
                self.output_text.appendPlainText("❌ Recipient email address is empty")
                self._reset_send_button()
                return
            
            if not email_data['credentials_file']:
                self.output_text.appendPlainText("❌ OAuth credentials file not selected")
                self.output_text.appendPlainText("💡 Click 'Browse' to select credentials.json or 'Help' for setup")
                self._reset_send_button()
                return
            
            if not os.path.exists(email_data['credentials_file']):
                self.output_text.appendPlainText(f"❌ Credentials file not found: {email_data['credentials_file']}")
                self.output_text.appendPlainText("💡 Please set up OAuth 2.0 authentication:")
                self.output_text.appendPlainText("   1. Click 'Help' button for detailed setup instructions")
                self.output_text.appendPlainText("   2. Download credentials.json from Google Cloud Console")
                self.output_text.appendPlainText("   3. Select the file using the 'Browse' button")
                self._reset_send_button()
                return
            
            # Test OAuth setup
            self.output_text.appendPlainText("🔍 Testing OAuth setup...")
            try:
                import mail_module
                success, user_email, error = mail_module.test_oauth_setup(email_data['credentials_file'])
                
                if not success:
                    self.output_text.appendPlainText(f"❌ OAuth setup failed: {error}")
                    self.output_text.appendPlainText("💡 Solutions:")
                    if "not found" in error:
                        self.output_text.appendPlainText("   • Click 'Browse' to select your credentials.json file")
                        self.output_text.appendPlainText("   • Click 'Help' for setup instructions if you don't have the file")
                    elif "invalid" in error.lower() or "format" in error.lower():
                        self.output_text.appendPlainText("   • Download a new credentials.json from Google Cloud Console")
                        self.output_text.appendPlainText("   • Make sure it's an OAuth 2.0 Desktop Application credential")
                    elif "expired" in error.lower() or "invalid_grant" in error.lower():
                        self.output_text.appendPlainText("   • Delete token.pickle file and try again")
                        self.output_text.appendPlainText("   • You'll need to re-authorize the application")
                    elif "permission" in error.lower() or "forbidden" in error.lower():
                        self.output_text.appendPlainText("   • Check OAuth consent screen in Google Cloud Console")
                        self.output_text.appendPlainText("   • Make sure Gmail API is enabled")
                    elif "libraries" in error.lower():
                        self.output_text.appendPlainText("   • Install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2")
                    else:
                        self.output_text.appendPlainText("   • Check the error message and OAuth setup")
                        self.output_text.appendPlainText("   • Click 'Help' for detailed setup instructions")
                    
                    self._reset_send_button()
                    return
                else:
                    self.output_text.appendPlainText(f"✅ OAuth setup verified! Authenticated user: {user_email}")
                    
            except Exception as e:
                self.output_text.appendPlainText(f"❌ Error testing OAuth setup: {str(e)}")
                self._reset_send_button()
                return
            
            # Get selected PDFs
            selected_items = self.pdf_list.get_selected_items()
            
            if not selected_items:
                self.output_text.appendPlainText("⚠️ No PDFs selected for sending")
                self._reset_send_button()
                return
            
            # Process selected PDFs
            files_to_send = []
            skipped_count = 0
            
            for pdf_item in selected_items:
                if pdf_item.status == PDFStatus.SUCCESS and pdf_item.full_path and os.path.exists(pdf_item.full_path):
                    # Extract user from filename
                    filename_base = os.path.splitext(pdf_item.filename)[0]
                    if filename_base.startswith("PRAD_"):
                        user = filename_base[5:]
                    elif filename_base.startswith("WODA_FORMAL_"):
                        user = filename_base[12:]
                    elif filename_base.startswith("WODA_"):
                        user = filename_base[5:]
                    else:
                        user = filename_base
                    
                    files_to_send.append({
                        'user': user,
                        'mail': pdf_item.recipient,
                        'pdf_path': pdf_item.full_path
                    })
                else:
                    skipped_count += 1
            
            if not files_to_send:
                self.output_text.appendPlainText("❌ No valid PDFs ready for sending")
                self._reset_send_button()
                return
            
            # Log summary
            self.output_text.appendPlainText(f"📧 Sending emails: {len(files_to_send)} ready, {skipped_count} skipped")
            
            # Create and start email sending thread
            self.email_sending_thread = EmailSendingThread(
                files_to_send,
                email_data['to'],
                email_data['credentials_file'],
                email_data['subject'],
                email_data['message']
            )
            
            # Connect signals
            self.email_sending_thread.email_started.connect(self.on_email_started)
            self.email_sending_thread.email_sent.connect(self.on_email_sent)
            self.email_sending_thread.email_failed.connect(self.on_email_failed)
            self.email_sending_thread.sending_finished.connect(self.on_sending_finished)
            self.email_sending_thread.log_message.connect(self.on_email_log_message)
            
            self.email_sending_thread.start()
            
        except Exception as e:
            self.output_text.appendPlainText(f"❌ Email sending error: {str(e)}")
            self._reset_send_button()
    
    def _reset_send_button(self):
        """Helper to reset send button state"""
        self.send_btn.setEnabled(True)
        self.send_btn.setText("📧 Send Emails")
    
    # Signal handlers for logging
    def on_log_message(self, message):
        """Handle general log message from threads"""
        self.output_text.appendPlainText(f"📝 {message}")
    
    def on_email_log_message(self, message):
        """Handle email-specific log message from email thread"""
        self.output_text.appendPlainText(message)
    
    # Signal handlers for PDF generation
    def on_pdf_started(self, filename, recipient):
        """Handle PDF generation started signal"""
        self.output_text.appendPlainText(f"⚙️ Generating PDF: {filename}")
        pdf_item = PDFItem(filename, recipient, PDFStatus.GENERATING)
        self.pdf_list.add_pdf_item(pdf_item)
    
    def on_pdf_completed(self, filename, recipient, full_path):
        """Handle PDF generation completed signal"""
        self.output_text.appendPlainText(f"✅ PDF generated successfully: {filename}")
        self.pdf_list.update_pdf_status(filename, PDFStatus.SUCCESS, "", full_path)
    
    def on_pdf_failed(self, filename, recipient, error):
        """Handle PDF generation failed signal"""
        self.output_text.appendPlainText(f"❌ PDF generation failed: {filename} - {error}")
        self.pdf_list.update_pdf_status(filename, PDFStatus.FAILED, error)
    
    def on_generation_finished(self, files):
        """Handle PDF generation finished signal"""
        self.files = files
        successful_count = sum(1 for item in self.pdf_list.pdf_items.values() if item.status == PDFStatus.SUCCESS)
        failed_count = sum(1 for item in self.pdf_list.pdf_items.values() if item.status == PDFStatus.FAILED)
        
        self.output_text.appendPlainText(f"🏁 PDF generation completed: {successful_count} successful, {failed_count} failed")
        
        # Re-enable generate button
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("📄 Generate PDFs")
        
        self.save_settings()  # Auto-save after successful operation
    
    # Signal handlers for email sending
    def on_email_started(self, filename, recipient):
        """Handle email sending started signal"""
        self.pdf_list.update_pdf_status(filename, PDFStatus.SENDING)
    
    def on_email_sent(self, filename, recipient):
        """Handle email sent signal"""
        self.pdf_list.update_pdf_status(filename, PDFStatus.SENT)
    
    def on_email_failed(self, filename, recipient, error):
        """Handle email sending failed signal"""
        self.pdf_list.update_pdf_status(filename, PDFStatus.SEND_FAILED, error)
    
    def on_sending_finished(self):
        """Handle email sending finished signal"""
        # Calculate statistics
        sent_items = [item for item in self.pdf_list.pdf_items.values() if item.status == PDFStatus.SENT]
        failed_items = [item for item in self.pdf_list.pdf_items.values() if item.status == PDFStatus.SEND_FAILED]
        
        self.output_text.appendPlainText(f"🏁 Email sending completed: {len(sent_items)} sent, {len(failed_items)} failed")
        
        # Show failed items if any
        if failed_items:
            self.output_text.appendPlainText("❌ Failed emails:")
            for item in failed_items:
                error_msg = item.error_message if item.error_message else "Unknown error"
                self.output_text.appendPlainText(f"   • {item.filename}: {error_msg}")
        
        # Re-enable send button and save settings
        self._reset_send_button()
        self.save_settings()
    
    def on_retry_email_requested(self, retry_items):
        """Handle retry email request from PDF list"""
        if retry_items:
            self.output_text.appendPlainText(f"🔄 Retrying email for {len(retry_items)} item(s)...")
            # Trigger send_emails which will process the selected items
            self.send_emails()
    
    def retry_failed_emails(self):
        """Retry all failed email sends"""
        failed_items = [item for item in self.pdf_list.pdf_items.values() 
                       if item.status == PDFStatus.SEND_FAILED]
        
        if not failed_items:
            self.output_text.appendPlainText("ℹ️ No failed emails to retry")
            return
        
        # Reset failed items to SUCCESS status and select them
        retry_count = 0
        for pdf_item in failed_items:
            if pdf_item.full_path and os.path.exists(pdf_item.full_path) and pdf_item.recipient:
                pdf_item.status = PDFStatus.SUCCESS
                pdf_item.selected = True
                self.pdf_list.update_pdf_status(pdf_item.filename, PDFStatus.SUCCESS, "", pdf_item.full_path)
                retry_count += 1
        
        if retry_count > 0:
            self.output_text.appendPlainText(f"🔄 Retrying {retry_count} failed email(s)...")
            self.send_emails()
        else:
            self.output_text.appendPlainText("❌ No valid failed emails found to retry (missing files or recipients)") 