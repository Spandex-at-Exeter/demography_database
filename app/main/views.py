from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import ContactForm
from flask_mail import Mail, Message
from app.matrix_functions import all_species_unreleased, all_populations_unreleased,all_matrices_unreleased, \
all_species_unreleased_complete, all_populations_unreleased_complete, all_matrices_unreleased_complete, \
all_species_released_complete, all_populations_released_complete, all_matrices_released_complete, \
all_species_released_compadre, all_populations_released_compadre, all_matrices_released_compadre, \
all_species_released_comadre, all_populations_released_comadre, all_matrices_released_comadre, \
all_matrices, all_pops, all_species, count_plants, count_comadre, count_compadre, count_plants_pop, count_compadre_pop, count_comadre_pop, species_compadre_count, species_comadre_count
from ..data_manage.forms import SpeciesForm, TaxonomyForm, TraitForm, PopulationForm, MatrixForm, PublicationForm, DeleteForm

import random

from .. import db
from ..models import Permission, Role, User, \
                    IUCNStatus, OrganismType, GrowthFormRaunkiaer, ReproductiveRepetition, \
                    DicotMonoc, AngioGymno, SpandExGrowthType, SourceType, Database, Purpose, MissingData, ContentEmail, Ecoregion, Continent, InvasiveStatusStudy, InvasiveStatusElsewhere, StageTypeClass, \
                    TransitionType, MatrixComposition, StartSeason, EndSeason, StudiedSex, Captivity, Species, Taxonomy, PurposeEndangered, PurposeWeed, Trait, \
                    Publication, AuthorContact, AdditionalSource, Population, Stage, StageType, Treatment, \
                    MatrixStage, MatrixValue, Matrix, Interval, Fixed, Small, CensusTiming, Institute, Status, Version, ChangeLogger, DigitizationProtocol
from ..decorators import admin_required, permission_required, crossdomain


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


#@main.route('/shutdown')
#def server_shutdown():
#    if not current_app.testing:
#        abort(404)
#    shutdown = request.environ.get('werkzeug.server.shutdown')
#    if not shutdown:
#        abort(500)
#    shutdown()
#    return 'Shutting down...'

# HOMEPAGE

@main.route('/', methods=['GET', 'POST'])
def index():
    ##Released and Complete Stats
    #1. Total
    all_species_released_green = all_species_released_complete()
    all_populations_released_green = all_populations_released_complete()
    all_matrices_released_green = all_matrices_released_complete()
    #2. Compadre
    all_species_released_compadre_green = all_species_released_compadre()
    all_populations_released_compadre_green = all_populations_released_compadre()
    all_matrices_released_compadre_green = all_matrices_released_compadre()
    #3. Comadre
    all_species_released_comadre_green = all_species_released_comadre()
    all_populations_released_comadre_green = all_populations_released_comadre()
    all_matrices_released_comadre_green = all_matrices_released_comadre()
    ##Released and Incomplete Stats
    #NDY 1. total, 2. compadre, 3. comadre

    ##Unreleased and Incomplete Stats
    #1. Total 
    all_species_unreleased_amber = all_species_unreleased()
    all_populations_unreleased_amber = all_populations_unreleased()
    all_matrices_unreleased_amber = all_matrices_unreleased()
    #2. Compadre
    #NDY
    #3. Comadre
    #NDY
    ##Unreleased and Complete Stats
    #1. Total
    all_species_unreleased_green = all_species_unreleased_complete()
    all_populations_unreleased_green = all_populations_unreleased_complete()
    all_matrices_unreleased_green = all_matrices_unreleased_complete()
    #2. Compadre
    #3. Comadre

    ##Admin use only stats
    #Matrix Stats
    count_matrices = all_matrices()
    comadre_count = count_comadre()
    compadre_count = count_compadre()
    plant_count = count_plants()
    #Population Stats
    count_pops = all_pops()
    comadre_count_pop = count_comadre_pop()
    compadre_count_pop = count_compadre_pop()
    plant_count_pop = count_plants_pop()
    #Species stats
    species_count = all_species()
    species_count_compadre = species_compadre_count()
    species_count_comadre = species_comadre_count()     
    species = Species.query.filter(Species.image_path != None).all()
    number = len(species)
    species2 = []
    for i in range(1,5):
        random_int = random.randint(0,number-1)
        s = species[random_int]
        species2.append(s)
    return render_template('index.html',species2 = species2, all_species_released_green = all_species_released_green, all_populations_released_green = all_populations_released_green, 
           all_matrices_released_green = all_matrices_released_green, all_species_released_compadre_green = all_species_released_compadre_green,
           all_populations_released_compadre_green = all_populations_released_compadre_green, all_matrices_released_compadre_green = all_matrices_released_compadre_green, 
           all_species_released_comadre_green = all_species_released_comadre_green, all_populations_released_comadre_green = all_populations_released_comadre_green, all_matrices_released_comadre_green = all_matrices_released_comadre_green, 
           all_species_unreleased_amber = all_species_unreleased_amber, all_species_unreleased_green = all_species_unreleased_green, 
           all_populations_unreleased_amber = all_populations_unreleased_amber, all_populations_unreleased_green = all_populations_unreleased_green, 
           all_matrices_unreleased_amber = all_matrices_unreleased_amber, all_matrices_unreleased_green = all_matrices_unreleased_green, 
           count_matrices = count_matrices, comadre_count = comadre_count, compadre_count = compadre_count, plant_count = plant_count, 
           count_pops = count_pops, comadre_count_pop = comadre_count_pop, compadre_count_pop = compadre_count_pop, plant_count_pop = plant_count_pop,
           species_count = species_count, species_count_compadre = species_count_compadre, species_count_comadre = species_count_comadre)


# now defunct 'display all data' page
@main.route('/data/')
# @login_required
def data():
    species = Species.query.all()

    return render_template('data.html', species=species)

### TABLE PAGES
# the big table of species
@main.route('/species-table/')
def species_table():
    # species = Species.query.all()
    species = Species.query.all()
    return render_template('species_table_template.html', species=species)

# the big table of publications
@main.route('/publications-table/')
def publications_table():
    publications = Publication.query.all()
    return render_template('publications_table_template.html', publications=publications)

###############################################################################################################################
### OVERVIEW PAGES
# species overview page
@main.route('/species=<list:species_ids>/publications=<list:pub_ids>')
def species_page(species_ids,pub_ids):
    if species_ids[0] == "all" and pub_ids[0] == "all":
        flash('Loading all species and publications is not allowed, sorry.')
        abort(404)
    
    try:
        #get species
        all_species = []
        if species_ids[0] != "all": # aka if species are filtered
            for id in species_ids:
                all_species.append((Species.query.filter_by(id=id)).first())

            all_populations_species = []
            for species in all_species:
                all_populations_species.extend(Population.query.filter_by(species_id=species.id).all())

        #get pubs
        all_pubs = []
        if pub_ids[0] != "all": # aka if publications are being filtered
            for id in pub_ids:
                all_pubs.append((Publication.query.filter_by(id=id)).first())

            all_populations_pubs = []
            for publications in all_pubs:
                all_populations_pubs.extend(Population.query.filter_by(publication_id=publications.id).all())
    except:
        abort(404)
            
    # variable for whether to show the compadrino info box at the top (when only 1 publication is selected)
    compadrino_info = False
    if species_ids[0] == "all" and len(pub_ids) == 1:
        compadrino_info = True
        
      
    # Pick the right populations + get stuff
    if species_ids[0] == "all": # aka if species are filtered 
        populations = all_populations_pubs
    elif pub_ids[0] == "all": # aka if publications are being filtered
        populations = all_populations_species
    else: # aka if publications AND species are being filtered
        populations = set(all_populations_species).intersection(all_populations_pubs)
    
    
    if species_ids[0] != "all":  #aka if species are filtered 
        all_pubs = []
        for population in populations:
            all_pubs.append(Publication.query.filter_by(id=population.publication_id).first())
        
    if pub_ids[0] != "all": # aka if publications are being filtered
        all_species = []
        for population in populations:
            all_species.append(Species.query.filter_by(id=population.species_id).first())
        
    # remove duplicates 
    
    
    populations = list(set(populations))
    all_species = list(set(all_species))
    publications = list(set(all_pubs))
    
    #print(publications)
    #publications.sort();
    #print(publications)
    
    can_edit = False
    try:
        if current_user.role_id in [1,3,4,6]:
            can_edit = True
    except:
        pass
    
    exeter_data = False
    try:
        if current_user.institute.institution_short == "UoE" and current_user.institute_confirmed == 1:
            exeter_data = True
    except:
        pass

    
    protocol = DigitizationProtocol.query.all() 
        
    protocol_dict = {}
    for ocol in protocol:
        protocol_dict[ocol.name_in_csv] = ocol.field_short_description   
    
    return render_template('species_template.html',all_species = all_species, publications = publications, populations = populations,can_edit = can_edit,exeter_data = exeter_data,compadrino_info = compadrino_info,protocol_dict = protocol_dict)

@main.route('/protocol')
def protocol_page():
    protocol = DigitizationProtocol.query.all() 
        
    protocol_dict = {}
    for ocol in protocol:
        protocol_dict[ocol.name_in_csv] = ocol.field_description 
        
    return render_template('protocol_template.html',protocol_dict = protocol_dict,protocol = protocol)

# Taxonomic explorer
# DOES NOT WORK IN FIREFOX
@main.route('/explorer/<taxon_level>/<taxon>')
# @login_required
def explorer(taxon_level,taxon):
    if taxon_level == "life":
        taxon_list = Taxonomy.query.all()
        next_taxon_level = "kingdom"
        tax_pos = 0
    elif taxon_level == "kingdom":
        taxon_list = Taxonomy.query.filter_by(kingdom=taxon).all()
        next_taxon_level = "phylum"
        tax_pos = 1
    elif taxon_level == "phylum":
        taxon_list = Taxonomy.query.filter_by(phylum=taxon).all()
        next_taxon_level = "class" 
        tax_pos = 2
    elif taxon_level == "class":
        taxon_list = Taxonomy.query.filter_by(tax_class=taxon).all()
        next_taxon_level = "order"
        tax_pos = 3
    elif taxon_level == "order":
        taxon_list = Taxonomy.query.filter_by(tax_order=taxon).all()
        next_taxon_level = "family"
        tax_pos = 4
    elif taxon_level == "family":
        taxon_list = Taxonomy.query.filter_by(family=taxon).all()
        next_taxon_level = "species"
        tax_pos = 5
    
    
    return render_template('explorer_template.html',taxon=taxon,taxon_list = taxon_list,taxon_level=taxon_level,next_taxon_level=next_taxon_level, tax_pos = tax_pos)


# contribute
@main.route('/contribute-data')
def contribute_data():
    return render_template('contribute_data.html')

#coming soon page
@main.route('/comingsoon')
def comingsoon():
    return render_template('coming_soon.html')

###############################################################################################################################
### Become a Compadrino Form and HTML page
@main.route('/become-a-compadrino', methods=('GET', 'POST'))
def become_a_compadrino():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            return 'Please fill in all fields <p><a href="/become-a-compadrino">Try Again!!!</a></p>'
        else:
            msg = Message("Message from your visitor" + form.name.data,
                          sender='YourUser@NameHere',
                          recipients=['compadre@gmail.com', 'spandex.ex@gmail.com'])
            msg.body = """
            From: %s <%s>,
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return "Successfully  sent message!"
    elif request.method == 'GET':
        return render_template('become_a_compadrino.html', form=form)


### Help Develop Site Form
@main.route('/help-develop-site', methods=('GET', 'POST'))
def help_develop_site():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            return 'Please fill in all fields <p><a href="/help-develop-site">Try Again!!!</a></p>'
        else:
            msg = Message("Message from your visitor" + form.name.data,
                          sender='YourUser@NameHere',
                          recipients=['spandex.ex@gmail.com', 'd.l.buss@exeter.ac.uk'])
            msg.body = """
            From: %s <%s>,
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return "Successfully  sent message!"
    elif request.method == 'GET':
        return render_template('help_develop_site.html', form=form)

### NEW DATA INPUT FORMS

#@main.route('/species/new', methods=['GET', 'POST'])
#def species_new_form():
#    form = SpeciesForm()
#    if form.validate_on_submit():
#        species = Species()
#        
#        species.species_accepted = form.species_accepted.data
#        species.species_common = form.species_common.data
#        species.iucn_status = form.iucn_status.data
#        species.esa_status = form.esa_status.data
#        species.invasive_status = form.invasive_status.data
#        species.gbif_taxon_key = form.gbif_taxon_key.data
#        species.image_path = form.image_path.data
#        species.image_path2 = form.image_path2.data
#        
#        db.session.add(species)
#        db.session.commit()
#
#        return redirect(url_for('.species_page',id=species.id))
#    
#    return render_template('data_entry/generic_form.html', form=form)
#
#@main.route('/taxonomy/new/species=<int:id_sp>', methods=['GET', 'POST'])
#def taxonomy_new_form(id_sp):
#    species = Species.query.get_or_404(id_sp)
#    form = TaxonomyForm()
#    
#    if form.validate_on_submit():
#        taxonomy = Taxonomy()
#        taxonomy.species_id = species.id
#        taxonomy.species_author = form.species_author.data
#        taxonomy.authority = form.authority.data
#        taxonomy.taxonomic_status = form.taxonomic_status.data
#        taxonomy.tpl_version = form.tpl_version.data
#        taxonomy.infraspecies_accepted = form.infraspecies_accepted.data
#        taxonomy.species_epithet_accepted = form.species_epithet_accepted.data 
#        taxonomy.genus_accepted = form.genus_accepted.data
#        taxonomy.genus = form.genus.data
#        taxonomy.family = form.family.data
#        taxonomy.tax_order = form.tax_order.data
#        taxonomy.tax_class = form.tax_class.data
#        taxonomy.phylum = form.phylum.data
#        taxonomy.kingdom = form.kingdom.data
#        
#        db.session.add(taxonomy)
#        db.session.commit()
#        
#        return redirect(url_for('.species_page',id=id_sp))
#    
#    return render_template('data_entry/generic_form.html', form=form,species = species)
#
#@main.route('/traits/new/species=<int:id_sp>', methods=['GET', 'POST'])
#def trait_new_form(id_sp):
#    species = Species.query.get_or_404(id_sp)
#    form = TraitForm()
#    
#    if form.validate_on_submit():
#        Trait = Trait()
#        trait.species_id = species.id
#        
#        trait.max_height = form.max_height.data
#        trait.organism_type = form.organism_type.data
#        trait.growth_form_raunkiaer = form.growth_form_raunkiaer.data
#        trait.reproductive_repetition = form.reproductive_repetition.data
#        trait.dicot_monoc = form.dicot_monoc.data
#        trait.angio_gymno = form.angio_gymno.data
#        return redirect(url_for('.species_page',id=id_sp))
#    
#    return render_template('data_entry/generic_form.html', form=form,species = species)
#
#@main.route('/publication/new', methods=['GET', 'POST'])
#def new_publication_form():
#    form = PublicationForm()
#    
#    if form.validate_on_submit():
#        publication = Publication()
#        
#        publication.source_type = form.source_type.data
#        publication.authors = form.authors.data 
#        publication.editors = form.editors.data
#        publication.pub_title = form.pub_title.data
#        publication.journal_book_conf = form.journal_book_conf.data
#        publication.year = form.year.data
#        publication.volume = form.volume.data
#        publication.pages = form.pages.data
#        publication.publisher = form.publisher.data
#        publication.city = form.city.data
#        publication.country = form.country.data
#        publication.institution = form.institution.data
#        publication.DOI_ISBN = form.DOI_ISBN.data
#        publication.name = form.pub_name.data
#        publication.corresponding_author = form.corresponding_author.data
#        publication.email = form.email.data
#        publication.purposes_id = form.purposes.data
#        publication.embargo = form.embargo.data
#        publication.missing_data = form.missing_data.data
#        publication.additional_source_string = form.additional_source_string.data  
#        
#        db.session.add(publication)
#        db.session.commit()
#        
#        return redirect(url_for('.publication_page',id=publication.id))
#    
#    return render_template('data_entry/publication_form.html',form=form)
#
#@main.route('/population/new/publication=<int:id_pub>/choose_species', methods=['GET'])
#def choose_species(id_pub):
#    publication = Publication.query.get_or_404(id_pub)
#    species = Species.query.all()
#    
#    return render_template('data_entry/choose_species.html',publication=publication,species=species)
#    
#@main.route('/population/new/publication=<int:id_pub>/species=<int:id_sp>', methods=['GET', 'POST'])
#def population_new_form(id_pub,id_sp):
#    publication = Publication.query.get_or_404(id_pub)
#    species = Species.query.get_or_404(id_sp)
#    form = PopulationForm()
#    
#    if form.validate_on_submit():
#        population = Population()
#        population.publication_id = id_pub
#        population.species_id = id_sp
#        
#        population.name = form.name.data
#        population.ecoregion = form.ecoregion.data
#        population.country = form.country.data
#        population.continent = form.continent.data
#        population.latitude = form.latitude.data
#        population.longitude = form.longitude.data
#        population.altitude = form.altitude.data
#        
#        db.session.add(population)
#        db.session.commit()
#        
#        return redirect(url_for('.publication_page',id=id_pub))
#    
#    return render_template('data_entry/generic_form.html', form=form, publication=publication, species=species)

# USER + PROFILE PAGES
# User
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()    
    return render_template('user.html', user=user)






