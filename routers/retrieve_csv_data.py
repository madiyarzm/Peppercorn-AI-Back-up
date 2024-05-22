import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import DBManager

retrieve_data_router = APIRouter()
DB_Manager = DBManager()

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_directory = os.path.join(parent_directory, "templates")
templates = Jinja2Templates(directory=templates_directory)


@retrieve_data_router.get("/retrieve-csv-data")
async def retrieve_uploaded_data(request: Request):
    # Retrieve the current user's username from the cookies
    username = request.cookies.get("username")

    # Query the database to retrieve uploaded data for the current user
    uploaded_data = DB_Manager.retrieve_uploaded_data(username)

    # Render an HTML page with the retrieved data
    return templates.TemplateResponse(
        "uploaded_data.html", {"request": request, "uploaded_data": uploaded_data}
    )


@retrieve_data_router.post("/delete-uploaded-data/{upload_id}")
async def delete_uploaded_data(request: Request, upload_id: str):
    # Delete the uploaded data with the specified upload_id
    DB_Manager.delete_uploaded_data(upload_id)

    # Redirect the user to the uploaded data page
    return RedirectResponse(url="/retrieve-csv-data", status_code=303)


@retrieve_data_router.get("/show-data-table/{upload_id}")
async def show_data_table(request: Request, upload_id: str):
    # Retrieve the data from the database based on the upload_id
    data = DB_Manager.retrieve_data_as_table(upload_id)

    # Render HTML page with the retrieved data
    return templates.TemplateResponse(
        "data_table.html", {"request": request, "data": data}
    )


@retrieve_data_router.post("/use-data/{upload_id}")
async def use_data(request: Request, upload_id: str):
    # Retrieve the necessary data from the database
    customer_data = DB_Manager.retrieve_data_as_table(upload_id)

    # Convert the customer data into a list of dictionaries
    customers = [
        {"name": row["name"], "email": row["email"], "income": row["income"]}
        for row in customer_data
    ]

    # Get the username
    username = request.cookies.get("username")

    # Update the client's customers list
    DB_Manager.update_clients_add_customers(username, customers)

    client = DB_Manager.check_user(username)

    # Redirect the user to the customer list page with client data in query parameters
    url = f"/customer-list?client={client}"
    return RedirectResponse(url=url, status_code=303)
