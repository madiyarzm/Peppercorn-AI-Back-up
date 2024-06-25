from fastapi import APIRouter, HTTPException, Request, status, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import DBManager
from schemas.business_context import BusinessContext
from schemas.user_credentials import UserCredentials, UserCredentialsLogin
import os

login_router = APIRouter()
DB_Manager = DBManager()

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_directory = os.path.join(parent_directory, "templates")
templates = Jinja2Templates(directory=templates_directory)


# Endpoint for main screen
@login_router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


# Endpoints for user registration
@login_router.get("/register")
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@login_router.post("/register")
async def register_user(user: UserCredentials):
    # Check if username already exists
    if DB_Manager.check_user({"username": user.username}):
        raise HTTPException(status_code=400, detail="username already exists")

    # Insert new user into the database
    DB_Manager.insert_user({"username": user.username, "password": user.password})

    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return response


# Endpoints for user login
@login_router.get("/login")
async def login_user(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@login_router.post("/login")
async def login_user(user: UserCredentialsLogin):
    # Check if username exists and password matches
    existing_user = DB_Manager.validate_user(
        {"username": user.username, "password": user.password}
    )
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # If login successful, set user credentials as cookies
    response = RedirectResponse(
        url="/customer-list", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="username", value=user.username)
    response.set_cookie(key="password", value=user.password)

    return response


# Endpoint for customer list
@login_router.get("/customer-list")
async def customer_list(
    request: Request, username: str = Cookie(None), password: str = Cookie(None)
):
    if username is None or password is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    existing_user = DB_Manager.validate_user(
        {"username": username, "password": password}
    )
    if not existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    customers = existing_user.get("customers", [])
    logged_in = existing_user.get("logged-in", False)

    return templates.TemplateResponse(
        "customer_list.html",
        {"request": request, "customer_data": customers, "logged_in": logged_in},
    )


@login_router.post("/customer-list")
async def save_business_context(
    request: Request, context: BusinessContext, username: str = Cookie(None)
):
    if username is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Retrieve the user from the database
    user = DB_Manager.check_user({"username": username})

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Check if the user is already logged in
    if not user.get("logged-in", False):
        # Save the business context
        DB_Manager.save_business_context(username, context.dict())

        # Update the logged-in status
        DB_Manager.clients_collection.update_one(
            {"username": username},
            {"$set": {"logged-in": True}}
        )

    return RedirectResponse(url="/customer-list", status_code=303)
