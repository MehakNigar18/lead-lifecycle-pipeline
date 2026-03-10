
# Azure Function entry point for the Lead Lifecycle Transformation Pipeline.

# Responsibilities:
# Receive HTTP trigger from Azure / ADF
# Call pipeline runner
#  Handle logging and error reporting

# Business logic is handled in:

import azure.functions as func

from app.python.pipeline_runner import main as run_pipeline
from utils.logger import get_logger


logger = get_logger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="run_lead_pipeline", methods=["GET", "POST"])
def run_lead_pipeline(req: func.HttpRequest) -> func.HttpResponse:
    
   # HTTP trigger for executing the Lead Lifecycle pipeline.
    

    logger.info("Azure Function trigger received for Lead Lifecycle pipeline")

    try:
        # Execute pipeline
        run_pipeline()

        logger.info("Lead lifecycle pipeline executed successfully")

        return func.HttpResponse(
            "Lead lifecycle pipeline executed successfully",
            status_code=200
        )

    except Exception as error:

        logger.exception("Lead lifecycle pipeline execution failed")

        return func.HttpResponse(
            f"Pipeline execution failed: {str(error)}",
            status_code=500
        )