import reflex as rx
import os

# config = rx.Config(app_name="app")

#Configure the Reflex app to use the manager node's IP
config = rx.Config(
    app_name="app",
    api_url=os.getenv("API_URL", "http://0.0.0.0:8000"),  # Point to the manager node's IP
    deploy_url=os.getenv("DEPLOY_URL", "http://0.0.0.0:3000"),
    frontend_port=os.getenv("FRONTEND_PORT", 3000),
    backend_port=os.getenv("BACKEND_PORT", 8000),
    backend_host=os.getenv("BACKEND_HOST", "0.0.0.0")
)