from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# -------- GOOGLE SHEETS --------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open("Leads VM Store").sheet1


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if "_embedded" in data and "leads" in data["_embedded"]:

        for lead in data["_embedded"]["leads"]:

            lead_id = lead.get("id")
            nome = lead.get("name")
            data_criacao = datetime.fromtimestamp(
                lead.get("created_at")
            ).strftime("%d/%m/%Y")

            vendedor = lead.get("responsible_user_id")
            status = lead.get("status_id")

            telefone = ""
            canal = ""

            sheet.append_row([
                lead_id,
                nome,
                telefone,
                canal,
                data_criacao,
                vendedor,
                status
            ])

    return "ok", 200


if __name__ == "__main__":
    app.run()
