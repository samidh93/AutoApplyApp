from chatgpt import ChatGPT
import json
import csv
import re


class emailCompanyGenerator:
    def __init__(self, company:str, location:str):
        self.company = company
        self.location = location
        exclude_patterns = ["ag", "mg", "gmbh","group","inc", "corp", "ltd","-"," ",".", ",","&", "'", "->"]
        self._replaceStrPattern(exclude_patterns)

    def _replaceStrPattern(self, patterns:list)->None:
        for pattern in patterns:
            if pattern in self.company.lower() or pattern in self.company:
                self.company = re.sub(r"(?i)\b" + pattern + r"\b", "", self.company)
                self.company = self.company.replace(pattern, "")
                # Remove special characters and foreign language characters
                self.company = re.sub(r'[^\w\s,.!?]', '', self.company, flags=re.UNICODE)

    @staticmethod
    def get_country_cities_domain(csv_file):
        # Open the CSV file and read the data
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            return [[row[0] for row in reader], [row[4] for row in reader]]

    german_cities = get_country_cities_domain("jobApp/data/de.csv")
    french_cities = get_country_cities_domain("jobApp/data/fr.csv")
    belgien_cities = get_country_cities_domain("jobApp/data/be.csv")
    swiss_cities = get_country_cities_domain("jobApp/data/sw.csv")
    luxemburg_Cities = get_country_cities_domain("jobApp/data/sw.csv")

    def genEmailsViaChatGpt(self) -> list:
        query = f"what is the career or recruiting email of the company {self.company} located in {self.location}. \
        respond in json fromat 'email':'value' if you don't know, try to guess it. i am sure you can\n"
        reply = ChatGPT("jobApp/secrets/openai.json").ask(query)
        print(f"chatgpt replied: {reply}")
        emails = json.loads(reply)
        return emails
    
    def locate_input_location(self,input_location:str,  country:str, list_of_cities:list[str]):
        if input_location.lower()==country or any(city in input_location for city in list_of_cities):
            return True
    
    def generate_emails(self)->list:
        email_list = []
        com = "com"
        if self.locate_input_location(self.location, "france", self.french_cities[0]):
            fr = "fr"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]
            email_list = [
                f"{domain}@{self.company}.{fr}" for domain in email_domains]

        if self.locate_input_location(self.location, "belgium", self.belgien_cities[0]):
            be = "be"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]
            email_list = [
                f"{domain}@{self.company}.{be}" for domain in email_domains]

        if self.locate_input_location(self.location, "switzerland", self.swiss_cities[0]):
            ch = "ch"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]

            email_list = [
                f"{domain}@{self.company}.{ch}" for domain in email_domains]

        if self.locate_input_location(self.location, "luxemburg", self.luxemburg_Cities[0]):
            lu = "lu"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]

            email_list = [
                f"{domain}@{self.company}.{lu}" for domain in email_domains]

        if self.locate_input_location(self.location, "germany", self.german_cities[0]):
            de = "de"
            email_domains = ["recruiting", "karriere", "jobs", "personal",
                             "talent", "bewerbung", "team", "mitarbeiten", "joinus", "chance"]

            email_list = [
                f"{domain}@{self.company}.{de}" for domain in email_domains]

        else:
            email_domains = ["recruiting", "careers", "jobs", "hr", "talentacquisition","career" ,
                             "staffing", "workwithus", "joinourteam", "employment", "opportunities"]
        # append always general emails pattern
        email_list += [
                f"{domain}@{self.company}.{com}" for domain in email_domains]

        return email_list


if __name__ == '__main__':
    emailsgen = emailCompanyGenerator("KWS Group GmbH - gmbh GMBH , ltd", "Paris, france")
    print(emailsgen.generate_emails())
