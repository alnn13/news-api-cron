import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_economic_news():
    api_key = os.getenv("MARKETAUX_API_KEY")
    url = f"https://api.marketaux.com/v1/news/all?topics=economy&language=en&api_token={api_key}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("data", [])[:3]
    if not articles:
        return "<p>Aucune actualité économique trouvée aujourd’hui.</p>"

    html_list = "<h2 style='color:#2c3e50;'>📰 Economic Brief</h2><ul>"

    for article in articles:
        title = article.get("title", "Sans titre")
        source = article.get("source", "Source inconnue")
        date = article.get("published_at", "Date inconnue")[:10]
        url = article.get("url", "#")

        html_list += f"""
        <li style='margin-bottom:15px;'>
            <a href="{url}" style="font-weight:bold; color:#2980b9; text-decoration:none;">{title}</a><br>
            <small>{source} • {date}</small>
        </li>
        """

    html_list += "</ul>"
    return html_list

def send_email(subject, body_html):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_TO")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html_part = MIMEText(body_html, "html", "utf-8")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email HTML envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    briefing = get_economic_news()
    send_email("📰 Résumé économique du jour", briefing)

