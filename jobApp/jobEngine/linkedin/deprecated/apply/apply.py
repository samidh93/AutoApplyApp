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