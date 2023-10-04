import os

variables = {
    "GATEWAY_BASEURL": os.getenv("GATEWAY_BASEURL", "http://localhost:8080"),
}
