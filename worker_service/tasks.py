from celery_app import celery_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# -----------------------------
# TEST TASK
# -----------------------------
@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def ping():
    return "pong"
# -----------------------------
# TASK 1 — генерация PDF
# -----------------------------
@celery_app.task
def generate_pdf_task(text: str) -> str:
    filename = f"/tmp/generated_{os.getpid()}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "Generated PDF")
    c.drawString(50, 770, text)
    c.save()

    return filename

# -----------------------------
# TASK 2 — отправка email
# -----------------------------
@celery_app.task
def send_email_task(to_email: str, subject: str, body: str) -> str:
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Email sending failed: {e}"