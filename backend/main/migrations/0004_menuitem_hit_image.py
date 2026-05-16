from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_menuitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='hit',
            field=models.BooleanField(default=False, verbose_name='Хіт продажів'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dishes/', verbose_name='Зображення'),
        ),
    ]
