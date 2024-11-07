import re

from ParserSample import DocumentReader
from extractor import *
from guessor.DateGuessor import *
import uuid

class ResumeParser:

    def __init__(self, fromText):
        self.fromText = fromText
        self.docToken = nlp(fromText)

        self.final_doc_token = final_nlp(fromText)
        self.real_token = pretrained_nlp(fromText)
        self.fallback_token = fallback_nlp(fromText)
        self.allInToken = allInNlp(self.fromText)

    def extractEmail(self):
        matcher = Matcher(nlp.vocab, validate=True)
        matcher.add("Email", [emailPattern])
        matches = matcher(self.docToken)

        if not matches:
            email = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',self.fromText)
            if email:
                return str(email[0]).replace("-","")
            else: return ""

        for matchID, start, end in matches:
            span = self.docToken[start:end]
            return str(span.text).replace("-", '')

    def extract_date(self):
        return self.extract_experience()
        # if date and 'years' not in str(date[0]):
        #     return self.extract_experience()
        # else: return date[0]

    def extract_experience(self):
        project_dates = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'GAP']
        exp = calculate_exp_years(project_dates)
        exp = "{:.1f}".format(exp/365)
        return exp

    def extract_gpe(self):
        matches = state_matcher(self.docToken)
        if not matches: return ""
        for matchID, start, end in matches:
            span = self.docToken[start:end]
            if span.text is not None:
                return span.text


    def extractPhoneNumber(self):
        matcher = Matcher(nlp.vocab, validate=True)

        matcher.add("PhoneNumber", None, usaRegexPattern, usaPatternOne,usaPatternTwo,indianPattern)
        matches = matcher(self.docToken)
        if not matches: return ""

        for matchID, start, end in matches:
            span = self.docToken[start:end]
            return span.text

    def extract_profession(self):
        designation = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'ROLE']
        if designation: return designation[0]
        else:
            profession_doc_token = profession_nlp(self.fromText)
            pesi = [ee for ee in profession_doc_token.ents if ee.label_.upper() == 'JOB_TITLE']
            if pesi: return pesi[0]
            else: return ""

    def extract_visa_status(self):
        matcher = Matcher(nlp.vocab, validate=True)
        matcher.add("greenCard", None, green_card_pattern, usa_citizen_pattern, green_card_pattern_one, h_one_b, opt,
                    cpt, h_four_ead, ead, h_one)
        matches = matcher(self.docToken)
        if not matches : return ""

        for matchID, start, end in matches:
            span = self.docToken[start:end]
            if str(span.text).casefold() == 'h1'.casefold():
                return "H1B"
            return span.text

    def extract_skill_set(self):
        gpe = [ee for ee in self.final_doc_token.ents if ee.label_.upper() == 'SKILLSET']

        if gpe:
            return ",".join(map(str, gpe))

    def extract_money(self):
        money = [ee for ee in self.docToken.ents if ee.label_ == 'MONEY']
        return money

    def extract_humanNames(self):
        people = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'PERSON']
        if people:
            return people[0]
        else: return ""


    def extract_firstName(self, from_human_name):
        return str(from_human_name).split()[0]

    def extract_middleName(self, from_human_name):
        return str(from_human_name).split()[1]

    def extract_last_name(self, from_human_name):
        try:
            return str(from_human_name).split()[-1]
        except:
            return ""


    def extract_postalCode(self):
        r = re.compile(r'[0-9]{5,6}')
        return r.findall(self.fromText)


    def extract_linkedin(self):
        return ""

    def extract_qualification(self):
        qualification = [ee for ee in self.real_token.ents if
                         ee.label_.upper() == 'ACADEMIC']
        if qualification:
            return ",".join(map(str, qualification))
        else: return ""

    def extract_gap_period(self):
        gap_period = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'GAP']
        gap = guess_date_format(gap_period)
        if gap:
            return int(gap)
        return 0

    def extract_certification(self):
        certification = [ee for ee in self.real_token.ents if
                         ee.label_.upper() == 'CERTIFICATION']
        if certification:
            return certification
        else:
            return ""


    def extract_employment_type(self):
        matches = employment_matcher(self.docToken)
        if not matches: return ""

        for matchID, start, end in matches:
            span = self.docToken[start:end]
            return span.text

    # def extract_address(self):
    #     address = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'ADDRESS']
    #     if address:
    #         return address[0]
    #     else:
    #         address = [ee for ee in self.fallback_token.ents if ee.label_.upper() == 'ADDRESS']
    #         if address: return address[0]
    #     return ""


    def extract_address(self):
        address = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'ADDRESS']
        if address:
            # Remove the text after the vertical bar (|) if present
            address_text = address[0].text.split("|")[0].strip()
            return address_text

        address = [ee for ee in self.fallback_token.ents if ee.label_.upper() == 'ADDRESS']
        if address:
            # Remove the text after the vertical bar (|) if present
            address_text = address[0].text.split("|")[0].strip()
            return address_text

        return ""


    def extract_current_employer(self):
        currentEmp = [ee for ee in self.allInToken.ents if ee.label_.upper() == 'CURRENT_EMPLOYER']
        if currentEmp:
            return currentEmp[0]
        else: return ""


    #Checks for country in the extracted address
    def extract_country(self):
        address = self.extract_address()  # Get the address from extract_address function

        # Regular expression pattern to match country names
        country_pattern = r'\b(?:' + '|'.join(countries) + r')\b'

        # Search for the country pattern in the address
        match = re.search(country_pattern, address, flags=re.IGNORECASE)
        if match:
            return match.group()

        return ''

    def extract_phone(self):
        return ""

    # def extract_city(self):
    #     text = self.allInToken.text
    #     pattern = r"\b(?:{})\b".format("|".join(states))
    #     matches = re.findall(pattern, text, flags=re.IGNORECASE)
    #
    #     if matches:
    #         return matches[0]
    #     else:
    #         return ''

    def extract_city(self):
        return ''

    def generate_uuid(self):
        return str(uuid.uuid3)

# parser = DocumentReader(r"D:\downloads\bulkparse_1\success_1183\253_1646244367Shreya_Sinha_Python_Developer.docx")
# docTxt = parser.read_doc()
# print(docTxt)
# cl = ResumeParser(docTxt)
# print(cl.extract_address())
# print(cl.extract_city())
# print(cl.extract_middleName(from_human_name=cl.extract_humanNames()))
# print(cl.extract_middleName(from_human_name=cl.extract_humanNames()))



