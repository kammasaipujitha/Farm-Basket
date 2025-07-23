import os
import django
import io
from django.core.management import call_command

# Set the settings module (based on your structure)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farm_basket_project.settings")


# Setup Django
django.setup()

# Export to JSON
try:
    print("Exporting data...")
    with io.open("data.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", stdout=f)
    print("Data export successful.")
except Exception as e:
    print("Error during export:", e)
