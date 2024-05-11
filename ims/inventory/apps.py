from django.apps import AppConfig

class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        import inventory.signals  # Adjust to use your actual app name
