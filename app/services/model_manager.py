import os

from dotenv import load_dotenv
from google import genai

from app.services.model_registry import ModelRegistry


load_dotenv()


class ModelManager:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)
        self.registry = ModelRegistry()

        self.simulate_failure = (
            os.getenv(
                "SIMULATE_MODEL_FAILURE",
                "false"
            ).lower() == "true"
        )

    def get_model_for_role(self, role: str) -> str:

        model_id = self.registry.get_active_model(role)

        model = self.registry.get_model(model_id)

        if not model:
            raise ValueError(
                f"Model configuration not found: {model_id}"
            )

        if model["status"] != "active":
            raise ValueError(
                f"Configured model is not active: {model_id}"
            )

        return model_id

    def get_fallback_models(self, role: str) -> list[str]:

        return self.registry.config.get(
            "fallback_roles",
            {}
        ).get(role, [])

    def get_models_for_role(self, role: str) -> list[str]:

        primary_model = self.get_model_for_role(role)

        fallback_models = self.get_fallback_models(role)

        return [
            primary_model,
            *[
                model
                for model in fallback_models
                if model != primary_model
            ]
        ]

    def _is_fallback_error(self, error: Exception) -> bool:

        error_text = str(error).lower()

        fallback_keywords = [
            "429",
            "rate limit",
            "resource exhausted",
            "503",
            "service unavailable",
            "temporarily unavailable",
            "timeout",
            "timed out",
            "overloaded",
            "unavailable",
        ]

        return any(
            keyword in error_text
            for keyword in fallback_keywords
        )

    def generate(self, role: str, prompt: str) -> str:

        models_to_try = self.get_models_for_role(role)

        last_error = None

        for index, model_id in enumerate(models_to_try):

            try:

                print(f"Trying model: {model_id}")

                if (
                    self.simulate_failure
                    and index == 0
                ):
                    raise RuntimeError(
                        "Simulated primary model failure."
                    )

                response = self.client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                )

                print(f"Model succeeded: {model_id}")

                return response.text

            except Exception as error:

                print(f"Model failed: {model_id}")
                print(f"Error: {error}")

                last_error = error

                is_last_model = (
                    index == len(models_to_try) - 1
                )

                if is_last_model:
                    break

                if not self._is_fallback_error(error):
                    raise RuntimeError(
                        f"Model {model_id} failed and "
                        f"the error is not considered "
                        f"fallback-safe."
                    ) from error

        raise RuntimeError(
            f"All configured models failed for "
            f"role '{role}'."
        ) from last_error

    def check_model_availability(self, model_id: str) -> dict:

        model = self.registry.get_model(model_id)

        if not model:
            return {
                "model": model_id,
                "available": False,
                "message": "Model is not registered."
            }

        if model["status"] != "active":
            return {
                "model": model_id,
                "available": False,
                "message": (
                    f"Model status is {model['status']}."
                )
            }

        return {
            "model": model_id,
            "available": True,
            "message": "Model is configured as active."
        }