from jobApp.jobEngine.ai.formFiller import FormFiller
from dotenv import load_dotenv
import os
from jobApp.jobEngine.job.job import Job

load_dotenv()
form_filler = FormFiller()
# fill job obj with random data
job = Job(
    id=None,
    job_id=12345,
    link="https://example.com/job",
    job_title="Software Engineer",
    job_location="Berlin, Germany",
    company_name="Expleo",
    num_applicants=None,
    posted_date=None,
    job_description="Software engineering position with focus on Python development",
    company_emails=None,
    job_poster_name=None,
    application_type=None,
    applied=False
)
form_filler.set_job(job)
context = form_filler.load_from_yaml(os.environ.get("YAML_PATH"))
form_filler.set_user_context(context)

language_levels = [
    "A1 (Basic user - very basic communication skills / working knowledge)",
    "A2 (Basic user - basic communication skills / working knowledge)",
    "B1 (Independent user - intermediate communication skills / professional working knowledge)",
    "B2 (Independent user - upper intermediate communication skills / professional working knowledge)",
    "C1 (Proficient user - advanced communication skills / full professional working knowledge)",
    "C2 (Proficient user - full professional working knowledge)"
]

country_phone_codes = [
    "Selectionner une option, ""Afghanistan (+93)", "Afrique du Sud (+27)", "Albanie (+355)", "Algérie (+213)", "Allemagne (+49)", 
    "Andorre (+376)", "Angola (+244)", "Arabie Saoudite (+966)", "Argentine (+54)", "Arménie (+374)", 
    "Australie (+61)", "Autriche (+43)", "Azerbaïdjan (+994)", "Bahamas (+1)", "Bahreïn (+973)", "Bangladesh (+880)", 
    "Belgique (+32)", "Bénin (+229)", "Bhoutan (+975)", "Biélorussie (+375)", "Bolivie (+591)", "Botswana (+267)", 
    "Brésil (+55)", "Bulgarie (+359)", "Burkina Faso (+226)", "Burundi (+257)", "Cambodge (+855)", "Cameroun (+237)", 
    "Canada (+1)", "Chili (+56)", "Chine (+86)", "Chypre (+357)", "Colombie (+57)", "Comores (+269)", "Congo (+242)", 
    "Corée du Sud (+82)", "Costa Rica (+506)", "Côte d'Ivoire (+225)", "Croatie (+385)", "Cuba (+53)", "Danemark (+45)", 
    "Djibouti (+253)", "Dominique (+1)", "Égypte (+20)", "Émirats Arabes Unis (+971)", "Équateur (+593)", "Érythrée (+291)", 
    "Espagne (+34)", "Estonie (+372)", "États-Unis (+1)", "Éthiopie (+251)", "Fidji (+679)", "Finlande (+358)", "France (+33)", 
    "Gabon (+241)", "Gambie (+220)", "Géorgie (+995)", "Ghana (+233)", "Grèce (+30)", "Guatemala (+502)", "Guinée (+224)", 
    "Haïti (+509)", "Honduras (+504)", "Hongrie (+36)", "Inde (+91)", "Indonésie (+62)", "Irak (+964)", "Iran (+98)", 
    "Irlande (+353)", "Islande (+354)", "Italie (+39)", "Japon (+81)", "Jordanie (+962)", "Kazakhstan (+7)", "Kenya (+254)", 
    "Kirghizistan (+996)", "Koweït (+965)", "Laos (+856)", "Lettonie (+371)", "Liban (+961)", "Libye (+218)", 
    "Liechtenstein (+423)", "Lituanie (+370)", "Luxembourg (+352)", "Madagascar (+261)", "Malaisie (+60)", "Mali (+223)", 
    "Malte (+356)", "Maroc (+212)", "Maurice (+230)", "Mexique (+52)", "Moldavie (+373)", "Monaco (+377)", "Mongolie (+976)", 
    "Monténégro (+382)", "Mozambique (+258)", "Namibie (+264)", "Népal (+977)", "Nicaragua (+505)", "Niger (+227)", 
    "Nigéria (+234)", "Norvège (+47)", "Nouvelle-Zélande (+64)", "Oman (+968)", "Ouganda (+256)", "Ouzbékistan (+998)", 
    "Pakistan (+92)", "Palestine (+970)", "Panama (+507)", "Paraguay (+595)", "Pays-Bas (+31)", "Pérou (+51)", 
    "Philippines (+63)", "Pologne (+48)", "Portugal (+351)", "Qatar (+974)", "République centrafricaine (+236)", 
    "République tchèque (+420)", "Roumanie (+40)", "Royaume-Uni (+44)", "Russie (+7)", "Rwanda (+250)", "Salvador (+503)", 
    "Sénégal (+221)", "Serbie (+381)", "Singapour (+65)", "Slovaquie (+421)", "Slovénie (+386)", "Somalie (+252)", 
    "Soudan (+249)", "Sri Lanka (+94)", "Suède (+46)", "Suisse (+41)", "Suriname (+597)", "Syrie (+963)", "Tadjikistan (+992)", 
    "Tanzanie (+255)", "Tchad (+235)", "Thaïlande (+66)", "Togo (+228)", "Tunisie (+216)", "Turquie (+90)", "Ukraine (+380)", 
    "Uruguay (+598)", "Vatican (+379)", "Venezuela (+58)", "Vietnam (+84)", "Yémen (+967)", "Zambie (+260)", "Zimbabwe (+263)"
]

questions_with_options = {
    "Do you require visa sponsorship for the country of work, in this case germany?": ["Yes", "No"],
    "Code Pays": country_phone_codes,
    "Numéro de téléphone portable": [], 
   "Welche Gehaltsvorstellung hast Du für das Jahresbrutto in dieser Position?": [],
    "What are your salary expectations? (EUR)": [],
    "What is your language proficiency (written/spoken) on an A1-C2 scale in German?": language_levels,
    "What is your language proficiency (written/spoken) on an A1-C2 scale in English?": language_levels,
    "What is today date?": [],
    "How many years do you have in hardware manufacturing?": [],
    "When can you start working, what is your notice period?": [],
    "By which date (1. of the month) would you want to join Nagarro?": [],
    "Your message to the hiring manager": [],
    "Sind Sie rechtlich befugt, in diesem Land zu arbeiten: Deutschland?": ["Ja", "Nein"],
    "What experience do you have in managing Jenkins and DevOps Tools? The answer must respect this condition: Geben Sie eine decimal Zahl größer als 6.0 ein": [],
    "Wie viele Jahre Berufserfahrung als Frontend Web Entwickler:in bringst Du mit? (bitte Zahl angeben) The answer must respect this condition: Geben Sie eine decimal Zahl größer als 0.0 ein": [],
    "Wie viele Jahre Erfahrung haben Sie mit: Vue.js? The answer must respect this condition: Geben Sie eine whole Zahl zwischen 0 und 99 ein": [],
    "Wie viele Jahre Erfahrung im Bereich Projektmanagement haben Sie?": []
}

# Loop through questions and call answer_question
for question, options in questions_with_options.items():
    print(f"Question: {question}")
    answer = form_filler.answer_question(question, options if options else [])
    print("Answer:", answer)
    print("-" * 50)  # Separator for better readability
