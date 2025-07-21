import requests
import os
import smtplib
from email.mime.text import MIMEText

def get_economic_news():
    api_key = os.getenv("MARKETAUX_API_KEY")
    url = f"https://api.marketaux.com/v1/news/all?topics=economy&language=en&api_token={api_key}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("data", [])[:3]
    if not articles:
        return "<p>Aucune actualité économique n’a été trouvée aujourd’hui.</p>"

    html = "<h2 style='color:#2c3e50;'>📰 Economic Brief</h2><ul style='padding-left:0;'>"

    for article in articles:
        title = article.get("title", "Sans titre")
        source = article.get("source", "Source inconnue")
        url_link = article.get("url", "#")

        html += f"""
        <li style='margin-bottom:20px; list-style:none;'>
            <a href="{url_link}" style="font-weight:bold; color:#2980b9; text-decoration:none;">{title}</a><br>
            <small style="color:#7f8c8d;">{source}</small>
        </li>
        """

    html += "</ul>"
    return html

def send_email(subject, html_body):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_TO")

    msg = MIMEText(html_body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email HTML envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    briefing_html = get_economic_news()
    send_email("📰 Résumé économique du jour", briefing_html)


