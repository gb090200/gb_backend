from flask import Flask, request, render_template_string
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
PDF_PATH = "Power_BI_Course.pdf"

HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>Free Power BI Course</title></head>
<body style='font-family: Arial; text-align: center; margin-top: 100px'>
  <h1>Get the Full Power BI PDF</h1>
  <form method='POST'>
    <input type='email' name='email' placeholder='Enter your email' required style='padding: 10px; width: 300px' /><br><br>
    <input type='submit' value='Get PDF for Free' style='padding: 10px 20px' />
  </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        send_pdf(email)
        return f"<h2>Thank you! The PDF has been sent to {email}</h2>"
    return render_template_string(HTML_FORM)

def send_pdf(recipient_email):
    EMAIL_ADDRESS = os.environ.get("EMAIL")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = 'Your Free Power BI Course PDF'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg.set_content("Thank you for signing up. Find your Power BI course attached.")

    with open(PDF_PATH, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='Power_BI_Course.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
