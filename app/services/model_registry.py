import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "models.json"


class ModelRegistry:

    def __init__(self):
        self.load()
        self.validate_fallbacks()

    def load(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    def save(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=2)

    def get_model(self, model_id: str):
        return self.config["models"].get(model_id)

    def get_all_models(self):
        return self.config["models"]

    def get_active_model(self, role: str):
        model_id = self.config["active_roles"].get(role)

        if not model_id:
            raise ValueError(
                f"No active model configured for role: {role}"
            )

        return model_id

    def set_active_model(self, role: str, model_id: str):

        model = self.get_model(model_id)

        if not model:
            raise ValueError(
                f"Unknown model: {model_id}"
            )

        if model["status"] != "active":
            raise ValueError(
                f"Model {model_id} is not active."
            )

        if model["role"] != role:
            raise ValueError(
                f"Model {model_id} cannot be used for role {role}."
            )

        self.config["active_roles"][role] = model_id
        self.save()

    def get_role_models(self, role: str):

        return {
            model_id: model
            for model_id, model in self.config["models"].items()
            if model["role"] == role
        }

    def validate_fallbacks(self):

        fallback_roles = self.config.get(
            "fallback_roles",
            {}
        )

        for role, models in fallback_roles.items():

            for model_id in models:

                model = self.get_model(model_id)

                if not model:
                    raise ValueError(
                        f"Fallback model not found: {model_id}"
                    )

                if model["status"] != "active":
                    raise ValueError(
                        f"Fallback model {model_id} "
                        f"is not active."
                    )

                if model["role"] != role:
                    raise ValueError(
                        f"Fallback model {model_id} "
                        f"does not belong to role {role}."
                    )