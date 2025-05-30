# Generated by Django 5.2.1 on 2025-05-29 15:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom complet ou raison sociale', max_length=100, verbose_name='Nom du fournisseur')),
                ('type', models.CharField(help_text="Catégorie principale d'activité", max_length=50, verbose_name='Type de fournisseur')),
                ('adresse', models.TextField(help_text='Adresse postale avec ville et pays', verbose_name='Adresse complète')),
                ('email', models.EmailField(help_text='Adresse postale avec ville et pays', max_length=254, verbose_name='Adresse complète')),
                ('telephone', models.CharField(help_text='Numéro avec indicatif (ex: +221 XXX XX XX)', max_length=20, verbose_name='Téléphone')),
                ('numero_rc', models.CharField(help_text="Numéro d'inscription au registre du commerce", max_length=50, verbose_name='Numéro RC')),
                ('ninea', models.CharField(help_text="Numéro d'Identification national des Entreprises et Associations", max_length=50, unique=True, verbose_name='NINEA')),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('Comptable', 'Comptable'), ('Directeur', 'Directeur'), ('CSA', 'CSA')], default='Comptable', max_length=20)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercice', models.CharField(max_length=9, unique=True, verbose_name='Exercice budgétaire')),
                ('montant_total', models.FloatField(verbose_name='Montant total alloué')),
                ('montant_disponible', models.FloatField(verbose_name='Montant disponible')),
                ('statut', models.CharField(choices=[('en_cours', 'En cours'), ('cloture', 'Clôturé')], default='en_cours', max_length=20, verbose_name='Statut du budget')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('comptable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Comptable responsable')),
            ],
        ),
        migrations.CreateModel(
            name='DemandeDepense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.TextField(help_text='Décrivez en détail la nécessité de cette dépense', verbose_name='Motif de la dépense')),
                ('montant_estime', models.FloatField(help_text='Estimation du coût en francs CFA', verbose_name='Montant estimé (FCFA)')),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('approuvée', 'Approuvée'), ('refusée', 'Refusée')], default='en_attente', max_length=20, verbose_name='Statut de la demande')),
                ('date_demande', models.DateField(auto_now_add=True, verbose_name='Date de la demande')),
                ('date_validation', models.DateField(blank=True, null=True, verbose_name='Date de validation')),
                ('commentaire_directeur', models.TextField(blank=True, help_text='Commentaires éventuels sur la décision', verbose_name='Commentaires du directeur')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes_depense', to=settings.AUTH_USER_MODEL, verbose_name='Demandeur')),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('designation', models.CharField(max_length=100, verbose_name='Désignation')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('prix_unitaire', models.FloatField()),
                ('total', models.FloatField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('rejettee', 'Rejetée')], default='en_attente', max_length=20)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='JournalAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField()),
                ('date_heure', models.DateTimeField(default=django.utils.timezone.now)),
                ('utilisateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LigneBudgetaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=100, verbose_name='Article ou poste budgétaire')),
                ('montant_alloue', models.FloatField(verbose_name='Montant alloué à cette ligne')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='core.budget')),
            ],
        ),
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_planifiee', models.BooleanField(default=False)),
                ('statut_validation', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('rejetee', 'Rejetée')], default='en_attente', max_length=20)),
                ('date_validation', models.DateField(blank=True, null=True)),
                ('date', models.DateField(help_text='Date effective de la dépense', verbose_name="Date d'engagement")),
                ('montant', models.FloatField(help_text='Montant effectivement dépensé', verbose_name='Montant (FCFA)')),
                ('description', models.TextField(help_text='Détails sur la nature de la dépense', verbose_name='Description')),
                ('type_depense', models.CharField(max_length=100, verbose_name='Type de dépense')),
                ('categorie', models.CharField(max_length=50, verbose_name='Catégorie budgétaire')),
                ('justificatif', models.FileField(blank=True, help_text='Document PDF/Image attestant la dépense', null=True, upload_to='justificatifs/depenses/', verbose_name='Pièce justificative')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depenses', to='core.budget', verbose_name='Budget associé')),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depenses', to='core.commande')),
                ('demande', models.ForeignKey(blank=True, help_text='Lien vers la demande préalable (si existante)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.demandedepense', verbose_name='Demande associée')),
                ('supervise_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depenses_supervisees', to=settings.AUTH_USER_MODEL)),
                ('valide_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depenses_validees', to=settings.AUTH_USER_MODEL)),
                ('ligne_budgetaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depenses', to='core.lignebudgetaire')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='ligne_budgetaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='core.lignebudgetaire'),
        ),
        migrations.CreateModel(
            name='RapportFinancier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('pdf', 'PDF'), ('excel', 'Excel')], help_text='Type de fichier généré', max_length=10, verbose_name='Format du rapport')),
                ('periode', models.CharField(help_text="Ex: 'T1 2024', 'Janvier - Mars 2024'", max_length=20, verbose_name='Période couverte')),
                ('nom_fichier', models.CharField(help_text='Nom original du rapport', max_length=255, verbose_name='Nom du fichier')),
                ('fichier', models.FileField(blank=True, help_text='Fichier PDF ou Excel généré', null=True, upload_to='rapports/', verbose_name='Fichier du rapport')),
                ('date_generation', models.DateTimeField(auto_now_add=True, verbose_name='Date de génération')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to='core.budget', verbose_name='Budget associé')),
                ('genere_par', models.ForeignKey(help_text='Responsable de la génération', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Généré par')),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100, verbose_name='Source de la recette')),
                ('type', models.CharField(max_length=50, verbose_name='Type de recette')),
                ('montant', models.FloatField(verbose_name='Montant (FCFA)')),
                ('date', models.DateField(verbose_name='Date de la recette')),
                ('justificatif', models.FileField(blank=True, null=True, upload_to='justificatifs/recettes/', verbose_name='Justificatif numérique')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recettes', to='core.budget', verbose_name='Budget associé')),
            ],
        ),
    ]
