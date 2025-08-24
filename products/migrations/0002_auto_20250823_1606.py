# products/migrations/0002_auto_seed_units.py

from django.db import migrations

def seed_units(apps, schema_editor):
    Unit = apps.get_model('products', 'Unit')  # model Đơn vị tính :contentReference[oaicite:0]{index=0}
    default_units = [
        ("Cái", "cái"),
        ("Hộp", "hộp"),
        ("Kilogram", "kg"),
    ]
    existing = set(Unit.objects.values_list('name', flat=True))
    to_create = [
        Unit(name=name, symbol=symbol)
        for name, symbol in default_units
        if name not in existing
    ]
    if to_create:
        Unit.objects.bulk_create(to_create)

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_units),
    ]
