# Generated by Django 3.0.5 on 2020-04-03 11:05

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('mobile', models.CharField(blank=True, max_length=20, verbose_name='mobile')),
                ('access_key', models.CharField(blank=True, max_length=255, verbose_name='access key')),
                ('access_secret', models.CharField(blank=True, max_length=255, verbose_name='access secret')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(help_text='duration in days.', verbose_name='duration')),
                ('price', models.DecimalField(decimal_places=2, help_text='precision 2', max_digits=10, verbose_name='price')),
                ('currency', models.CharField(choices=[('USD', 'USD')], max_length=3, verbose_name='currency')),
                ('type', models.CharField(choices=[('Monthly', 'Monthly'), ('Annual', 'Annual')], max_length=10, verbose_name='License Type')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='updated on')),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('short_description', models.CharField(max_length=70, verbose_name='short description')),
                ('version', models.CharField(max_length=10, verbose_name='version')),
                ('documentation_link', models.URLField(blank=True, null=True, verbose_name='documentation link')),
                ('download_link', models.URLField(blank=True, null=True, verbose_name='download link')),
                ('video_link', models.URLField(blank=True, help_text='Provide the link of a playlist or single video.', verbose_name='video link')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='updated on')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='softwares', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50, verbose_name='reference')),
                ('license_key', models.CharField(blank=True, max_length=50, verbose_name='License Key')),
                ('is_used', models.BooleanField(default=False, verbose_name='is used')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('is_verified', models.BooleanField(default=False, help_text='indicates if payment is verified.', verbose_name='is verified')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='amount')),
                ('currency', models.CharField(choices=[('USD', 'USD')], max_length=3)),
                ('name', models.CharField(max_length=100, verbose_name='client name')),
                ('email', models.EmailField(max_length=254, verbose_name='client email')),
                ('address', models.CharField(max_length=255, verbose_name='client address')),
                ('country', models.CharField(max_length=2, verbose_name='client country')),
                ('mobile', models.CharField(blank=True, max_length=20, verbose_name='mobile')),
                ('payment_response', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='updated on')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='activation.License')),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='activation.Software')),
            ],
        ),
        migrations.AddField(
            model_name='license',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='activation.Software'),
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Maximum Characters 50', max_length=50, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('index', models.IntegerField(help_text='indicates the order of the software descriptions', verbose_name='index')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='updated on')),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptions', to='activation.Software')),
            ],
            options={
                'ordering': ['index', 'id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='license',
            unique_together={('software', 'type')},
        ),
    ]
