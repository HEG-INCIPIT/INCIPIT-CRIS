from django.urls import path

from . import views, views_person, views_article, views_project, views_dataset, views_institution, views_funder, views_visualizer, views_search

urlpatterns = [
    # Index page
    path('', views.index, name='index'),

    # Search POST
    path('search', views_search.search, name='search'),

    # Import data
    path('import-data/', views.import_data, name='import_data'),

    # Manage data
    path('manage-data/', views.manage_data, name='manage_data'),
    path('backup-triplestore/', views.backup_triplestore, name='backup_triplestore'),
    path('download-file/', views.download_file_superuser, name='download_file_superuser'),
    path('populate-triplestore/', views.populate_triplestore, name='populate_triplestore'),
    path('delete-data/', views.delete_data, name='delete_data'),

    # Link ORCID
    path('orcid/', views_person.orcid, name='orcid'),
    path('delete-orcid/<path:pid>', views_person.delete_orcid, name='delete_orcid'),

    # Persons urls
    path('persons/', views_person.person_results, name='person_results'),
    path('persons/filter/<int:page>/<str:filter_category>/', views_person.person_results, name='person_results'),
    path('persons/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_person.person_results, name='person_results'),
    path('persons/edition/profil/add-article/<path:pid>', views_person.person_article_addition, name='person_article_addition'),
    path('persons/edition/profil/delete-article/<path:pid>', views_person.person_article_deletion, name='person_article_deletion'),
    path('persons/edition/profil/add-project/<path:pid>', views_person.person_project_addition, name='person_project_addition'),
    path('persons/edition/profil/delete-project/<path:pid>', views_person.person_project_deletion, name='person_project_deletion'),
    path('persons/edition/profil/add-dataset/<path:pid>', views_person.person_datasets_addition, name='person_datasets_addition'),
    path('persons/edition/profil/delete-dataset/<path:pid>', views_person.person_datasets_deletion, name='person_datasets_deletion'),
    path('persons/edition/profil/add-work/<path:pid>', views_person.person_work_addition, name='person_work_addition'),
    path('persons/edition/profil/delete-work/<path:pid>', views_person.person_work_deletion, name='person_work_deletion'),
    path('persons/edition/profil/add-affiliation/<path:pid>', views_person.person_affiliation_addition, name='person_affiliation_addition'),
    path('persons/edition/profil/delete-affiliation/<path:pid>', views_person.person_affiliation_deletion, name='person_affiliation_deletion'),
    path('persons/edition/profil/add-title/<path:pid>', views_person.person_title_addition, name='person_title_addition'),
    path('persons/edition/profil/delete-title/<path:pid>', views_person.person_title_deletion, name='person_title_deletion'),
    path('persons/edition/profil/add-job-title/<path:pid>', views_person.person_job_title_addition, name='person_job_title_addition'),
    path('persons/edition/profil/delete-job-title/<path:pid>', views_person.person_job_title_deletion, name='person_job_title_deletion'),
    path('persons/edition/profil/add-linkedin-profile/<path:pid>', views_person.person_linkedin_addition, name='person_linkedin_addition'),
    path('persons/edition/profil/delete-linkedin-profile/<path:pid>', views_person.person_linkedin_deletion, name='person_linkedin_deletion'),
    path('persons/edition/profil/<str:field_to_modify>/<path:pid>', views_person.person_field_edition, name='person_field_edition'),
    path('persons/edition/<path:pid>', views_person.person_edition, name='person_edition_display'),
    path('persons/<path:pid>', views_person.person_profile, name='person_profile'),

    # Articles urls
    path('articles/', views_article.article_results, name='article_results'),
    path('articles/filter/<int:page>/<str:filter_category>/', views_article.article_results, name='article_results'),
    path('articles/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_article.article_results, name='article_results'),
    path('articles/creation/', views_article.article_creation, name='article_creation'),
    path('articles/edition/field/add-author/<path:pid>', views_article.article_author_addition, name='article_author_addition'),
    path('articles/edition/field/delete-author/<path:pid>', views_article.article_author_deletion, name='article_author_deletion'),
    path('articles/edition/field/add-project/<path:pid>', views_article.article_project_addition, name='article_project_addition'),
    path('articles/edition/field/delete-project/<path:pid>', views_article.article_project_deletion, name='article_project_deletion'),
    path('articles/edition/field/add-dataset/<path:pid>', views_article.article_dataset_addition, name='article_dataset_addition'),
    path('articles/edition/field/delete-dataset/<path:pid>', views_article.article_dataset_deletion, name='article_dataset_deletion'),
    path('articles/edition/field/add-institution/<path:pid>', views_article.article_institution_addition, name='article_institution_addition'),
    path('articles/edition/field/delete-institution/<path:pid>', views_article.article_institution_deletion, name='article_institution_deletion'),
    path('articles/edition/field/add-doi/<path:pid>', views_article.article_doi_addition, name='article_doi_addition'),
    path('articles/edition/field/delete-doi/<path:pid>', views_article.article_doi_deletion, name='article_doi_deletion'),
    path('articles/edition/delete-article/<path:pid>', views_article.article_deletion, name='article_deletion'),
    path('articles/edition/field/<str:field_to_modify>/<path:pid>', views_article.article_field_edition, name='article_field_edition'),
    path('articles/edition/<path:pid>', views_article.article_edition, name='article_edition'),
    path('articles/<path:pid>', views_article.article_profile, name='article_profile'),

    # Projects urls
    path('projects/', views_project.project_results, name='project_results'),
    path('projects/filter/<int:page>/<str:filter_category>/', views_project.project_results, name='project_results'),
    path('projects/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_project.project_results, name='project_results'),
    path('projects/creation/', views_project.project_creation, name='project_creation'),
    path('projects/edition/field/add-member/<path:pid>', views_project.project_member_addition, name='project_member_addition'),
    path('projects/edition/field/delete-member/<path:pid>', views_project.project_member_deletion, name='project_member_deletion'),
    path('projects/edition/delete-project/<path:pid>', views_project.project_deletion, name='project_deletion'),
    path('projects/edition/field/add-article/<path:pid>', views_project.project_article_addition, name='project_article_addition'),
    path('projects/edition/field/delete-article/<path:pid>', views_project.project_article_deletion, name='project_article_deletion'),
    path('projects/edition/field/add-dataset/<path:pid>', views_project.project_dataset_addition, name='project_dataset_addition'),
    path('projects/edition/field/delete-dataset/<path:pid>', views_project.project_dataset_deletion, name='project_dataset_deletion'),
    path('projects/edition/field/add-institution/<path:pid>', views_project.project_institution_addition, name='project_institution_addition'),
    path('projects/edition/field/delete-institution/<path:pid>', views_project.project_institution_deletion, name='project_institution_deletion'),
    path('projects/edition/field/add-funder/<path:pid>', views_project.project_funder_addition, name='project_funder_addition'),
    path('projects/edition/field/delete-funder/<path:pid>', views_project.project_funder_deletion, name='project_funder_deletion'),
    path('projects/edition/field/<str:field_to_modify>/<path:pid>', views_project.project_field_edition, name='project_field_edition'),
    path('projects/edition/<path:pid>', views_project.project_edition, name='project_edition'),
    path('projects/<path:pid>', views_project.project_profile, name='project_profile'),

    # Datasets urls
    path('datasets/', views_dataset.dataset_results, name='dataset_results'),
    path('datasets/filter/<int:page>/<str:filter_category>/', views_dataset.dataset_results, name='dataset_results'),
    path('datasets/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_dataset.dataset_results, name='dataset_results'),
    path('datasets/creation/', views_dataset.dataset_creation, name='dataset_creation'),
    path('datasets/edition/field/add-creator/<path:pid>', views_dataset.dataset_creator_addition, name='dataset_creator_addition'),
    path('datasets/edition/field/delete-creator/<path:pid>', views_dataset.dataset_creator_deletion, name='dataset_creator_deletion'),
    path('datasets/edition/field/add-maintainer/<path:pid>', views_dataset.dataset_maintainer_addition, name='dataset_maintainer_addition'),
    path('datasets/edition/field/delete-maintainer/<path:pid>', views_dataset.dataset_maintainer_deletion, name='dataset_maintainer_deletion'),
    path('datasets/edition/field/add-project/<path:pid>', views_dataset.dataset_project_addition, name='dataset_project_addition'),
    path('datasets/edition/field/delete-project/<path:pid>', views_dataset.dataset_project_deletion, name='dataset_project_deletion'),
    path('datasets/edition/field/add-article/<path:pid>', views_dataset.dataset_article_addition, name='dataset_article_addition'),
    path('datasets/edition/field/delete-article/<path:pid>', views_dataset.dataset_article_deletion, name='dataset_article_deletion'),
    path('datasets/edition/field/add-institution/<path:pid>', views_dataset.dataset_institution_addition, name='dataset_institution_addition'),
    path('datasets/edition/field/delete-institution/<path:pid>', views_dataset.dataset_institution_deletion, name='dataset_institution_deletion'),
    path('datasets/edition/delete-dataset/<path:pid>', views_dataset.dataset_deletion, name='dataset_deletion'),
    path('datasets/edition/field/<str:field_to_modify>/<path:pid>', views_dataset.dataset_field_edition, name='dataset_field_edition'),
    path('datasets/edition/<path:pid>', views_dataset.dataset_edition, name='dataset_edition'),
    path('datasets/<path:pid>', views_dataset.dataset_profile, name='dataset_profile'),

    # Institutions urls
    path('institutions/', views_institution.institution_results, name='institution_results'),
    path('institutions/filter/<int:page>/<str:filter_category>/', views_institution.institution_results, name='institution_results'),
    path('institutions/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_institution.institution_results, name='institution_results'),
    path('institutions/creation/', views_institution.institution_creation, name='institution_creation'),
    path('institutions/edition/field/add-parent-institution/<path:pid>', views_institution.institution_parent_organization_addition, name='institution_parent_organization_addition'),
    path('institutions/edition/field/delete-parent-institution/<path:pid>', views_institution.institution_parent_organization_deletion, name='institution_parent_organization_deletion'),
    path('institutions/edition/field/add-sub-institution/<path:pid>', views_institution.institution_sub_organization_addition, name='institution_sub_organization_addition'),
    path('institutions/edition/field/delete-sub-institution/<path:pid>', views_institution.institution_sub_organization_deletion, name='institution_sub_organization_deletion'),
    path('institutions/edition/field/add-worker/<path:pid>', views_institution.institution_worker_addition, name='institution_worker_addition'),
    path('institutions/edition/field/delete-worker/<path:pid>', views_institution.institution_worker_deletion, name='institution_worker_deletion'),
    path('institutions/edition/field/add-affiliate/<path:pid>', views_institution.institution_affiliate_addition, name='institution_affiliate_addition'),
    path('institutions/edition/field/delete-affiliate/<path:pid>', views_institution.institution_affiliate_deletion, name='institution_affiliate_deletion'),
    path('institutions/edition/field/add-article/<path:pid>', views_institution.institution_article_addition, name='institution_article_addition'),
    path('institutions/edition/field/delete-article/<path:pid>', views_institution.institution_article_deletion, name='institution_article_deletion'),
    path('institutions/edition/field/add-project/<path:pid>', views_institution.institution_project_addition, name='institution_project_addition'),
    path('institutions/edition/field/delete-project/<path:pid>', views_institution.institution_project_deletion, name='institution_project_deletion'),
    path('institutions/edition/field/add-dataset/<path:pid>', views_institution.institution_dataset_addition, name='institution_dataset_addition'),
    path('institutions/edition/field/delete-dataset/<path:pid>', views_institution.institution_dataset_deletion, name='institution_dataset_deletion'),
    path('institutions/edition/field/add-funder/<path:pid>', views_institution.institution_funder_addition, name='institution_funder_addition'),
    path('institutions/edition/field/delete-funder/<path:pid>', views_institution.institution_funder_deletion, name='institution_funder_deletion'),
    path('institutions/edition/delete-institution/<path:pid>', views_institution.institution_deletion, name='institution_deletion'),
    path('institutions/edition/field/<str:field_to_modify>/<path:pid>', views_institution.institution_field_edition, name='institution_field_edition'),
    path('institutions/edition/<path:pid>', views_institution.institution_edition, name='institution_edition'),
    path('institutions/<path:pid>', views_institution.institution_profile, name='institution_profile'),


    # Funders urls
    path('funders/', views_funder.funder_results, name='funder_results'),
    path('funders/filter/<int:page>/<str:filter_category>/', views_funder.funder_results, name='funder_results'),
    path('funders/filter/<int:page>/<str:filter_category>/<str:filter_letter>', views_funder.funder_results, name='funder_results'),
    path('funders/edition/field/add-project/<path:pid>', views_funder.funder_project_addition, name='funder_project_addition'),
    path('funders/edition/field/delete-project/<path:pid>', views_funder.funder_project_deletion, name='funder_project_deletion'),


    # Visualizer
    path('visualizer', views_visualizer.index, name='visualizer_index'),
]
