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
        return "Aucune actualité économique n’a été trouvée aujourd’hui."

    news_list = []
    for i, article in enumerate(articles, 1):
        title = article.get("title", "Sans titre")
        source = article.get("source", "Source inconnue")
        url = article.get("url", "#")
        news_list.append(f"{i}. {title} ({source})\n{url}")

    return "\n\n".join(news_list)

def send_email(subject, body):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_TO")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Debug pour t’assurer que les variables sont bien prises en compte
    print(f"EMAIL DEBUG → FROM: {sender}, TO: {recipient}, PASS: {password[:4]}***")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    briefing = get_economic_news()
    send_email("📰 Résumé économique du jour", briefing)
