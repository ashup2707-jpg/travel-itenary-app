"""
Email sender module for sending itineraries
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any
from dotenv import load_dotenv
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# Load environment variables
try:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except Exception:
    pass


class EmailSender:
    """
    Email sender for itineraries using SMTP
    """
    
    def __init__(self):
        """Initialize email sender with configuration from environment"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        # Hardcoded emails as per user requirement
        self.sender_email = "ashup2707@gmail.com"
        self.receiver_email = "f20201480g@alumni.bits-pilani.ac.in"
        sender_password_raw = os.getenv("SENDER_PASSWORD", "").strip()
        # Remove spaces from password (Gmail app passwords may have spaces)
        self.sender_password = sender_password_raw.replace(" ", "")
        
        if not self.sender_password:
            raise ValueError(
                "Email configuration missing. Set SENDER_PASSWORD in .env file.\n"
                "For Gmail: Use an App Password (https://myaccount.google.com/apppasswords)\n"
                "Sender email is hardcoded to: ashup2707@gmail.com"
            )
    
    def format_itinerary_html(self, itinerary: Dict[str, Any]) -> str:
        """
        Format itinerary as HTML email
        
        Args:
            itinerary: Itinerary dictionary
        
        Returns:
            HTML string
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 10px; }
                h2 { color: #764ba2; margin-top: 30px; }
                h3 { color: #667eea; margin-top: 20px; }
                .stats { background: #f5f7fa; padding: 15px; border-radius: 8px; margin: 20px 0; }
                .day-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .time-block { background: #f8fafc; border-left: 4px solid #667eea; padding: 12px; margin: 10px 0; border-radius: 6px; }
                .morning { border-left-color: #fb923c; background: #fff7ed; }
                .afternoon { border-left-color: #fbbf24; background: #fef3c7; }
                .evening { border-left-color: #3b82f6; background: #dbeafe; }
                .poi-item { margin: 8px 0 8px 20px; }
                .feasibility-badge { display: inline-block; padding: 5px 12px; border-radius: 20px; color: white; font-weight: bold; font-size: 0.9em; }
                .high { background: #4caf50; }
                .medium { background: #ff9800; }
                .low { background: #f44336; }
                .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 0.9em; text-align: center; }
            </style>
        </head>
        <body>
            <h1>✈️ Your Travel Itinerary</h1>
        """
        
        if "days" in itinerary:
            days = itinerary["days"]
            total_pois = sum(
                len(block.get("pois", []))
                for day in days
                for block in day.get("blocks", [])
            )
            
            html += f"""
            <div class="stats">
                <strong>📅 Duration:</strong> {len(days)} days<br>
                <strong>📍 Places to Visit:</strong> {total_pois} locations<br>
            </div>
            """
            
            for day in days:
                day_num = day.get("day", 0)
                date = day.get("date", "")
                feasibility = day.get("feasibilityScore", 1.0)
                
                # Determine feasibility class
                feas_class = "high" if feasibility >= 0.8 else "medium" if feasibility >= 0.6 else "low"
                
                html += f"""
                <div class="day-card">
                    <h2>Day {day_num} {f'- {date}' if date else ''}</h2>
                    <span class="feasibility-badge {feas_class}">✓ {int(feasibility * 100)}% Feasible</span>
                """
                
                for block in day.get("blocks", []):
                    block_type = block.get("type", "")
                    pois = block.get("pois", [])
                    
                    if not pois:
                        continue
                    
                    time_info = block.get("time", {})
                    time_str = ""
                    if time_info:
                        start = time_info.get("start", "")
                        end = time_info.get("end", "")
                        if start and end:
                            time_str = f" • {start} - {end}"
                    
                    icon = "🌅" if block_type == "morning" else "☀️" if block_type == "afternoon" else "🌆"
                    
                    html += f"""
                    <div class="time-block {block_type}">
                        <h3>{icon} {block_type.capitalize()}{time_str}</h3>
                    """
                    
                    for poi in pois:
                        poi_name = poi.get("poiId", "").replace("node/", "").replace("way/", "").replace("relation/", "").replace("_", " ")
                        duration = poi.get("duration", "")
                        
                        html += f"""
                        <div class="poi-item">
                            • {poi_name}
                            {f'<span style="color: #64748b;"> (🕐 {duration} min)</span>' if duration else ''}
                        </div>
                        """
                    
                    travel_time = block.get("travelTime", 0)
                    if travel_time and travel_time > 0:
                        html += f'<div style="margin-top: 10px; color: #64748b; font-size: 0.9em;">🚗 {travel_time} min travel time</div>'
                    
                    html += "</div>"
                
                total_travel = day.get("totalTravelTime", 0)
                if total_travel and total_travel > 0:
                    html += f'<div style="margin-top: 15px; color: #64748b; text-align: right;">Total Travel Time: {total_travel} minutes</div>'
                
                html += "</div>"
        
        html += """
            <div class="footer">
                <p>🌟 This itinerary was created by Voyage - Your AI Travel Planning Assistant</p>
                <p>Have a wonderful trip!</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def generate_pdf(self, itinerary: Dict[str, Any]) -> BytesIO:
        """
        Generate PDF from itinerary
        
        Args:
            itinerary: Itinerary dictionary
        
        Returns:
            BytesIO buffer containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=20
        )
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=8,
            spaceBefore=12
        )
        normal_style = styles['Normal']
        
        # Title
        elements.append(Paragraph("✈️ Your Travel Itinerary", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        if "days" in itinerary:
            days = itinerary["days"]
            total_pois = sum(
                len(block.get("pois", []))
                for day in days
                for block in day.get("blocks", [])
            )
            
            # Stats
            stats_data = [
                ['📅 Duration', f'{len(days)} days'],
                ['📍 Places to Visit', f'{total_pois} locations']
            ]
            stats_table = Table(stats_data, colWidths=[2*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f7fa')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Days
            for day_idx, day in enumerate(days):
                if day_idx > 0:
                    elements.append(PageBreak())
                
                day_num = day.get("day", 0)
                date = day.get("date", "")
                feasibility = day.get("feasibilityScore", 1.0)
                
                # Day header
                date_str = f" - {date}" if date else ""
                day_title = f"Day {day_num}{date_str}"
                elements.append(Paragraph(day_title, heading_style))
                
                # Feasibility badge
                feas_color = colors.HexColor('#4caf50') if feasibility >= 0.8 else colors.HexColor('#ff9800') if feasibility >= 0.6 else colors.HexColor('#f44336')
                feas_text = f"✓ {int(feasibility * 100)}% Feasible"
                feas_para = Paragraph(f'<b><font color="{feas_color.hex()}">{feas_text}</font></b>', normal_style)
                elements.append(feas_para)
                elements.append(Spacer(1, 0.15*inch))
                
                # Blocks
                for block in day.get("blocks", []):
                    block_type = block.get("type", "")
                    pois = block.get("pois", [])
                    
                    if not pois:
                        continue
                    
                    time_info = block.get("time", {})
                    time_str = ""
                    if time_info:
                        start = time_info.get("start", "")
                        end = time_info.get("end", "")
                        if start and end:
                            time_str = f" • {start} - {end}"
                    
                    icon = "🌅" if block_type == "morning" else "☀️" if block_type == "afternoon" else "🌆"
                    block_title = f"{icon} {block_type.capitalize()}{time_str}"
                    elements.append(Paragraph(block_title, subheading_style))
                    
                    # POIs
                    for poi in pois:
                        poi_name = poi.get("name") or poi.get("poiId", "").replace("node/", "").replace("way/", "").replace("relation/", "").replace("_", " ")
                        duration = poi.get("duration", "")
                        duration_str = f" (🕐 {duration} min)" if duration else ""
                        poi_text = f"• {poi_name}{duration_str}"
                        elements.append(Paragraph(poi_text, normal_style))
                        elements.append(Spacer(1, 0.05*inch))
                    
                    # Travel time
                    travel_time = block.get("travelTime", 0)
                    if travel_time and travel_time > 0:
                        travel_text = f"🚗 {travel_time} min travel time"
                        elements.append(Paragraph(travel_text, ParagraphStyle('TravelTime', parent=normal_style, fontSize=9, textColor=colors.grey)))
                        elements.append(Spacer(1, 0.1*inch))
                
                # Total travel time for day
                total_travel = day.get("totalTravelTime", 0)
                if total_travel and total_travel > 0:
                    total_travel_text = f"<b>Total Travel Time: {total_travel} minutes</b>"
                    elements.append(Paragraph(total_travel_text, ParagraphStyle('TotalTravel', parent=normal_style, alignment=TA_LEFT)))
                    elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=normal_style,
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("🌟 This itinerary was created by Voyage - Your AI Travel Planning Assistant", footer_style))
        elements.append(Paragraph("Have a wonderful trip!", footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def send_itinerary(
        self,
        itinerary: Dict[str, Any],
        recipient_emails: List[str] = None,
        subject: str = "Your Travel Itinerary from Voyage"
    ) -> Dict[str, Any]:
        """
        Send itinerary to email addresses with PDF attachment
        
        Args:
            itinerary: Itinerary dictionary
            recipient_emails: List of recipient email addresses (defaults to hardcoded receiver)
            subject: Email subject line
        
        Returns:
            Dictionary with success status and message
        """
        # Use hardcoded receiver email if not provided
        if recipient_emails is None or len(recipient_emails) == 0:
            recipient_emails = [self.receiver_email]
        
        try:
            # Generate PDF
            print("Generating PDF...")
            try:
                pdf_buffer = self.generate_pdf(itinerary)
                print("PDF generated successfully")
            except Exception as pdf_error:
                print(f"PDF generation error: {pdf_error}")
                raise Exception(f"Failed to generate PDF: {str(pdf_error)}")
            
            # Create message
            msg = MIMEMultipart('mixed')
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(recipient_emails)
            msg['Subject'] = subject
            
            # Create HTML version
            html_content = self.format_itinerary_html(itinerary)
            
            # Create plain text version (simplified)
            text_content = "Your Travel Itinerary\n\n"
            text_content += f"Duration: {len(itinerary.get('days', []))} days\n\n"
            text_content += "Please see the attached PDF for the complete itinerary.\n\n"
            text_content += "Created by Voyage - Your AI Travel Planning Assistant"
            
            # Attach text and HTML parts
            msg_alternative = MIMEMultipart('alternative')
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg_alternative.attach(part1)
            msg_alternative.attach(part2)
            msg.attach(msg_alternative)
            
            # Attach PDF
            pdf_part = MIMEBase('application', 'pdf')
            pdf_part.set_payload(pdf_buffer.read())
            encoders.encode_base64(pdf_part)
            pdf_part.add_header(
                'Content-Disposition',
                f'attachment; filename=itinerary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            )
            msg.attach(pdf_part)
            
            # Send email
            print(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            print(f"Sender: {self.sender_email}")
            print(f"Receiver: {', '.join(recipient_emails)}")
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=15) as server:
                    print("SMTP connection established")
                    server.starttls()
                    print("TLS started")
                    print("Attempting login...")
                    server.login(self.sender_email, self.sender_password)
                    print("Login successful")
                    print("Sending message...")
                    server.send_message(msg)
                    print("Message sent")
            except smtplib.SMTPAuthenticationError as auth_err:
                print(f"Authentication error: {auth_err}")
                raise
            except smtplib.SMTPException as smtp_err:
                print(f"SMTP error: {smtp_err}")
                raise
            
            print(f"Email sent successfully to: {', '.join(recipient_emails)}")
            
            return {
                "success": True,
                "message": f"Itinerary PDF sent successfully to {len(recipient_emails)} recipient(s)",
                "recipients": recipient_emails
            }
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = (
                "Email authentication failed. For Gmail: use an App Password "
                "(Google Account → Security → App passwords), not your regular password. "
                "Set SENDER_PASSWORD in the backend .env file."
            )
            print(f"ERROR: {error_msg} ({e})")
            return {
                "success": False,
                "message": error_msg,
                "error": "authentication_failed"
            }
        except (OSError, ConnectionError) as e:
            error_msg = f"Could not connect to email server ({self.smtp_server}:{self.smtp_port}). Check network or try again later."
            print(f"ERROR: {error_msg} ({e})")
            return {
                "success": False,
                "message": error_msg,
                "error": "connection_error"
            }
        except smtplib.SMTPException as e:
            error_msg = f"Email server error: {str(e)}"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "message": error_msg,
                "error": "smtp_error"
            }
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": error_msg,
                "error": "unknown_error"
            }


def get_email_sender() -> EmailSender:
    """Get initialized email sender"""
    return EmailSender()
