from chatgpt import ChatGPT
import json
import csv


class emailCompanyGenerator:
    def __init__(self, company, location):
        self.company = company
        self.location = location

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

    def generate_emails(self)->list:
        email_list = []
        com = "com"
        if self.location in self.french_cities[0]:
            fr = "fr"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]
            email_list = [
                f"{domain}@{self.company}.{fr}" for domain in email_domains]

        elif self.location in self.belgien_cities[0]:
            be = "be"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]
            email_list = [
                f"{domain}@{self.company}.{be}" for domain in email_domains]

        elif self.location in self.swiss_cities[0]:
            ch = "ch"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]

            email_list = [
                f"{domain}@{self.company}.{ch}" for domain in email_domains]

        elif self.location in self.luxemburg_Cities[0]:
            lu = "lu"
            email_domains = ["recrutement", "carrieres", "emplois", "rh", "talents", "embauche",
                             "equipe", "travailleravecnous", "rejoigneznotreequipe", "opportunites"]

            email_list = [
                f"{domain}@{self.company}.{lu}" for domain in email_domains]

        elif self.location in self.german_cities[0]:
            de = "de"
            email_domains = ["recruiting", "karriere", "jobs", "personal",
                             "talent", "bewerbung", "team", "mitarbeiten", "joinus", "chance"]

            email_list = [
                f"{domain}@{self.company}.{de}" for domain in email_domains]

        else:
            email_domains = ["recruiting", "careers", "jobs", "hr", "talentacquisition",
                             "staffing", "workwithus", "joinourteam", "employment", "opportunities"]
            email_list += [
                f"{domain}@{self.company}.{com}" for domain in email_domains]

        return email_list


if __name__ == '__main__':
    emailsgen = emailCompanyGenerator("luxoft", "Brussels")
    print(emailsgen.generate_emails())
