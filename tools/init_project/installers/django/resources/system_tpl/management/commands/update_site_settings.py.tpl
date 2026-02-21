import json
from django.conf import settings
from django.core.management.base import BaseCommand
from features.system.models import SiteSettings

class Command(BaseCommand):
    help = "Update Site Settings from JSON fixture (features/system/fixtures/site_settings.json)"

    def handle(self, *args, **options):
        fixture_path = settings.BASE_DIR / "features" / "system" / "fixtures" / "site_settings.json"

        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"Fixture not found: {fixture_path}"))
            return

        try:
            with open(fixture_path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON: {e}"))
            return

        # Simple fixture format check (Django list of objects)
        if isinstance(data, list) and len(data) > 0:
            fields = data[0].get("fields", {})
        else:
            fields = data # assume dict

        site_settings = SiteSettings.load()
        updated_fields = 0

        for field_name, new_value in fields.items():
            if hasattr(site_settings, field_name):
                current_value = getattr(site_settings, field_name)
                if str(current_value) != str(new_value):
                    setattr(site_settings, field_name, new_value)
                    updated_fields += 1
                    self.stdout.write(self.style.SUCCESS(f"  [UPDATE] {field_name}: {new_value}"))

        if updated_fields:
            site_settings.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Site Settings updated ({updated_fields} fields changed)"))
        else:
            self.stdout.write(self.style.SUCCESS("✓ All fields up to date"))
