from app.services.model_manager import ModelManager


manager = ModelManager()

print("\n=== MODEL MANAGER TEST ===")

print(
    "Cheap/Fast model:",
    manager.get_model_for_role("cheap_fast")
)

print(
    "Powerful model:",
    manager.get_model_for_role("powerful")
)

print("\n=== FALLBACK TEST ===")

print(
    "Cheap/Fast chain:",
    manager.get_models_for_role("cheap_fast")
)

print(
    "Powerful chain:",
    manager.get_models_for_role("powerful")
)