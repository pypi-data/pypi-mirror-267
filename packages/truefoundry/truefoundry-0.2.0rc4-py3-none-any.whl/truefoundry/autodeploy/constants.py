import os

DEBUG = os.getenv("AUTODEPLOY_DEBUG", "")

AUTODEPLOY_TFY_BASE_URL = os.getenv(
    "AUTODEPLOY_TFY_BASE_URL", "https://app.devtest.truefoundry.tech"
).strip("/")
AUTODEPLOY_OPENAI_BASE_URL = os.environ.get("AUTODEPLOY_OPENAI_BASE_URL")
AUTODEPLOY_OPENAI_API_KEY = os.environ.get("AUTODEPLOY_OPENAI_API_KEY")
AUTODEPLOY_MODEL_NAME = os.environ.get(
    "AUTODEPLOY_MODEL_NAME", "auto-deploy-openai/gpt-4-turbo-2024-04-09"
)
