from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from .jobsAttachSessionToLoginLinkedin import JobSearchRequestSessionAttachLinkedin
from .linkedinSeleniumBase import LinkedinSeleniumBase

''' handle linkedin easy apply form template'''

class LinkedInEasyApplyFormHandler:
    def __init__(self, candidate_profile: CandidateProfile, csv_jobs='jobApp/data/jobs.csv', linkedin_data_file = 'jobApp/secrets/linkedin.json'):
        self.csv_file = csv_jobs
        self.links = self.load_links_from_csv()
        # only for debugging, split login and apply in sesssions, keep login session open
        #login = JobSearchRequestSessionAttachLinkedin(linkedin_data_file)
        #bot = login.createJobSearchRequestSession()
        #self.driver = bot.driver  # pass the new driver to current one
        self.linkedinObj = LinkedinSeleniumBase(linkedin_data_file)
        self.driver = self.linkedinObj.login_linkedin()
        self.label_elements_map = {}
        self.candidate = candidate_profile
        self.button_apply_clicked = False

    def load_links_from_csv(self):
        # load only onsite links
        links = []  # list of intern lists
        if os.path.isfile(self.csv_file):
            print("loading links from input jobs file: ", self.csv_file)
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    links.append(row[2])  # intern links
        self.links = links
        print(f"onsite apply links count: {len(links)}")

    ###### get url in browser #######
    def get_the_url(self, url=None):
        # navigate to the URL
        try:  # try to open link in browser
            self.driver.get(url)
        except:
            print("can't open link in the browser")
            self.status = False

    ###### find application form #########
    def _find_application_form(self):
      # fill the expected first page template
        try:
            self.div_element_form_holder = self.driver.find_element(
                By.CSS_SELECTOR, 'div.artdeco-modal.artdeco-modal--layer-default.jobs-easy-apply-modal')
            if self.div_element_form_holder:
                # Find the form element within the div
                form_element = self.div_element_form_holder.find_element(
                    By.TAG_NAME, 'form')
                if form_element:
                    #print(f"form_element found: form object {form_element}")
                    self.form = form_element  # pass the form to parent
                else:
                    # The form element was not found within the div
                    print('Form element not found')
            else:
                # The div element was not found
                print('Div element not found')
        except:
            print("no page found")

#########################################################################

    def send_value(self, element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "file":
            print(f"sending file path: {value}")
            element.send_keys(value)
        elif element_type == "text":
            element.clear()
            element.send_keys(value)
        else:
            print("input type not recognized")

    def click_option(self, element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "radio":
            for elem in element:
                if elem == value:
                    elem.click()
        elif element_type == "checkbox":
            for elem in element:
                if elem == value:
                    elem.click()

    def select_option(self, select_element, user_value):
        select = Select(select_element)
        if isinstance(select.options, Iterable):
            if user_value in select.options:
                select.select_by_visible_text(user_value)
            else:  # return first option to bypass error; needed to be corrected
                select.select_by_visible_text(
                    select.first_selected_option.accessible_name)
            return
        else:
            select.select_by_visible_text(select.first_selected_option.text)


    def _createDictFromFormDiv(self, divs:  list[WebElement]):
        # Iterate over the divs and extract the label and corresponding input/select values
        for div in divs:
            fieldset = self._find_fieldset_tag(div)
            if fieldset is not None:
                # we have a set of fields (dialog or checkbox)
                span_text = self._find_span_text(fieldset)
                inputs_elems = self._find_input_options_tag(fieldset, span_text.text)
                print(f"added field element with label: {span_text}")
                self.label_elements_map[span_text.text] = inputs_elems
            # search for label w
            else:
                label = self._find_label_tag(div)
                if label is not None:
                    input_elem = self._find_input_tag(div, label)
                    # text field
                    if input_elem is not None:
                        print(f"added input element with label: {label}")
                        self.label_elements_map[label] = input_elem
                    # search for select options
                    else:
                        select_elem = self._find_select_tag(div, label)     
                        if select_elem is not None:
                            print(f"added select element with label: {label}")
                            self.label_elements_map[label] = select_elem

    ########## fill form page ###########
    def fillFormPage(self):
        header = self._find_header(self.form)
        if header == "Contact info" or header == "Kontaktinfo":
            return self._fill_contact_info(self.form)
            #self.label_elements_map.clear()
        elif header == "Resume" or header == "Lebenslauf":
            return self._fill_resume(self.form)
            #self.label_elements_map.clear()
        elif header == "Additional" or header == "Additional Questions" or header == "Weitere Fragen":
            print("filling additional questions")
            return self._fill_additionals(self.form)
            #self.label_elements_map.clear()
        else:
            print("page header no recognized")

    ####### Click Button Apply #########
    def clickApplyPage(self):
        # click on the easy apply button, skip if already applied to the position
        try:
            print("try clicking button easy apply")
            # Wait for the button element to be clickable
            button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            # button = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")
            button.click()
            self.button_apply_clicked = True
            print("button apply clicked")
        # if already applied or not found
        except:
            print('easy apply job button is not found, skipping')
            self.status = False

    ########### Detect PAge #############
    def _detect_form_page_type(self, form: WebElement, start_time=None):
        if start_time is None:
            start_time = time.time()  # Record the start time
        elapsed_time = time.time() - start_time  # Calculate elapsed time in seconds
        if elapsed_time >= 180:  # 180 seconds = 3 minutes
            print("Time limit (3 minutes) exceeded. Returning from applyForJob.")
            return False
        # detect if the current page has next, review or submit 
        if self._detectSubmitButtonForm(form): # only submit
            print("page form with submit detected")
            return self._execute_submit(form)
        elif self._detectReviewButtonForm(form): # recursive one
            print("page form with review detected")
            self._execute_review(form)
            return self._detect_form_page_type(form,start_time)
        elif self._detectNextButtonForm(form): # recursive many
            print("page form with next detected")
            self._execute_next(form)
            return self._detect_form_page_type(form,start_time)

    ####### Apply Phase #####
    def applyForJob(self, job_link: str) -> bool:
        # keep track of the time for application, do not exceed max 3 minutes:
        start_time = time.time() # begin counter
        elapsed_time = time.time() - start_time  # Calculate elapsed time in seconds
        if elapsed_time >= 180:  # 180 seconds = 3 minutes
            print("Time limit (3 minutes) per application exceeded. Returning from applyForJob.")
            return False
        # open job url
        self.get_the_url(job_link)  # get the url form the job
        # return true if job was success or already applied, false if job not found, deleted or can't apply
        if self.applicationSubmitted():
            return True
        self.clickApplyPage()  # try to click apply button: retry when not clicked
        if not self.button_apply_clicked:
            self.clickApplyPage()
        if not self.button_apply_clicked:
            return False
        # detect form page type: 
        self._find_application_form()  # try to find the form
        if not self._detect_form_page_type(self.form, start_time):
            return False
        self.button_apply_clicked = False
        return True
    
    def applicationSubmitted(self)->bool :
        # click on the easy apply button, skip if already applied to the position
        try:
            # Wait for the timeline entries to load
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-apply-timeline__entity')))
            timeline_entries = self.driver.find_elements(By.CLASS_NAME, 'post-apply-timeline__entity')
            for entry in timeline_entries:
                activity_text = entry.find_element(By.CLASS_NAME, 'full-width').text.strip()
                if activity_text == 'Application submitted':
                    print("application already submitted, skipping ..")
                    #time.sleep(1)
                    return True
        except:
            return False

    def is_applications_closed(self):
        try:
            # Wait for the error element to load
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-details-top-card__apply-error')))
            error_element = self.driver.find_element(By.CLASS_NAME, 'jobs-details-top-card__apply-error')
            error_message = error_element.find_element(By.CLASS_NAME, 'artdeco-inline-feedback__message').text.strip()
            if "No longer accepting applications" in error_message:
                print("application closed, no longer accepting applicants")
                return True
        except:
            return False

if __name__ == '__main__':
    pass
