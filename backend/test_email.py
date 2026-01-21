"""
Test script to diagnose email sending issues
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

def test_email_config():
    """Test email configuration"""
    print("=" * 60)
    print("Email Configuration Test")
    print("=" * 60)
    
    # Check environment variables
    sender_email = "ashup2707@gmail.com"
    receiver_email = "f20201480g@alumni.bits-pilani.ac.in"
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    print(f"\n✓ Sender Email: {sender_email}")
    print(f"✓ Receiver Email: {receiver_email}")
    print(f"✓ SMTP Server: {smtp_server}")
    print(f"✓ SMTP Port: {smtp_port}")
    
    if sender_password:
        # Mask password for security
        masked = sender_password[:4] + "*" * (len(sender_password) - 8) + sender_password[-4:] if len(sender_password) > 8 else "*" * len(sender_password)
        print(f"✓ SENDER_PASSWORD: {masked} (length: {len(sender_password)})")
        # Check for spaces
        if " " in sender_password:
            print(f"⚠️  Password contains spaces - will be removed automatically")
            sender_password = sender_password.replace(" ", "")
            print(f"   After removing spaces: {masked.replace(' ', '')} (length: {len(sender_password)})")
    else:
        print("✗ SENDER_PASSWORD: NOT SET")
        print("\n❌ Error: SENDER_PASSWORD is missing in .env file")
        return False
    
    # Test SMTP connection
    print("\n" + "=" * 60)
    print("Testing SMTP Connection...")
    print("=" * 60)
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        print(f"\n1. Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("   ✓ Connection established")
        
        print("2. Starting TLS...")
        server.starttls()
        print("   ✓ TLS started")
        
        print("3. Attempting login...")
        server.login(sender_email, sender_password)
        print("   ✓ Login successful!")
        
        print("4. Creating test email...")
        msg = MIMEText("This is a test email from the Travel Planner.")
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Test Email - Travel Planner"
        
        print("5. Sending test email...")
        server.send_message(msg)
        print("   ✓ Test email sent successfully!")
        
        server.quit()
        print("\n✅ All email tests passed!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're using a Gmail App Password (not your regular password)")
        print("2. Generate a new App Password: https://myaccount.google.com/apppasswords")
        print("3. Copy the 16-character password exactly (spaces are OK, they'll be removed)")
        print("4. Make sure 2-Step Verification is enabled on your Google account")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP Error: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_generation():
    """Test PDF generation"""
    print("\n" + "=" * 60)
    print("Testing PDF Generation...")
    print("=" * 60)
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO
        
        print("\n1. Testing reportlab import...")
        print("   ✓ reportlab imported successfully")
        
        print("2. Creating test PDF...")
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = [Paragraph("Test PDF", styles['Title'])]
        doc.build(elements)
        buffer.seek(0)
        
        pdf_size = len(buffer.getvalue())
        print(f"   ✓ PDF created successfully (size: {pdf_size} bytes)")
        
        print("\n✅ PDF generation test passed!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nTroubleshooting:")
        print("Install reportlab: pip install reportlab")
        return False
        
    except Exception as e:
        print(f"\n❌ PDF Generation Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🔍 Email & PDF Diagnostic Test\n")
    
    # Test PDF generation first
    pdf_ok = test_pdf_generation()
    
    # Test email configuration
    email_ok = test_email_config()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"PDF Generation: {'✅ PASS' if pdf_ok else '❌ FAIL'}")
    print(f"Email Configuration: {'✅ PASS' if email_ok else '❌ FAIL'}")
    
    if pdf_ok and email_ok:
        print("\n🎉 All tests passed! Email sending should work.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")