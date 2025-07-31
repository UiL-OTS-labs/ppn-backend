#html text weghalen 
#mail laten werken
#html test


import uuid
import pytest
from playwright.sync_api import expect



def test_backend_starts(page_en, backend_app):
    page_en.goto(backend_app.url)
    assert page_en.title() == 'ILS Labs Experiments Admin'


def test_frontend_starts(page_en, as_admin, frontend_app):
    page_en.goto(frontend_app.url)
    assert page_en.title() == 'Experimenten ILS Labs'


def test_create_easy_experiment(apps, as_admin):

    """ Test if a researcher can create a simple test 
    with mild criteria """

    Experiment = apps.backend.get_model('experiments', 'Experiment')
    Location = apps.backend.get_model('experiments', 'Location')
    apps.backend.load('leader.json')
    location = Location.objects.create(name="Test Lab")
    page = as_admin
    page.goto(f"{apps.backend.url}/experiments/new/")


    # Fill in the experiment form
    page.fill('input[name="name"]', 'Verhalen en emotie 4: De buurman is een klootzak')
    page.fill('input[name="duration"]', 'ongeveer twee uur')
    page.fill('input[name="compensation"]', '20 euro')

    frame = page.frame_locator('#id_task_description_ifr')
    frame.locator('body').fill("De sessie bestaat uit 3 delen, waarvan het eerste deel het langste duurt. In deel 1 lees je op een computerscherm 64 korte verhaaltjes opgedeeld in kleine fragmenten. Bij elk verhaaltje wordt je gevraagd om het gedrag van de hoofdpersoon te beoordelen met een rating. Tijdens deze eerste taak meten we ook de activiteit van je gezichtsspieren.\r\n\r\nHet tweede deel is een vragenlijst waarbij je dezelfde verhaaltjes te zien krijgt, maar nu in hun geheel. We vragen dan of je met behulp van een ratingschaal wilt aangeven wat je van de afloop van het verhaaltje vindt.\r\nDeel 3 bestaat uit een korte vragenlijst over jouw perspectief op menselijk gedrag.\r\n\r\nIn totaal zul je voor dit experiment circa 2 uur in het lab zijn.")
    frame = page.frame_locator('#id_additional_instructions_ifr')
    frame.locator('body').fill("Je kunt alleen meedoen met dit experiment als je voldoet aan de volgende criteria:\r\n<ul><li>bent opgegroeid met het Nederlands als moedertaal (meerdere moedertalen is geen bezwaar)</li>\r\n<li>je bent niet dyslectisch</li>\r\n<li>je bent tussen de 18 en 30 jaar oud</li>\r\n<li>je bent student</li>\r\n<li>je hebt niet eerder deelgenomen aan een van de volgende experimenten: Verhalen en emotie (november 2014-januari 2015), Verhalen en emotie 2 (oktober-november 2015), Persoonlijkheid en lezen (juni 2016)</li>\r\n<li>je bent op dit moment geen eerste- of tweedejaars student in de RMA linguistics (want dan heb je weleens een presentatie over dit onderzoek gehoord, en als je weet waar het over gaat kun je niet meedoen)</li>\r\n<li>je hebt geen botox-behandeling in je gezicht gehad</li>\r\n<li>je hebt geen baardgroei op de diagonale lijn tussen je mondhoek en de bovenste aanzet van je oor, dus waar je oor aan je hoofd vastzit, zie plaatje:<br/> <img src=\"https://resources.lab.hum.uu.nl/resources/plaatjes_voor_ppnsysteem/baardgroei_diagonaal_cirkel.png\"alt=\"Diagonale lijn van mondhoek naar bovenkant oor\" style=\"width:236px;height:225px;\">\r\n</li>\r\n</ul>")
    page.select_option('select[name="location"]', label='Test Lab')
    page.check('input[name="use_timeslots"]')
    page.fill('input[name="default_max_places"]', '1')
    page.check('input[name="open"]')
    page.check('input[name="public"]')
    page.select_option('select[name="leader"]', label='Ben')

    page.click('#submit')

    # Criteria for experiment
    page.locator('input#id_language_2').click()    
    page.locator('#id_multilingual_2').click()     
    page.locator('#id_sex_2').click()              
    page.locator('#id_handedness_2').click()      
    page.locator('#id_dyslexia_2').click()        
    page.locator('#id_social_status_2').click()   
    page.fill('input[name="min_age"]', '18')      
    page.fill('input[name="max_age"]', '60')      

    page.locator('button:has-text("Save")').click()  
 
    page.goto(f"{apps.backend.url}/experiments/1/timeslots/")
    input = page.locator("#id_datetime")
    current_value = input.input_value()  
    date = current_value.split(" ")[0]  
    input.fill(f"{date} 9:45")
    page.click ('#save-new-slot')      
    input.fill(f"{date} 23:59") 
    page.click ('#save-new-slot')
    input.fill(f"{date} 11:32")
    page.click ('#save-new-slot')
    input.fill(f"{date} 15:11")
    page.click ('#save-new-slot')
    

    assert Experiment.objects.filter(name="Verhalen en emotie 4: De buurman is een klootzak").exists()

def test_create_difficult_experiment(apps, as_admin):

    """ Test if a researcher can make a complex test 
    with harsh criteria """

    Experiment = apps.backend.get_model('experiments', 'Experiment')
    Location = apps.backend.get_model('experiments', 'Location')
    apps.backend.load('leader.json')
    location = Location.objects.create(name="Test Lab")
    page = as_admin
    page.goto(f"{apps.backend.url}/experiments/new/")


    # Fill in the experiment form
    page.fill('input[name="name"]', 'Leer een taal van een andere planeet')
    page.fill('input[name="duration"]', 'ongeveer 30 minutes')
    page.fill('input[name="compensation"]', 'een <a href=\"https://cadeau.yesty.nl/\">yesty cadeaubon</a> van 5 euro')
   
    frame = page.frame_locator('#id_task_description_ifr')
    frame.locator('body').fill("<p>In dit experiment hoor je eerst woorden uit een taal van een andere planeet. Daarna hoor je nieuwe woorden uit dezelfde taal en krijg je vragen over wat je net gehoord hebt.</p>")
    frame = page.frame_locator('#id_additional_instructions_ifr')
    frame.locator('body').fill("<p>Je kunt alleen meedoen met dit experiment als je bent opgegroeid met het Nederlands als moedertaal (meerdere moedertalen is geen bezwaar), en als je tussen de 18 en 69 jaar oud bent.<br>Je kunt niet meedoen aan dit onderzoek als je een aandachtsstoornis hebt, of als je dyslectisch bent.<br>Bovendien kun je niet meedoen als je al hebt meegedaan aan de onderzoeken \"Leer een buitenaardse taal\" (vanaf maart 2023) of \"Een fantasietaal\" (vanaf mei 2024).</p>")
    page.select_option('select[name="location"]', label='Test Lab')
    page.check('input[name="use_timeslots"]')
    page.fill('input[name="default_max_places"]', '1')
    page.check('input[name="open"]')
    page.check('input[name="public"]')
    page.select_option('select[name="leader"]', label='Ben')

    page.click('#submit')

    # Criteria for experiment
    page.locator('input#id_language_0').click()    
    page.locator('#id_multilingual_0').click()     
    page.locator('#id_sex_0').click()              
    page.locator('#id_handedness_0').click()      
    page.locator('#id_dyslexia_1').click()      
    page.locator('#id_social_status_1').click()   
    page.fill('input[name="min_age"]', '18')      
    page.fill('input[name="max_age"]', '20')     

    page.locator('button:has-text("Save")').click()  
    page.goto(f"{apps.backend.url}/experiments/2/timeslots/")
    input = page.locator("#id_datetime")
    current_value = input.input_value()  
    date = current_value.split(" ")[0]

    input.fill(f"{date} 23:59")
    page.click ('#save-new-slot')  
    input.fill(f"{date} 9:45")
    page.click ('#save-new-slot')      
    input.fill(f"{date} 11:32")
    page.click ('#save-new-slot')
    input.fill(f"{date} 15:11")
    page.click ('#save-new-slot')


    assert Experiment.objects.filter(name="Leer een taal van een andere planeet").exists()
    
   
def test_create_users(page, apps):
    """ Test if you can create multiple users with sign up form """

    page.goto(f"{apps.frontend.url}/participant/sign_up/")

    page.fill('input[name="email"]', 'Alberta.Bacon@test.com')   
    page.locator('input#id_language_0').click()
    page.locator('#id_multilingual_0').click()                 
    page.locator('#id_dyslexic_1').click()                       
    page.locator('#id_mailing_list_0').click() 

    page.click('#submit')
    assert page.url == (f"{apps.frontend.url}participant/sign_up/subscribed/")

    page.goto(f"{apps.frontend.url}/participant/sign_up/")

    page.fill('input[name="email"]', 'ChrisP.Bacon@test.com')   
    page.locator('input#id_language_0').click()
    page.locator('#id_multilingual_0').click()                 
    page.locator('#id_dyslexic_1').click()                       
    page.locator('#id_mailing_list_0').click()                   

    page.click('#submit')
    assert page.url == (f"{apps.frontend.url}participant/sign_up/subscribed/")

    
def test_create_right_user(page, apps):
    ''' Test if a user can sign up using the specific experiment sign up form '''

    page.goto(f"{apps.frontend.url}/participant/register/1/")

    page.fill('input[name="name"]', 'Han S. Olo')           
    page.fill('input[name="email"]', 'HanS.Olo@test.com')   
    page.fill('input[name="phone"]', '0610032023')             
    page.fill('input[name="birth_date"]', '15-09-2005')         
    page.locator('input#id_language_0').click()
    page.locator('input#id_language_0').click()                
    page.locator('#id_multilingual_0').click()                  
    page.locator('#id_sex_0').click()                           
    page.locator('#id_handedness_1').click()                    
    page.locator('#id_dyslexic_1').click()                      
    page.locator('#id_social_status_0').click()                 
    page.locator('#id_timeslot_0').click()                     
    page.locator('#id_mailinglist_1').click()                   
    page.locator('#id_consent_0').click()                       
    assert page.get_by_text(", 9:45 uur").count() == 0
    assert page.get_by_text(", 15:11 uur").count() == 1
    page.click('#submit')
    assert page.url == (f"{apps.frontend.url}participant/register/1/success/")
     

def test_create_wrong_user(page, apps):

    ''' Test if a participant can't join an experiment 
    they're not qualified for with all the reasons why'''

    page.goto(f"{apps.frontend.url}/participant/register/2/")

    page.fill('input[name="name"]', 'Anita Beth')              
    page.fill('input[name="email"]', 'Anita.Beth@test.com')    
    page.fill('input[name="phone"]', '0613052004')              
    page.fill('input[name="birth_date"]', '15-08-2003')         
    page.locator('input#id_language_0').click()
    page.locator('input#id_language_0').click()                
    page.locator('#id_multilingual_1').click()                 
    page.locator('#id_sex_1').click()                          
    page.locator('#id_handedness_1').click()               
    page.locator('#id_dyslexic_0').click()                  
    page.locator('#id_social_status_0').click()                 
    page.locator('#id_timeslot_0').click()                      
    page.locator('#id_mailinglist_1').click()                   
    page.locator('#id_consent_0').click()                       
    

    
    reasons = [
        "omdat je geslacht niet overeen komt",
        "omdat je voorkeurshand niet overeen komt",
        "omdat je volgens onze gegevens student bent",
        "omdat je volgens onze gegevens dyslectisch bent", 
        "omdat je meertalig bent",
        "omdat je leeftijd niet overeen komt"
    ]
   
    page.click('#submit')
    text = page.locator(".uu-hero.text-bg-warning").text_content()
    text = " ".join(text.split())
    
    for reason in reasons:
        assert reason in text, f"Reden niet gevonden: {reason}"


def test_remove_from_timeslot(apps, as_admin):

    ''' Test if the researcher can delete a timeslot'''

    apps.backend.load('leader.json')
    page = as_admin
    page.goto(f"{apps.backend.url}/experiments/1/timeslots/delete/1")
    page.locator('#delete-all-selected').click() 
    success_alert = page.locator(".alert")
    expect(success_alert).to_have_text('Timeslot removed!')
    assert success_alert.is_visible()

    
def test_invite_participant(apps, as_admin):

    ''' Testing if the researcher can invite participants and only the right participant
    is in the list of avaible participants'''
    

    apps.backend.load('leader.json')
    page = as_admin
    page.goto(f"{apps.backend.url}/experiments/2/invite/")
    assert page.locator("text=Han S. Olo").count() == 0 #because he's not a student
    page.check('input[name="participants[]"]')
    page.get_by_role("button", name="Invite participants").click()
    success_alert = page.locator(".alert")
    expect(success_alert).to_have_text('Successfully invited participants!')
    assert success_alert.is_visible()
    
    
def test_merge_participant(apps, as_admin):

    """ Test if two participant merge succesfully """

    apps.backend.load('leader.json')
    page = as_admin

    page.goto(f"{apps.backend.url}/participants/merge/")

    page.click("#select2-id_old_participant-container")
    old_option = page.locator("li.select2-results__option", has_text="[1] name unknown")
    old_option.click()

    page.click("#select2-id_new_participant-container")
    new_option = page.locator("li.select2-results__option", has_text="[3] Han S. Olo")
    new_option.click()

    page.click("button.btn.btn-primary:has-text('Merge participants')")

    success_alert = page.locator("div.alert.alert-success")
    expect(success_alert).to_have_text("Participant merged!")
    assert success_alert.is_visible()
    page.goto(f"{apps.backend.url}/participants/")
    table_body = page.locator("#DataTables_Table_0 tbody")
    rows_count = table_body.locator("tr").count()
    assert rows_count == 2, f"Expected 2 participant, but found {rows_count}"


def test_delete_participant(apps, as_admin):

    ''' Test if the researcher can delete a participant'''

    apps.backend.load('leader.json')
    page = as_admin
    
    page.goto(f"{apps.backend.url}/participants/1/del/")
    page.get_by_role("button", name="Delete participant").click()

    cell = page.locator("td.dtr-control.sorting_1", has_text="1")

    assert cell.count() == 0


def test_comment(apps,as_admin):

    """ Test if comments can be placed and are visible """

    apps.backend.load('leader.json')
    page = as_admin

    page.goto(f"{apps.backend.url}/comments/new/2/1")
    page.fill('textarea[name="comment"]', 'is vervelend')
    page.click("button.btn.btn-primary:has-text('Add')")

    success_alert = page.locator("div.alert.alert-success")
    expect(success_alert).to_have_text("Comment added!")
    assert success_alert.is_visible()

    page.goto(f"{apps.backend.url}/comments/")
    row_with_comment = page.locator("#DataTables_Table_0 tbody tr", has_text="is vervelend")
    expect(row_with_comment).to_have_count(1)
