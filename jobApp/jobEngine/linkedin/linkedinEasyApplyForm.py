from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
import os
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from .jobsAttachSessionToLoginLinkedin import JobSearchRequestSessionAttachLinkedin
import time
''' handle linkedin easy apply form template'''

class LinkedInEasyApplyFormHandler:
    def __init__(self, candidate_profile: CandidateProfile, csv_links='jobApp/data/links.csv', linkedin_data_file = 'jobApp/secrets/linkedin.json'):
        self.links = []
        self.csv_file = csv_links
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()
        login = JobSearchRequestSessionAttachLinkedin(linkedin_data_file,  headless=False)
        bot = login.createJobSearchRequestSession()
        self.driver = bot.driver  # pass the new driver to current one
        self.label_elements_map = {}
        self.candidate = candidate_profile
        self.button_apply_clicked = False

    def load_links_from_csv(self):
        # load only onsite links
        links = []  # list of intern lists
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    if row[5] == "None":  # append only easy apply links
                        links.append(row[4])  # intern links
        self.links = links
        print(f"onsite apply links count: {len(links)}")

    def get_the_url(self, url=None):
        # navigate to the URL
        try:  # try to open link in browser
            self.driver.get(url)
        except:
            print("can't open link in the browser")
            self.status = False

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
    #### user details section ######
    def _send_user_contact_infos(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        for label, element in elements_dict.items():
            if label == 'First name':
                self.send_value(element, user.firstname)
            elif label == 'Last name':
                self.send_value(element, user.lastname)
            elif 'Phone country code' in label:
                self.select_option(element, user.phone_code)
            elif label == 'Mobile phone number':
                self.send_value(element, user.phone_number)
            elif 'Email address' in label:
                self.select_option(element, user.email)
            else:
                raise ValueError("Unsupported label: {}".format(label))

    def _send_user_documents(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        for label, element in elements_dict.items():
            if label == 'Upload resume':
                self.send_value(element, user.resume.file_path)
            elif label == "Upload cover letter": # ignore cover letter: need specification later
                pass
            else:
                raise ValueError("Unsupported label: {}".format(label))

    def _send_user_answers(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        # try to answer most form questions
        for label, element in elements_dict.items():
            if isinstance(element, list):
                print("The element is of type list.")
                if element[0].get_attribute("type") == "radio":
                    #handle dialog questions
                    self._handle_dialog_question(label , element)
                elif element[0].get_attribute("type") == "checkbox":
                    #handle dialog questions
                    self._handle_checkbox_question(label , element)
            elif element.get_attribute("type") == "text":
                # handle text based questions
                self._handle_text_question(label, element)
            else:
                #handle dialog questions
                self._handle_select_question(label , element)

    def _handle_text_question(self, label, element: WebElement ):
        try:
            print("processing text question")
            if "salary" in label:
                self.send_value(element, self.candidate.salary)
            if "Erfahrung" or "Experience" in label:
                self.send_value(element, self.candidate.years_exp)
        except:
            pass 
    def _handle_dialog_question(self, label, element: WebElement ):
        try:
            print("processing dialog question")
            input_options = element.find_elements(By.TAG_NAME, "input")
            for opt in input_options:
                print("option: ", opt)
                if opt.get_attribute("value") == "Yes":
                    opt.click()
        except:
            pass 
    def _handle_select_question(self, label, element: WebElement ):
        try:
            print("processing select question")
            dropdown = Select(element)
            # Get the number of options in the dropdown
            options_count = len(dropdown.options)
            # Calculate the index of the middle option
            middle_index = options_count // 2
            # Select the option in the middle by index
            dropdown.select_by_index(options_count-1)
        except:
            pass 
    def _handle_checkbox_question(self, label , elements: WebElement):
        try:
            print("checkbox question")
            options_count = len(elements)
            middle_index = options_count // 2
            # random value in the middle
            checkbox = elements[options_count-1]
            # Find the associated label using its attributes (for or id) or relationship (preceding-sibling, following-sibling, etc.)
            label = checkbox.find_element(By.XPATH, "//label[@for='" + checkbox.get_attribute("id") + "']")
            if not label.is_selected():
                label.click()  # Click the label to interact with the checkbox
                print("Label clicked successfully.")
        except Exception as e:
            print("An error occurred:", e)
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

    def _find_divs_document_upload(self) -> list[WebElement]:
        if self.form != None:  # if form is found
            try:
                div_elements = self.form.find_elements(
                    By.XPATH, "//div[contains(@class, 'js-jobs-document-upload__container') and contains(@class, 'display-flex') and contains(@class, 'flex-wrap')]")
                return div_elements
            except NoSuchElementException:
                print("No upload elements found")

    def _find_divs_selection_grouping(self) -> list[WebElement]:
        if self.form != None:  # if form is found
            try:
                # Find the div with class "jobs-easy-apply-form-section__grouping"
                divs = self.form.find_elements(
                    By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
                print("found divs with selection grouping")
                return divs
            except NoSuchElementException:
                print("No div elements found")

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

    def _find_fieldset_tag(self, element: WebElement):
        try: 
            fieldset_element = element.find_element(By.TAG_NAME, 'fieldset')
            print(f"Fieldset: {fieldset_element.text}")
            return fieldset_element
            #print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("fieldset element not found.") 

    def _find_span_text(self, element: WebElement):
        try: 
            span_element = element.find_element(By.TAG_NAME, 'span')
            span_element.text.strip()
            return span_element
            #print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("no span element not found.")   

    def _find_input_options_tag(self, element: WebElement, label=None):
        try:
            # Attempt to find the 'input' element inside the 'div' element
            input_elements = element.find_elements(By.TAG_NAME, 'input')
            #print(f"Input Value: {value}")
            return input_elements
        except NoSuchElementException:
            # Handle the case when 'input' element is not found
            print("Input elements not found.")
            
    def _find_label_tag(self, element: WebElement):
        try: 
            label_element = element.find_element(By.TAG_NAME, 'label')
            label = label_element.text.strip()
            return label
            #print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("no label element not found.")       

    def _find_input_tag(self, element: WebElement, label=None):
        try:
            # Attempt to find the 'input' element inside the 'div' element
            input_element = element.find_element(By.TAG_NAME, 'input')
            value = input_element.get_attribute('value').strip()
            #print(f"Input Value: {value}")
            return input_element
        except NoSuchElementException:
            # Handle the case when 'input' element is not found
            print("Input element not found.")

    def _find_select_tag(self, element: WebElement, label=None):
        try:
             # Attempt to find the 'select' element inside the 'div' element
             select_element = element.find_element(By.TAG_NAME, 'select')
             # Create a Select object
             select = Select(select_element)
             # assign label with select element object
             selected_option = select.options
             return select_element
             # outside function
             self.label_elements_map[label] = select_element
        except NoSuchElementException:
             # Handle the case when 'select' element is not found
             print("Select element not found.")

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
    def _fill_contact_info(self, form: WebElement):
        #self._find_application_form()  # try to find the form
        try:
            divs = self._find_divs_selection_grouping()
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                self._createDictFromFormDiv(divs)
                # fill the form with candidate data
                self._send_user_contact_infos(self.candidate, self.label_elements_map)
                # click next buttton
                self.label_elements_map.clear()
        except:
            print("no contact infos to fill")
    ###
    def _fill_resume(self, form: WebElement):
        self.label_elements_map.clear()
        try:
            divs = self._find_divs_document_upload()
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                self._createDictFromFormDiv(divs)
                # fill the form with candidate data
                self._send_user_documents(self.candidate, self.label_elements_map)
                # click next buttton
                self.label_elements_map.clear()

        except:
            print("no resume to fill")
    
    ####
    def _fill_additionals(self, form: WebElement):
        #self._find_application_form()  # try to find the form
        try:
            divs = self._find_divs_selection_grouping()
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                self._createDictFromFormDiv(divs)
                # fill the form with candidate data
                self._send_user_answers(self.candidate, self.label_elements_map)
                # click next buttton
                self.label_elements_map.clear()
        except Exception as e:
            print("catched error while filling additional questions", e)
    ######## find hear ####
    def _find_header(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            h3_element = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold')
            # Print the inner text of the element.
            print(f"page header: {h3_element.text}")
            return h3_element.text
        except:
            print("no header found")
            return "NA"
    ####### Click Buttons Pages #########
    def clickApplyPage(self):
        # click on the easy apply button, skip if already applied to the position
        try:
            print("try clicking button easy apply")
            # Wait for the button element to be clickable
            button = WebDriverWait(self.driver, 10).until(
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

    def _clickNextPage(self, form: WebElement):
        # click the next page button
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Next']")
            # Click the button
            button.click()
            self.nextClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("next button element not found.")
            self.nextClicked = False
            return False
    def _clickReviewPage(self, form: WebElement):
        # click the review page button
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Review']")
            # Click the button
            button.click()
            self.ReviewClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Review button element not found.")
            self.ReviewClicked = False
            return False
    def _clickSubmitPage(self, form: WebElement):
        # click the submit page button
        # Find the button using its aria-label attribute
        try:
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit application']")))
            # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            self.SubmitClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Submit button element not found.")
            self.SubmitClicked = False
            return False
    ########### Detect PAge #############
    def _detectNextButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Next']")
            return True
        except :            
            # Handle the case when 'next' element is not found
            print("next button element not found.")
            return False
    def _detectReviewButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Review']")
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Review button element not found.")
            return False
    def _detectSubmitButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            #button = form.find_element(By.XPATH, "//span[text()='Submit application']")
            # Wait for the button to be clickable or visible
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit application']")))
            # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Submit button element not found.")
            return False
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


    ########### each case func ########
    def _execute_submit(self, form:WebElement):
        # on page submit execute
        return self._clickSubmitPage(form)
    def _execute_review(self, form:WebElement):
        current_header = self._find_header(form)
        # click review, if header is same, try filling the page if is not filled
        self._clickReviewPage(form)
        last_header = self._find_header(form)
        if last_header != current_header:
            # we skipped page
            return
            # on page review execute
        self.fillFormPage()
        # return button clicker
        return self._clickReviewPage(form)

    def _execute_next(self, form:WebElement): # this 90% of the cases 
        current_header = self._find_header(form)
        # click review, if header is same, try filling the page if is not filled
        self._clickNextPage(form)
        last_header = self._find_header(form)
        if last_header != current_header:
            # we skipped page
            return
        # on page next execute
        self.fillFormPage()
        # return button clicker
        return self._clickNextPage(form)

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
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-apply-timeline__entity')))
            timeline_entries = self.driver.find_elements(By.CLASS_NAME, 'post-apply-timeline__entity')
            for entry in timeline_entries:
                activity_text = entry.find_element(By.CLASS_NAME, 'full-width').text.strip()
                if activity_text == 'Application submitted':
                    print("application already submitted, skipping ..")
                    time.sleep(1)
                    return True
        except:
            return False

    def is_applications_closed(self):
        try:
            # Wait for the error element to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-details-top-card__apply-error')))
            error_element = self.driver.find_element(By.CLASS_NAME, 'jobs-details-top-card__apply-error')
            error_message = error_element.find_element(By.CLASS_NAME, 'artdeco-inline-feedback__message').text.strip()
            if "No longer accepting applications" in error_message:
                print("application closed, no longer accepting applicants")
                return True
        except:
            return False

if __name__ == '__main__':
    pass
