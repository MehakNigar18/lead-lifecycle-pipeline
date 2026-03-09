import azure.functions as func
import logging
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "app/python"))

from main import main as run_pipeline

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="run_lead_pipeline")
def run_lead_pipeline(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Lead lifecycle pipeline triggered")

    try:
        run_pipeline()

        return func.HttpResponse(
            "Lead lifecycle pipeline executed successfully",
            status_code=200
        )

    except Exception as e:
        logging.error(str(e))

        return func.HttpResponse(
            "Pipeline execution failed",
            status_code=500
        )