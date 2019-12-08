# Generated by Django 2.2.4 on 2019-12-06 16:40

import analizer.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campagne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grume_data', djongo.models.fields.EmbeddedModelField(model_container=analizer.models.GrumeData, null=True)),
                ('info_sciage', djongo.models.fields.ArrayModelField(model_container=analizer.models.DataInfoSciage)),
            ],
        ),
        migrations.CreateModel(
            name='InfoConfigurationLigne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longueur_de_campagne_mm', models.PositiveIntegerField()),
                ('epaisseur_principale_multilame', models.PositiveIntegerField()),
                ('hauteur_produits_multilame', models.PositiveIntegerField()),
                ('epaisseur_secondaire_multilame', models.PositiveIntegerField()),
                ('nombre_produits_secondaires', models.PositiveIntegerField()),
                ('numero_configuration', models.PositiveIntegerField()),
                ('largeur_deligneuse1', models.PositiveIntegerField()),
                ('largeur_deligneuse2', models.PositiveIntegerField()),
                ('largeur_deligneuse3', models.PositiveIntegerField()),
                ('largeur_deligneuse4', models.PositiveIntegerField()),
                ('largeur_deligneuse5', models.PositiveIntegerField()),
                ('hauteur_deligneuse', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InfosTempsDeCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure_grume_prete_pour_ejection', models.DateTimeField()),
                ('heure_table_analyse_en_attente_chargement', models.DateTimeField()),
                ('heure_ejection_sur_quai_analyse', models.DateTimeField()),
                ('heure_debut_griffage_analyse', models.DateTimeField()),
                ('heure_fin_griffage_analyse', models.DateTimeField()),
                ('heure_debut_rotation_analyse', models.DateTimeField()),
                ('heure_fin_rotation_analyse', models.DateTimeField()),
                ('heure_fin_optimisation', models.DateTimeField()),
                ('heure_debut_griffage_analyse2', models.DateTimeField()),
                ('heure_fin_griffage_analyse2', models.DateTimeField()),
                ('heure_debut_rotation_analyse2', models.DateTimeField()),
                ('heure_fin_rotation_analyse2', models.DateTimeField()),
                ('heure_fin_optimisation2', models.DateTimeField()),
                ('heure_fin_rotation_optimale', models.DateTimeField()),
                ('heure_fin_de_griffage_analyse', models.DateTimeField()),
                ('depart_transfert_table_vers_intermediaire_portique', models.DateTimeField()),
                ('heure_table_position_intermediaire', models.DateTimeField()),
                ('heure_chariot_sciage_position_attente_table', models.DateTimeField()),
                ('depart_transfert_table_intermediaire_vers_sciage', models.DateTimeField()),
                ('heure_depart_griffage_sciage', models.DateTimeField()),
                ('heure_fin_griffage_sciage', models.DateTimeField()),
                ('heure_table_en_position_chargement', models.DateTimeField()),
                ('reserve1', models.DateTimeField()),
                ('reserve2', models.DateTimeField()),
                ('reserve3', models.DateTimeField()),
                ('reserve4', models.DateTimeField()),
                ('reserve5', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.CharField(max_length=50, null=True)),
                ('y', models.IntegerField()),
            ],
        ),
    ]
