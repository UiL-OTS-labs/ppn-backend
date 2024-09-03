# Generated by Django 2.0.9 on 2018-12-14 10:53

from django.db import migrations
import cdh.core.fields.encrypted_fields


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0004_criteriumanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteriumanswer',
            name='answer',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(verbose_name='criterium_answer:attribute:answer'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='birth_date',
            field=cdh.core.fields.encrypted_fields.EncryptedDateField(blank=True, null=True, verbose_name='participant:attribute:birth_date'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='capable',
            field=cdh.core.fields.encrypted_fields.EncryptedBooleanField(default=True, verbose_name='participant:attribute:capable'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='dyslexic',
            field=cdh.core.fields.encrypted_fields.EncryptedBooleanField(verbose_name='participant:attribute:dyslexic'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=cdh.core.fields.encrypted_fields.EncryptedEmailField(verbose_name='participant:attribute:email'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email_subscription',
            field=cdh.core.fields.encrypted_fields.EncryptedBooleanField(default=False, verbose_name='participant:attribute:email_subscription'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='handedness',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(blank=True, choices=[('left', 'participant:attribute:handedness:lefthanded'), ('right', 'participant:attribute:handedness:righthanded')], null=True, verbose_name='participant:attribute:handedness'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='language',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(verbose_name='participant:attribute:language'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='multilingual',
            field=cdh.core.fields.encrypted_fields.EncryptedNullBooleanField(verbose_name='participant:attribute:multilingual'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='name',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(blank=True, null=True, verbose_name='participant:attribute:name'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='phonenumber',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(blank=True, null=True, verbose_name='participant:attribute:phonenumber'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='sex',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(blank=True, choices=[('M', 'participant:attribute:sex:male'), ('F', 'participant:attribute:sex:female')], null=True, verbose_name='participant:attribute:sex'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='social_status',
            field=cdh.core.fields.encrypted_fields.EncryptedTextField(blank=True, choices=[('student', 'participant:attribute:social_role:student'), ('other', 'participant:attribute:social_role:other')], null=True, verbose_name='participant:attribute:social_status'),
        ),
        migrations.AlterField(
            model_name='secondaryemail',
            name='email',
            field=cdh.core.fields.encrypted_fields.EncryptedEmailField(verbose_name='secondary_email:attribute:email'),
        ),
    ]
