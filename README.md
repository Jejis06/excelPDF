# 🧾 Utility Bills PDF Generator & Email Sender

A comprehensive PyQt5 desktop application for generating utility bill PDFs from Excel data and automatically sending them via Gmail. Perfect for property managers, landlords, or businesses that need to generate and distribute multiple utility bills efficiently.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 📊 **Multi-Utility Support**
- **Water Bills** - Generate water utility bills with consumption tracking
- **Electric Bills** - Create electricity bills with usage calculations
- **Custom Templates** - Flexible PDF generation from Excel data

### 📧 **Advanced Email Integration**
- **Gmail OAuth 2.0** - Secure authentication (no app passwords needed)
- **Batch Email Sending** - Send multiple bills with progress tracking
- **Email Retry System** - Retry failed sends with one click
- **Smart Error Handling** - User-friendly error messages with solutions

### 📋 **PDF Management**
- **Real-time Status Tracking** - Monitor PDF generation and email status
- **Context Menu Actions** - Right-click to open, retry, or manage PDFs
- **Failed PDF Recovery** - Easy retry for failed generations or sends
- **Live Progress Updates** - Visual feedback during operations

### 🎨 **Modern User Interface**
- **Clean Design** - Modern PyQt5 interface with intuitive controls
- **Responsive Layout** - Adapts to different screen sizes
- **Status Indicators** - Color-coded status for easy monitoring
- **Threaded Operations** - Non-blocking UI during long operations

### 🔧 **Developer Features**
- **Executable Building** - One-click compilation to Windows/macOS executables
- **Comprehensive Logging** - Detailed but clean error reporting
- **OAuth Management** - Built-in Gmail logout and re-authentication
- **Settings Persistence** - Automatic saving of user preferences

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Gmail account with OAuth 2.0 credentials
- Excel files with utility data

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd excelPDF
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail OAuth:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download `credentials.json` file

4. **Run the application:**
   ```bash
   python app.py
   ```

## 📖 Usage Guide

### 🔐 **Gmail Setup**

1. **Configure OAuth:**
   - Click "Browse" next to "Credentials File"
   - Select your downloaded `credentials.json`
   - Click "❓ Help" for detailed OAuth setup instructions

2. **First-time Authentication:**
   - Click "Send Emails" to trigger OAuth flow
   - Browser will open for Google account authentication
   - Grant permissions for Gmail access
   - Token will be saved for future use

3. **Account Management:**
   - Use "🚪 Logout" button to switch accounts
   - Re-authenticate anytime by logging out first

### 📊 **Excel Data Preparation**

Your Excel files should contain columns for:
- **Names/Recipients** - Customer or tenant names
- **Email Addresses** - Destination emails
- **Usage Data** - Consumption values (water/electricity)
- **Billing Information** - Amounts, dates, account numbers

### 🧾 **Generating Bills**

1. **Select Tab:**
   - Choose "Water" or "Electric" tab
   - Each tab has independent settings

2. **Configure Settings:**
   - **Excel File:** Select your data file
   - **Output Directory:** Choose where PDFs are saved
   - **Email Settings:** Configure sender details

3. **Generate PDFs:**
   - Click "Generate PDFs" button
   - Monitor progress in the PDF list
   - Green = Success, Red = Failed, Blue = In Progress

4. **Send Emails:**
   - Review generated PDFs in the list
   - Click "Send Emails" to batch send
   - Use context menu for individual operations

### 🔄 **Managing Failed Operations**

#### **Failed PDF Generation:**
- Right-click failed PDFs → "🔄 Retry Generation"
- Or click "🔄 Remove Failed PDFs" to clean up

#### **Failed Email Sends:**
- Right-click failed emails → "🔄 Retry Failed Email"
- Or click "🔄 Retry Failed Emails" for bulk retry
- PDFs automatically reset to sendable status

## 🏗️ Building Executables

Create standalone executables for distribution without requiring Python installation.

### Quick Build

```bash
# macOS/Linux
./build.sh current          # Build for current platform
./build.sh windows          # Build for Windows
./build.sh macos            # Build for macOS

# Windows
build.bat current           # Build for current platform
build.bat windows           # Build for Windows
```

### Advanced Build Options

```bash
# Full control with Python script
python build_executable.py windows --onefile --clean
python build_executable.py macos --debug
python build_executable.py --help  # See all options
```

### Build Output
- **Single File:** `dist/UtilityBills.exe` (Windows) or `dist/UtilityBills` (macOS)
- **Directory:** `dist/UtilityBills/` (faster startup, multiple files)

## 📁 Project Structure

```
excelPDF/
├── app.py                  # Main application entry point
├── base_utility_tab.py     # Core UI and functionality
├── waterPage.py           # Water-specific implementations
├── electricPage.py        # Electric-specific implementations
├── mail_module.py         # Gmail integration and OAuth
├── data_lib.py           # Data processing utilities
├── base_doc.py           # PDF generation base classes
├── appLayout.ui          # Qt Designer UI file
├── requirements.txt      # Python dependencies
├── build_executable.py   # Executable build script
├── build.sh             # Unix build helper
├── build.bat            # Windows build helper
├── README.md            # This file
└── pdfs/                # Generated PDF output directory
```

## ⚙️ Configuration

### Settings Persistence
- All settings automatically saved on change
- OAuth tokens stored securely
- Email configurations preserved between sessions

### Data Files
- `data.json` - Water utility settings
- `data2.json` - Electric utility settings
- `token.pickle` - Gmail OAuth token (auto-generated)

## 🐛 Troubleshooting

### Common Issues

#### **"OAuth authentication failed"**
- **Solution:** Click "🚪 Logout" then re-authenticate
- **Cause:** Expired or invalid OAuth token

#### **"PDF file not found"**
- **Solution:** Regenerate PDFs before sending emails
- **Cause:** PDF was deleted or generation failed

#### **"Gmail SMTP authentication failed"**
- **Solution:** Check OAuth scope and re-authenticate
- **Cause:** Incorrect OAuth permissions

#### **"Excel file format error"**
- **Solution:** Verify Excel file has required columns
- **Cause:** Missing or incorrectly named data columns

### Debug Mode
Run with debug logging:
```bash
python build_executable.py current --debug
```

### Log Locations
- **Console Output:** Real-time status in application
- **Error Details:** Displayed in user-friendly dialog boxes

## 🔒 Security & Privacy

### OAuth 2.0 Implementation
- **No Password Storage** - Uses secure OAuth tokens only
- **Local Token Storage** - Credentials stored locally, not transmitted
- **Scope Limitation** - Only requests necessary Gmail permissions
- **Secure Authentication** - Google-managed authentication flow

### Data Handling
- **Local Processing** - All data processing happens locally
- **No Cloud Storage** - Excel data and PDFs remain on your system
- **Encrypted Tokens** - OAuth tokens stored in encrypted format

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📋 Requirements

### System Requirements
- **Operating System:** Windows 10+, macOS 10.14+, or Linux
- **Python:** 3.7 or higher
- **Memory:** 4GB RAM recommended
- **Storage:** 100MB+ free space for installation

### Python Dependencies
```
PyQt5>=5.15.0              # GUI framework
openpyxl>=3.0.0            # Excel file processing
requests>=2.25.0           # HTTP requests
pdfkit>=1.0.0              # PDF generation
google-auth>=2.0.0         # Google authentication
google-auth-oauthlib>=1.0.0 # OAuth implementation
google-auth-httplib2>=0.1.0 # HTTP transport
google-api-python-client>=2.0.0 # Gmail API
PyInstaller>=5.0.0         # Executable building
Pillow>=8.0.0              # Image processing (optional)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Issues:** Report bugs or request features via GitHub Issues
- **Documentation:** Check this README and inline help tooltips
- **OAuth Help:** Click "❓ Help" button in email settings for setup guide

### Contact
- **Developer:** Utility Bills Team
- **Version:** 1.0.4
- **Last Updated:** 2025

---

## 🎯 Key Benefits

✅ **Automated Workflow** - Generate hundreds of bills in minutes  
✅ **Professional PDFs** - Clean, consistent bill formatting  
✅ **Secure Email** - OAuth 2.0 authentication, no passwords  
✅ **Error Recovery** - Smart retry system for failed operations  
✅ **Cross-Platform** - Works on Windows, macOS, and Linux  
✅ **Standalone Builds** - No Python installation required for end users  
✅ **User-Friendly** - Intuitive interface with helpful error messages  

---

**Made with ❤️ for efficient utility bill management**
