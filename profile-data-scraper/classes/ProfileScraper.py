import pandas as pd
import numpy as np
import configparser
from datetime import datetime
from classes.Helpers import Helpers
from classes.Finders import Finders

config = configparser.ConfigParser()
config.read('config.ini')

# UNLOCKED PROFILE CLASSES
UNLOCKED_POSITIONS_ID = 'profile-positions'
UNLOCKED_EDUCATIONS_ID = 'profile-education'
UNLOCKED_POSITION_CLASS_NAME = 'profile-position'
UNLOCKED_EDUCATION_CLASS_NAME = 'profile-education'
UNLOCKED_SCHOOL_NAME_CNAME = 'profile-education__school-name'
UNLOCKED_DEGREE_CNAME = 'profile-education__degree'
UNLOCKED_FIELD_OF_STUDY_CNAME = 'profile-education__field-of-study'
UNLOCKED_EDUCATION_DATES_CNAME = 'profile-education__dates'

UNLOCKED_POSITION_TITLE_CNAME = 'profile-position__title'
UNLOCKED_POSITION_SECONDARY_TITLE_CNAME = 'profile-position__secondary-title'
UNLOCKED_POSITION_DATES_CNAME = 'profile-position__dates-employed'
UNLOCKED_POSITION_DURATION_CNAME = 'profile-position__duration'
UNLOCKED_POSITION_LOCATION_CNAME = 'profile-position__company-location'

# LOCKED PROFILE CLASSES
LOCKED_SUMMARY_POSITION_CN = 'profile-topcard__summary-position'
LOCKED_TITLE_CNAME = 'profile-topcard__summary-position-title'
LOCKED_DURATION_CNAME = 'profile-topcard__time-period-bullet'
PRESSO = 'presso'
PRESSO_LEN = len(PRESSO)

# CSV
CSV_IMPORT_PATH = 'import/'
CSV_EXPORT_PATH = 'export/'

# COLUMN NAMES
CURRENT_LOCATION = 'current_location'

POSITION_TITLE = 'position_title'
POSITION_COMPANY_NAME = 'position_company_name'
POSITION_DURATION = 'position_duration'
POSITION_DATES = 'position_dates'
POSITION_LOCATION = 'position_location'

EDUCATION_SCHOOL_NAME = 'education_scool_name'
EDUCATION_TITLE = 'education_title'
EDUCATION_DURATION = 'education_duration'
EDUCATION_DEGREE_NAME = 'education_degree_name'
EDUCATION_FIELD_OF_STUDY = 'education_filed_of_study'
EDUCATION_DATES = 'education_dates'

CLMN_LOCKED_PROFILE = 'is_locked_profile'
    
class ProfileScraper:
    # INIT

    def __init__(self, browser):
        print('Initializing Profile Scraper class')
        self.browser = browser

        # Classes
        self.Helpers = Helpers(browser)
        self.Finders = Finders(browser)

        # Global variable initialization
        self.initialize_columns_name()

         # App config
        self.LOCKED_PROFILE_WAIT = int(config['CONFIG']['LOCKED_PROFILE_WAIT'])
        self.UNLOCKED_PROFILE_WAIT = int(config['CONFIG']['UNLOCKED_PROFILE_WAIT'])

    # HELPERS

    def initialize_columns_name(self):
        self.COLUMN_NAME = [CLMN_LOCKED_PROFILE, CURRENT_LOCATION, EDUCATION_SCHOOL_NAME, EDUCATION_TITLE, EDUCATION_DURATION, EDUCATION_DEGREE_NAME, EDUCATION_FIELD_OF_STUDY, EDUCATION_DATES]

        for i in range(1, 5):
            self.COLUMN_NAME.append(POSITION_TITLE + str(i))
            self.COLUMN_NAME.append(POSITION_COMPANY_NAME + str(i))
            self.COLUMN_NAME.append(POSITION_DURATION + str(i))
            self.COLUMN_NAME.append(POSITION_DATES + str(i))
            self.COLUMN_NAME.append(POSITION_LOCATION + str(i))

    def inizialize_global_iteration_variable(self):
        self.initialize_empty_object_to_return()
        self.POS_INDEX = 0

    def initialize_empty_object_to_return(self):
        self.TO_RETURN = {}

        for col_name in self.COLUMN_NAME:
            self.TO_RETURN[col_name] = None

    # CSV
        
    def import_csv(self, name):
        df = pd.read_csv(CSV_IMPORT_PATH + name.strip() + '.csv')
        return df

    def initialize_empty_columns(self, df):
        for col in self.COLUMN_NAME:
            df[col] = np.nan

        return df

    def save_csv(self, df, name):
        df.to_csv(CSV_EXPORT_PATH + name.strip() + '_profiles_' + datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + '.csv', index=False)

    # MAIN

    def scrape_profile(self, df, index):
        entity_cname = 'profile-topcard-person-entity__name'
        el = self.Finders.wait_to_find_element_by_class_name(entity_cname)

        if el is not None:
            cname = 'profile-topcard__summary-link'
            cards = self.Finders.wait_to_find_elements_by_class_name(cname)
            is_profile_locked = self.Helpers.is_profile_blocked(cards)

            if is_profile_locked == 1:
                data_dict = self.scrape_locked_profile()
                self.Helpers.wait_given_time(self.LOCKED_PROFILE_WAIT)
            else:
                data_dict = self.scrape_unlocked_profile()
                self.Helpers.wait_given_time(self.UNLOCKED_PROFILE_WAIT)

            df.loc[index, CLMN_LOCKED_PROFILE] = is_profile_locked

            if data_dict is not None:
                for key in data_dict:
                    if data_dict[key] is not None:
                        df.loc[index, key] = data_dict[key]
        else:
            print('No entity name found. Skipping to next user')
            return None

    # UNLOCKED PROFILE

    def scrape_unlocked_profile(self):
        self.inizialize_global_iteration_variable()
        
        # LOCATION
        location_cname = 'profile-topcard__location-data'
        loc = self.Finders.safe_find_element_by_class_name(location_cname)
        
        if loc is not None: 
            location_text = loc.text
            print('Location: ' + location_text)
            self.TO_RETURN[CURRENT_LOCATION] = location_text
            print('\n')
        
        # POSITIONS
        container = self.Finders.safe_find_element_by_id(UNLOCKED_POSITIONS_ID)
        if container is not None:
            positions = self.Finders.safe_find_elements_by_class_name(UNLOCKED_POSITION_CLASS_NAME, container)
            if positions is not None:
                self.scrape_unlocked_profile_positions(positions)
        
        # EDUCATIONS
        container = self.Finders.safe_find_element_by_id(UNLOCKED_EDUCATIONS_ID)
        if container is not None:
            educations = self.Finders.safe_find_elements_by_class_name(UNLOCKED_EDUCATION_CLASS_NAME, container)
            if educations is not None:
                edu = [educations[0]]
                self.scrape_unlocked_profile_educations(edu)

        return self.TO_RETURN
  
    def scrape_unlocked_profile_educations(self, educations):
        for edu in educations:
            self.Helpers.scroll_to_element_height(edu)
            
            # SCHOOL NAME
            school_name = self.Finders.safe_find_element_by_class_name(UNLOCKED_SCHOOL_NAME_CNAME, edu)
            if school_name is not None:
                school_name_text = self.Helpers.get_string_without_hidden_text(school_name)
                print('School Name: ' + school_name_text)
                self.TO_RETURN[EDUCATION_SCHOOL_NAME] = school_name_text
                
            # DEGREE
            degree = self.Finders.safe_find_element_by_class_name(UNLOCKED_DEGREE_CNAME, edu)
            if degree is not None:
                degree_text = self.Helpers.get_string_without_hidden_text(degree)
                print('Degree Name: ' + degree_text)
                self.TO_RETURN[EDUCATION_DEGREE_NAME] = degree_text
                
            # FIELD OF STUDY
            study = self.Finders.safe_find_element_by_class_name(UNLOCKED_FIELD_OF_STUDY_CNAME, edu)
            if study is not None:
                study_name_text = self.Helpers.get_string_without_hidden_text(study)
                print('Field of study: ' + study_name_text)
                self.TO_RETURN[EDUCATION_FIELD_OF_STUDY] = study_name_text
                
            # EDUCATION DATES
            edu_dates = self.Finders.safe_find_element_by_class_name(UNLOCKED_EDUCATION_DATES_CNAME, edu)
            if edu_dates is not None:
                edu_dates_text = self.Helpers.get_string_without_hidden_text(edu_dates)
                print('Education dates: ' + edu_dates_text)
                self.TO_RETURN[EDUCATION_DATES] = edu_dates_text

    def scrape_unlocked_profile_positions(self, positions):
        for pos in positions:
            self.POS_INDEX += 1
            self.Helpers.scroll_to_element_height(pos)
            
            # MAIN TITLE
            title = self.Finders.safe_find_element_by_class_name(UNLOCKED_POSITION_TITLE_CNAME, pos)
            if title is not None:
                title_text = self.Helpers.get_string_without_hidden_text(title)
                print('Title: ' + title_text)
                key = POSITION_TITLE + str(self.POS_INDEX)
                self.TO_RETURN[key] = title_text
                
            # SECONDARY TITLE
            sec_title = self.Finders.safe_find_element_by_class_name(UNLOCKED_POSITION_SECONDARY_TITLE_CNAME, pos)
            if sec_title is not None:
                sec_title_text = self.Helpers.get_string_without_hidden_text(sec_title)
                print('Secondary Title (Company Name): ' + sec_title_text)
                key = POSITION_COMPANY_NAME + str(self.POS_INDEX)
                self.TO_RETURN[key] = sec_title_text
                
            # DATES
            dates = self.Finders.safe_find_element_by_class_name(UNLOCKED_POSITION_DATES_CNAME, pos)
            if dates is not None:
                dates_text = self.Helpers.get_string_without_hidden_text(dates)
                print('Dates: ' + dates_text)
                key = POSITION_DATES + str(self.POS_INDEX)
                self.TO_RETURN[key] = dates_text
                
            # DURATION
            duration = self.Finders.safe_find_element_by_class_name(UNLOCKED_POSITION_DURATION_CNAME, pos)
            if duration is not None:
                duration_text = self.Helpers.get_string_without_hidden_text(duration)
                print('Duration: ' + duration_text)
                key = POSITION_DURATION + str(self.POS_INDEX)
                self.TO_RETURN[key] = duration_text
                
            # LOCATION
            location = self.Finders.safe_find_element_by_class_name(UNLOCKED_POSITION_LOCATION_CNAME, pos)
            if location is not None:
                location_text = self.Helpers.get_string_without_hidden_text(location)
                print('Location: ' + location_text) 
                key = POSITION_LOCATION + str(self.POS_INDEX)
                self.TO_RETURN[key] = location_text   
            
            print('\n')

    # LOCKED PROFILE
    
    def scrape_locked_profile(self):
        self.inizialize_global_iteration_variable()
        
        # LOCATION
        location_cname = 'profile-topcard__location-data'
        loc = self.Finders.safe_find_element_by_class_name(location_cname)
        
        if loc is not None: 
            location_text = loc.text
            print('Location: ' + location_text)
            self.TO_RETURN[CURRENT_LOCATION] = location_text
            print('\n')
        
        # CURRENT POSITION
        curr_pos_cname = 'profile-topcard__current-positions'
        cp = self.Finders.safe_find_element_by_class_name(curr_pos_cname)
        
        if cp is not None:    
            curr_positions = cp.find_elements_by_class_name(LOCKED_SUMMARY_POSITION_CN)
            self.scrape_summary_position(curr_positions)
        
        # PREVIOUS POSITION
        prev_pos_cname = 'profile-topcard__previous-positions'
        pp = self.Finders.safe_find_element_by_class_name(prev_pos_cname)
        
        if pp is not None:
            prev_positions = pp.find_elements_by_class_name(LOCKED_SUMMARY_POSITION_CN)
            self.scrape_summary_position(prev_positions)
            
            
        # EDUCATION
        education_cname = 'profile-topcard__educations'
        education = self.Finders.safe_find_element_by_class_name(education_cname)
        
        if education is not None:
            educations = education.find_elements_by_class_name(LOCKED_SUMMARY_POSITION_CN)
            edu = [educations[0]] # Prendo solo la prima
            self.scrape_summary_education(edu)

        return self.TO_RETURN

    def scrape_summary_position(self, positions):
        for position in positions:
            self.POS_INDEX += 1
            raw_position_text = position.text
            
            # TITLE
            title = self.Finders.safe_find_element_by_class_name(LOCKED_TITLE_CNAME, position)
            if title is not None:
                title = title.text
                print('Title: ' + title)
                key = POSITION_TITLE + str(self.POS_INDEX)
                self.TO_RETURN[key] = title
                
            # DURATION
            duration = self.Finders.safe_find_element_by_class_name(LOCKED_DURATION_CNAME, position)
            if duration is not None:
                duration = duration.text
                print('Duration: ' + duration)
                key = POSITION_DURATION + str(self.POS_INDEX)
                self.TO_RETURN[key] = duration
                
            presso_index = raw_position_text.index(PRESSO) if PRESSO.lower() in raw_position_text.lower() else None
            if presso_index is not None:
                # Rimuovo tutto cio che c'è prima di "presso"
                company_name = raw_position_text[presso_index + PRESSO_LEN:]

                # COMPANY NAME
                # Se c'è la duration la rimuovo 
                if duration is not None:
                    duration_index = company_name.index(duration)
                    company_name = company_name[:duration_index]

                company_name = company_name.strip()
                print('Company Name: ' + company_name)
                key = POSITION_COMPANY_NAME + str(self.POS_INDEX)
                self.TO_RETURN[key] = company_name
            
            print('\n')

    def scrape_summary_education(self, educations):
        for position in educations:
            raw_position_text = position.text
            school_name = raw_position_text
            
            # TITLE
            title = self.Finders.safe_find_element_by_class_name(LOCKED_TITLE_CNAME, position)
            if title is not None:
                title = title.text
                print('Title: ' + title)
                self.TO_RETURN[EDUCATION_TITLE] = title
                
                # Rimuovo dalla raw string il ruolo (titolo)
                school_name = school_name.replace(title, '')
                
            # DURATION
            duration = self.Finders.safe_find_element_by_class_name(LOCKED_DURATION_CNAME, position)
            if duration is not None:
                duration = duration.text
                print('Duration: ' + duration)
                self.TO_RETURN[EDUCATION_DURATION] = duration
                
                # Rimuovo dalla raw string la duration
                school_name = school_name.replace(duration, '')
            
            # SCHOOL NAME
            # Rimuovo dalla raw string la stringa "presso"
            school_name = school_name.replace('presso', '').strip()
            print('School Name: ' + school_name)
            self.TO_RETURN[EDUCATION_SCHOOL_NAME] = school_name
            
            print('\n')
