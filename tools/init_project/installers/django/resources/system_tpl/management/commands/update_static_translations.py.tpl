import json
from django.conf import settings
from django.core.management.base import BaseCommand
from features.system.models import StaticTranslation

class Command(BaseCommand):
    help = "Update Static Translations from JSON fixture"

    def handle(self, *args, **options):
        fixture_path = settings.BASE_DIR / "features" / "system" / "fixtures" / "static_translations.json"

        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"Fixture not found: {fixture_path}"))
            return

        with open(fixture_path, encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for item in data:
            fields = item.get("fields", item)
            key = fields.get("key")
            if not key: continue

            obj, created = StaticTranslation.objects.update_or_create(
                key=key,
                defaults={
                    "text": fields.get("text", ""),
                    "description": fields.get("description", "")
                }
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  [{verb}] {key}")
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Processed {count} translations"))
