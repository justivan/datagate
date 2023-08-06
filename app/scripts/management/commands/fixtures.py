from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.apps import apps

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parents[3]
FIXTURES_DIR = BASE_DIR.parent / "fixtures"

app_labels = [label for label in settings.LOCAL_APPS]


class Command(BaseCommand):
    help = "Dump and load data"

    def add_arguments(self, parser):
        parser.add_argument("action", choices=["dump", "load"], help='Specify the action to perform: "dump" or "load"')

    def handle(self, *args, **options):
        action = options["action"]

        if action == "dump":
            self.dump()
        elif action == "load":
            self.load()

    # Run dumpdata for each model in each app and save output to separate files
    def dump(self):
        # Create the "fixtures" directory if it doesn't exist
        if not os.path.exists(FIXTURES_DIR):
            os.makedirs(FIXTURES_DIR)

        for app_label in app_labels:
            app_models = apps.get_app_config(app_label).get_models()

            APP_DIR = FIXTURES_DIR / app_label
            # Create the "app" directory if it doesn't exist
            if not APP_DIR.exists():
                os.makedirs(APP_DIR)

            for model in app_models:
                model_name = model._meta.model_name
                output_file = APP_DIR / f"{model_name}.json"

                call_command("dumpdata", f"{app_label}.{model_name}", output=output_file)

    def load(self):
        try:
            if not os.path.exists(FIXTURES_DIR):
                raise FileNotFoundError("Fixtures directory does not exist")
            fixtures = [
                "accounts/user",
                "definitions/country",
                "definitions/region",
                "definitions/area",
                "definitions/mealplan",
                # "clients/operatorgroup",
                # "clients/operator",
                "accommodation/tagtype",
                "accommodation/tag",
                "accommodation/salescontact",
                "accommodation/purchasemanager",
                "accommodation/hotelstatus",
                "accommodation/hotelchain",
                "accommodation/hotelcategory",
                "accommodation/hotel",
                # "accommodation/hotelmapping",
            ]

            call_command("loaddata", *fixtures)
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")

    def generate_fixture_names(self, names, prefix=""):
        return [prefix + name for name in names]
