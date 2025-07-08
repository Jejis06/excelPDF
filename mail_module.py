"""
Gmail OAuth 2.0 Email Module
Handles email sending using Gmail SMTP with OAuth 2.0 authentication instead of app passwords.
"""

import os
import pickle
import smtplib
import base64
import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False
    print("⚠️ Google OAuth libraries not available. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2")


# OAuth 2.0 scope for Gmail SMTP sending
SCOPES = ['https://mail.google.com/']


def get_oauth_credentials(credentials_file_path):
    """
    Get OAuth 2.0 credentials for Gmail authentication
    
    Args:
        credentials_file_path: Path to the credentials.json file
        
    Returns:
        Credentials object or None if authentication fails
    """
    if not GOOGLE_APIS_AVAILABLE:
        raise ImportError("Google OAuth libraries not available. Please install required packages.")
    
    if not os.path.exists(credentials_file_path):
        raise FileNotFoundError(f"Credentials file not found: {credentials_file_path}")
    
    # Derive token file path from credentials file path
    credentials_dir = os.path.dirname(credentials_file_path)
    token_file = os.path.join(credentials_dir, 'token.pickle')
    
    creds = None
    
    # Load existing token if available
    if os.path.exists(token_file):
        try:
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        except Exception:
            creds = None
    
    # If there are no (valid) credentials available, request authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        try:
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        except Exception:
            pass  # Token saving failed, but we can continue
    
    return creds


def generate_oauth_string(email, access_token):
    """
    Generate OAuth 2.0 authentication string for SMTP
    
    Args:
        email: Email address of the authenticated user
        access_token: OAuth 2.0 access token
        
    Returns:
        Base64 encoded OAuth string
    """
    auth_string = f'user={email}\x01auth=Bearer {access_token}\x01\x01'
    return base64.b64encode(auth_string.encode()).decode()


def send_email_pdf_figs(path_to_pdf, subject, message, destination, mail, credentials_file_path, pdf_filename):
    """
    Send email with PDF attachment using Gmail SMTP with OAuth 2.0 authentication
    
    Args:
        path_to_pdf: Path to the PDF file to attach
        subject: Email subject
        message: Email body text
        destination: Recipient email address
        mail: Sender email address (should match the OAuth authenticated account)
        credentials_file_path: Path to the credentials.json file for OAuth 2.0
        pdf_filename: Name for the PDF attachment
    """
    try:
        # Get OAuth 2.0 credentials
        creds = get_oauth_credentials(credentials_file_path)
        if not creds:
            raise Exception("Failed to obtain OAuth 2.0 credentials")
        
        # Get access token
        access_token = creds.token
        if not access_token:
            raise Exception("No access token available")
        
        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = mail
        msg['To'] = destination
        
        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        
        # Attach the pdf to the msg going by e-mail
        if not os.path.exists(path_to_pdf):
            raise FileNotFoundError(f"PDF file not found: {path_to_pdf}")
        
        with open(path_to_pdf, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
        msg.attach(attach)
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Authenticate using OAuth 2.0
        oauth_string = generate_oauth_string(mail, access_token)
        server.docmd('AUTH', 'XOAUTH2 ' + oauth_string)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        
    except FileNotFoundError as e:
        raise Exception(f"PDF file not found: {str(e)}")
    
    except smtplib.SMTPAuthenticationError as e:
        raise Exception(f"Gmail SMTP authentication failed: {str(e)}")
    
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error: {str(e)}")
    
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")


def test_oauth_setup(credentials_file_path):
    """
    Test OAuth 2.0 setup and authentication
    
    Args:
        credentials_file_path: Path to the credentials.json file
        
    Returns:
        tuple: (success: bool, email: str or None, error: str or None)
    """
    try:
        if not GOOGLE_APIS_AVAILABLE:
            return False, None, "Google OAuth libraries not available. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2"
        
        if not os.path.exists(credentials_file_path):
            return False, None, f"Credentials file not found: {credentials_file_path}"
        
        # Test credential loading
        with open(credentials_file_path, 'r') as f:
            creds_data = json.load(f)
        
        # Check if it's a valid OAuth client credentials file
        if 'installed' not in creds_data and 'web' not in creds_data:
            return False, None, "Invalid credentials file format. Expected OAuth 2.0 client credentials from Google Cloud Console."
        
        # Try to get OAuth credentials (this might trigger browser auth)
        creds = get_oauth_credentials(credentials_file_path)
        if not creds:
            return False, None, "Failed to obtain OAuth credentials"
        
        # Check if we have a valid access token
        if not creds.token:
            return False, None, "No access token available"
        
        # Get user email (if available)
        user_email = "OAuth User"
        
        return True, user_email, None
        
    except Exception as e:
        error_msg = str(e)
        if "invalid_grant" in error_msg.lower():
            return False, None, "OAuth tokens expired. Delete token.pickle and try again."
        elif "403" in error_msg or "forbidden" in error_msg.lower():
            return False, None, "OAuth permission denied. Check your Google Cloud Console settings."
        else:
            return False, None, f"OAuth setup error: {error_msg}"


def get_oauth_setup_instructions():
    """
    Get detailed instructions for setting up OAuth 2.0 with Gmail
    
    Returns:
        str: Formatted instructions
    """
    return """
🔐 Gmail OAuth 2.0 Setup Instructions

Follow these steps to set up secure Gmail authentication:

1. **Go to Google Cloud Console**
   • Open: https://console.cloud.google.com/
   • Sign in with your Google account

2. **Create a New Project** (if needed)
   • Click "Select a project" → "New Project"
   • Enter a project name → Click "Create"
   • Wait for project creation to complete

3. **Enable Gmail API**
   • Go to "APIs & Services" → "Library"
   • Search for "Gmail API"
   • Click on "Gmail API" → Click "Enable"

4. **Configure OAuth Consent Screen**
   • Go to "APIs & Services" → "OAuth consent screen"
   • Choose "External" → Click "Create"
   • Fill in required fields:
     - App name: Your application name
     - User support email: Your email address
     - Developer contact information: Your email address
   • Click "Save and Continue" through all steps
   • Add your email to test users if in testing mode

5. **Create OAuth 2.0 Credentials**
   • Go to "APIs & Services" → "Credentials"
   • Click "Create Credentials" → "OAuth client ID"
   • Application type: "Desktop application"
   • Name: Choose any name (e.g., "Email App")
   • Click "Create"

6. **Download credentials.json**
   • Click the download button (⬇️) next to your OAuth client
   • Save the file as "credentials.json"
   • Keep this file secure and private

7. **Install Required Python Packages**
   Run this command in your terminal:
   pip install google-auth google-auth-oauthlib google-auth-httplib2

8. **Use the credentials.json file**
   • Select the downloaded credentials.json file in the app
   • The first time you send an email, a browser will open
   • Sign in and grant permission to send emails
   • Future emails will use saved tokens automatically

⚠️ **Important Security Notes:**
• Keep credentials.json private and secure
• Don't share token.pickle files with others
• You can revoke access anytime in your Google Account settings
• The app only requests permission to send emails (minimal scope)

🔧 **Troubleshooting:**
• Make sure Gmail API is enabled in your project
• Verify your email is added as a test user
• Check that the credentials file is valid JSON
• Ensure you're using the correct Google account

For more help, visit: https://developers.google.com/gmail/api/quickstart/python
    """.strip()


# Example usage and testing
if __name__ == "__main__":
    def test_oauth_email():
        """Test OAuth email functionality"""
        credentials_path = "credentials.json"
        
        if not os.path.exists(credentials_path):
            print(f"❌ Credentials file not found: {credentials_path}")
            print("\n" + get_oauth_setup_instructions())
            return
        
        # Test OAuth setup
        success, email, error = test_oauth_setup(credentials_path)
        if not success:
            print(f"❌ OAuth setup test failed: {error}")
            return
        
        print(f"✅ OAuth setup test successful! User: {email}")
        print("\n📧 To test email sending, use send_email_pdf_figs() with a valid PDF file")
    
    test_oauth_email()
