from jobApp.jobEngine.ai.formFiller import FormFiller
from dotenv import load_dotenv
import os
from jobApp.jobEngine.job.job import Job

load_dotenv()
form_filler = FormFiller()
# fill job obj with random data
job = Job(
    id=None,
    job_id=None,
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

# Dictionary to associate questions with their options
questions_with_options = {
    "What is your language proficiency (written/spoken) on an A1-C2 scale in German?": language_levels,
    "What is your language proficiency (written/spoken) on an A1-C2 scale in English?": language_levels,
    "What is today date?": [],
    "How many years do you have in hardware manufacturing?": [],
    "When can you start working, what is your notice period?": [],
    "By which date (1. of the month) would you want to join Nagarro?": [],
    "What are your salary expectations? (EUR)": [],
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
