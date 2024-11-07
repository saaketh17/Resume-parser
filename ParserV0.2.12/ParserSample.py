import subprocess

import docx2txt as dst
import textract
import os
import re
import sys, fitz
from tqdm import tqdm
from striprtf.striprtf import rtf_to_text


# fileManager = ExcelFileCreator.ExcelCreator('parsedCandidates.xlsx')
# fileManager.createFile()


class DocumentReader:

    def __init__(self, readFromPath):
        self.readFromPath = readFromPath

    def read_doc(self):
        try:
            # if self.readFromPath.endswith('.pdf'):
            if self.readFromPath.endswith('.pdf') or self.readFromPath.endswith('.PDF'):
                doc = fitz.open(self.readFromPath)
                text = ""
                for page in doc:
                    text = text + str(page.getText())
                tx = " ".join(text.split('\n'))
                tx = re.sub(r' |♦|\t{1,}| {3,}||‍', ' ', tx)
                tx = re.sub(r'\r', '', tx)
                return tx
            # elif self.readFromPath.endswith('.docx'):
            elif self.readFromPath.endswith('.docx') or self.readFromPath.endswith('.DOCX'):
                resumeText = dst.process(self.readFromPath)
                resumeText = " ".join(resumeText.split('\n'))
                resumeText = re.sub(r' |♦|\t{1,}| {3,}||‍', ' ', resumeText)
                resumeText = re.sub(r'\r', '', resumeText)
                return resumeText
            elif self.readFromPath.endswith('.doc') or self.readFromPath.endswith('.DOC'):
                os.environ['ANTIWORDHOME'] = './antiword'
                resumeText = textract.process(self.readFromPath,extension='doc').decode('utf-8')
                resumeText = " ".join(resumeText.split('\n'))
                resumeText = re.sub(r' |♦|\t{1,}| {3,}||‍', ' ', resumeText)
                resumeText = re.sub(r'\r', '', resumeText)
                return resumeText
            elif self.readFromPath.endswith('.rtf'):
                # resumeText = textract.process(self.readFromPath, extension='rtf').decode('utf-8')
                # resumeText = " ".join(resumeText.split('\n'))
                # resumeText = re.sub(r' |♦|\t{1,}| {3,}||‍', ' ', resumeText)
                # return resumeText
                with open(self.readFromPath) as infile:  #--> Changes made to read and extract .rtf folder
                    content = infile.read()
                    resumeText = rtf_to_text(content)
                    resumeText = " ".join(resumeText.split('\n'))
                    resumeText = re.sub(r' |♦|\t{1,}| {3,}||‍', ' ', resumeText)
                    resumeText = re.sub(r'\r', '', resumeText)
                return resumeText


        except Exception as e:
            print(f'{self.readFromPath} is not a valid resume' + str(e))
            return ""

    def create_training_data(self,fromPath):
        f = open("ResumeTrainingPhaseTwo.txt", "w+")
        i = 0
        for each_resume in tqdm(os.listdir(fromPath)):
            i += 1
            print(each_resume)
            if i < 600:
                parser = DocumentReader(
                    fromPath+'/' + each_resume)
                try:
                    resume_text = parser.read_doc()
                    if resume_text is None:
                        print('hi')
                    else:
                        f.write('\n')
                        f.write(resume_text)
                except:
                    print("cant do this")
            else:
                exit('ENDING IT')
        f.close()



# DocumentReader('').create_training_data('/Users/sraavanchevireddy/Downloads/500 Resumes')

# # /Users/sraavanchevireddy/Downloads/Resumes/
# # /Users/sraavanchevireddy/Desktop/Resumes/Training Data/
# /Users/sraavanchevireddy/Downloads/FilesforResumeParser/Candidate

#



#     print(each_resume)
#     emailAddress = nerd.extractEmail(resume_text)
#     phoneNumber = nerd.extractPhoneNumber(resume_text)
#     name = nerd.extract_humanNames(resume_text)
#     state = nerd.extract_gpe(resume_text)
#     postalCode = nerd.extract_postalCode(resume_text)
#     linkedin = nerd.extract_linkedin(resume_text)
#     skills = nerd.extract_skill_set(resume_text)
#     profession = nerd.extract_profession(resume_text)
#     date = nerd.extract_date(resume_text)
#     money = nerd.extract_money(resume_text)
#     visa = nerd.extract_visa_status(resume_text)
#     qualification = nerd.extract_qualification(resume_text)
#     gapPeriod = nerd.extract_gap_period(resume_text)
#
#     print(f'Qualification is {qualification}')
#     fileManager.save(f'{name}', f'{emailAddress}', f'{phoneNumber}', f'{postalCode}', f'{linkedin}', f'{skills}',
#                      f'{visa}', f'{profession}', f'{date}', f'{qualification}',f'{gapPeriod}')


