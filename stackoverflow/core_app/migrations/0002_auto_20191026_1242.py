# Generated by Django 2.1.5 on 2019-10-26 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acomment',
            name='a_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anwsers', to='core_app.Answer'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='q_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core_app.Question'),
        ),
        migrations.AlterField(
            model_name='qcomment',
            name='q_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core_app.Question'),
        ),
        migrations.AlterField(
            model_name='upvote',
            name='a_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='core_app.Answer'),
        ),
    ]
