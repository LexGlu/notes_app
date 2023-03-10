# Generated by Django 4.1.7 on 2023-02-27 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0002_note_reminder"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name="note",
            old_name="content",
            new_name="text",
        ),
        migrations.AddField(
            model_name="note",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notes",
                to="notes.category",
            ),
        ),
    ]
