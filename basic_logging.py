import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log"
)

logging.info("Application started")
logging.warning("This is a warning")
logging.error("This is an error")

print("Logs written to app.log")