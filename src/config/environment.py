import os

variables = {
    "GATEWAY_BASEURL": os.getenv("GATEWAY_BASEURL", "http://localhost:8080"),
    "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "http://localhost:5173"),
}
