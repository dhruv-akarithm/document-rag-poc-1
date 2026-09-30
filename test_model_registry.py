from app.services.model_registry import ModelRegistry


registry = ModelRegistry()

print("\n=== ALL MODELS ===")

for model_id, model in registry.get_all_models().items():
    print(model_id)
    print("  Name:", model["display_name"])
    print("  Role:", model["role"])
    print("  Status:", model["status"])


print("\n=== ACTIVE MODELS ===")

print(
    "Cheap/Fast:",
    registry.get_active_model("cheap_fast")
)

print(
    "Powerful:",
    registry.get_active_model("powerful")
)