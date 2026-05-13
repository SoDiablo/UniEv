# services/email_service.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
import string

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "noreply@uniev.com")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")


def generate_verification_code(length=6):
    """Generate a random 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=length))


async def send_email(to: str, subject: str, body: str):
    """Send email asynchronously. Errors are logged but do not crash the app."""
    try:
        msg = MIMEMultipart('alternative')
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to
        
        # Create HTML part
        html_part = MIMEText(body, "html", "utf-8")
        msg.attach(html_part)
        
        await aiosmtplib.send(
            msg, 
            hostname=SMTP_HOST, 
            port=SMTP_PORT,
            username=SMTP_USER, 
            password=SMTP_PASSWORD,
            start_tls=True
        )
        print(f"✅ Email sent to {to}")
        return True
    except Exception as e:
        print(f"❌ Email send failed to {to}: {e}")
        return False


async def send_verification_code_email(to: str, code: str, name: str = ""):
    """Send verification code email"""
    subject = "UniEv — E-posta Doğrulama Kodu"
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(90deg, #0f766e 0%, #14b8a6 50%, #0f766e 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .code-box {{ background: white; border: 2px dashed #14b8a6; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
            .code {{ font-size: 32px; font-weight: bold; color: #0f766e; letter-spacing: 8px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏠 UniEv</h1>
                <p>Güvenli Öğrenci Konut Platformu</p>
            </div>
            <div class="content">
                <h2>Merhaba{' ' + name if name else ''}!</h2>
                <p>UniEv hesabınızı doğrulamak için aşağıdaki kodu kullanın:</p>
                
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                
                <p>Bu kod <strong>15 dakika</strong> süreyle geçerlidir.</p>
                
                <div class="warning">
                    <strong>⚠️ Güvenlik Uyarısı:</strong><br>
                    Bu kodu kimseyle paylaşmayın. UniEv ekibi asla sizden bu kodu istemez.
                </div>
                
                <p>Eğer bu işlemi siz yapmadıysanız, bu e-postayı görmezden gelebilirsiniz.</p>
            </div>
            <div class="footer">
                <p>© 2026 UniEv - Öğrenciler için güvenli konut platformu</p>
                <p>Bu otomatik bir e-postadır, lütfen yanıtlamayın.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return await send_email(to, subject, body)


async def send_password_reset_code_email(to: str, code: str, name: str = ""):
    """Send password reset code email"""
    subject = "UniEv — Şifre Sıfırlama Kodu"
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(90deg, #0f766e 0%, #14b8a6 50%, #0f766e 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .code-box {{ background: white; border: 2px dashed #dc2626; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
            .code {{ font-size: 32px; font-weight: bold; color: #dc2626; letter-spacing: 8px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            .warning {{ background: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏠 UniEv</h1>
                <p>Şifre Sıfırlama</p>
            </div>
            <div class="content">
                <h2>Merhaba{' ' + name if name else ''}!</h2>
                <p>Şifrenizi sıfırlamak için aşağıdaki kodu kullanın:</p>
                
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                
                <p>Bu kod <strong>15 dakika</strong> süreyle geçerlidir.</p>
                
                <div class="warning">
                    <strong>⚠️ Güvenlik Uyarısı:</strong><br>
                    Eğer şifre sıfırlama talebinde bulunmadıysanız, bu e-postayı görmezden gelin ve hesabınızın güvenliğini kontrol edin.
                </div>
                
                <p>Bu kodu kimseyle paylaşmayın.</p>
            </div>
            <div class="footer">
                <p>© 2026 UniEv - Öğrenciler için güvenli konut platformu</p>
                <p>Bu otomatik bir e-postadır, lütfen yanıtlamayın.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return await send_email(to, subject, body)


# Legacy functions for backward compatibility
async def send_verification_email(to: str, token: str):
    url = f"{APP_URL}/api/auth/verify-email?token={token}"
    await send_email(
        to, "UniEv — E-posta Adresinizi Doğrulayın",
        f"<p>Hesabınızı doğrulamak için <a href='{url}'>bu bağlantıya</a> tıklayın.</p>"
        f"<p>Bu bağlantı 24 saat geçerlidir.</p>"
    )


async def send_reset_email(to: str, token: str, name: str = ""):
    """Send password reset link email"""
    url = f"{APP_URL}/reset-password?token={token}"
    subject = "UniEv — Şifre Sıfırlama"
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(90deg, #0f766e 0%, #14b8a6 50%, #0f766e 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #0f766e; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
            .button:hover {{ background: #0a5a5a; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            .info {{ background: #e7f3ff; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏠 UniEv</h1>
                <p>Şifre Sıfırlama Talebi</p>
            </div>
            <div class="content">
                <h2>Merhaba{' ' + name if name else ''}!</h2>
                <p>Hesabınız için şifre sıfırlama talebinde bulunuldu.</p>
                
                <div class="info">
                    <strong>ℹ️ Şifrenizi sıfırlamak için:</strong><br>
                    Aşağıdaki butona tıklayın ve yeni şifrenizi belirleyin.
                </div>
                
                <div style="text-align: center;">
                    <a href="{url}" class="button">Şifremi Sıfırla</a>
                </div>
                
                <p style="font-size: 12px; color: #666; margin-top: 20px;">
                    Veya bu bağlantıyı tarayıcınıza kopyalayın:<br>
                    <a href="{url}" style="color: #0f766e; word-break: break-all;">{url}</a>
                </p>
                
                <p>Bu bağlantı <strong>1 saat</strong> süreyle geçerlidir.</p>
                
                <div class="warning">
                    <strong>⚠️ Güvenlik Uyarısı:</strong><br>
                    Eğer şifre sıfırlama talebinde bulunmadıysanız, bu e-postayı görmezden gelin ve hesabınızın güvenliğini kontrol edin.
                </div>
                
                <p>Bu bağlantıyı kimseyle paylaşmayın.</p>
            </div>
            <div class="footer">
                <p>© 2026 UniEv - Öğrenciler için güvenli konut platformu</p>
                <p>Bu otomatik bir e-postadır, lütfen yanıtlamayın.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return await send_email(to, subject, body)
