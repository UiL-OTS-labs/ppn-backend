from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apiauth", "0008_auto_20200402_0951"),
    ]

    # Django is using native UUID fields instead of the old CHAR(32) implementation.
    # If the table is already using UUID, this migration has no effect.
    # Reverse migration is included for completeness sake, but not expected to be used.
    operations = [
        migrations.RunSQL('''ALTER TABLE apiauth_usertoken MODIFY token UUID''',
                          '''ALTER TABLE apiauth_usertoken MODIFY token CHAR(32)''')
    ]
