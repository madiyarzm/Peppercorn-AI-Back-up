import os
from fastapi import APIRouter, Cookie, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from database import DBManager
from schemas.email_content import EmailContent
import boto3

load_dotenv()

sending_emails_router = APIRouter()
DB_Manager = DBManager()

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_directory = os.path.join(parent_directory, "templates")
templates = Jinja2Templates(directory=templates_directory)


ses_client = boto3.client(
    service_name="ses",
    region_name=os.environ.get("AWS_REGION"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


@sending_emails_router.get("/send-email")
async def send_email(request: Request):
    return templates.TemplateResponse("send_email.html", {"request": request})


async def get_email_addresses_from_db(username: str = Cookie(None)):
    # Fetch the client record from the database based on the username
    client = DB_Manager.check_user({"username": username})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    # Extract the list of email addresses from the customers key of the client record
    email_addresses = [customer["email"] for customer in client.get("customers", [])]
    return email_addresses


@sending_emails_router.post("/send-email")
async def send_email(
    username: str = Cookie(None),
    subject: str = Form(...),
    body: str = Form(...),
):
    try:
        email_addresses = await get_email_addresses_from_db(username)
        email_content = EmailContent(
            email_addresses=email_addresses, subject=subject, body=body
        )

        response = ses_client.send_email(
            Source="momedhat2005@gmail.com",
            Destination={"ToAddresses": email_addresses},
            Message={
                "Subject": {"Data": email_content.subject},
                "Body": {"Text": {"Data": email_content.body}},
            },
        )

        return {"message": "Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@sending_emails_router.post("/verify-email")
async def verify_email_identity(username: str = Cookie(None)):
    email_addresses = await get_email_addresses_from_db(username)
    response = ses_client.verify_email_identity(EmailAddress="momedhat2005@gmail.com")
    print("Verify Response: ", response)
    # Redirect the user to "/send-email"
    return RedirectResponse(url="/send-email")
