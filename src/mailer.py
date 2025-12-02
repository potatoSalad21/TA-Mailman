import os.path
import json
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

SCOPES = ["https://mail.google.com/"]
UNI_MAIL_PREF = "@freeuni.edu.ge"

TA_MAIL = "dzira24@freeuni.edu.ge"
SUBJECT = "Programming Methodology Assignment"


class GradeMailer:
    _creds = None
    _grades = None

    def __init__(self):
        pass

    def readGrades(self, path):
        with open(path, 'r',) as data:
            self._grades = json.load(data)

    def mailGrades(self):
        for prefix in self._grades:
            print(prefix, ": ", self._grades[prefix])
            try:
                service = build("gmail", "v1", credentials=self._creds)
                msg = EmailMessage()
                msg["To"] = prefix + UNI_MAIL_PREF
                msg["From"] = TA_MAIL
                msg["Subject"] = SUBJECT
                msg.set_content(self._grades[prefix])

                encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
                send_msg = (
                    service.users()
                        .messages()
                        .send(userId="me", body={"raw": encoded_msg})
                        .execute()
                )

                print(send_msg)

            except HttpError as err:
                print(f"Http error: {err}")

    def auth(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self._creds = creds
