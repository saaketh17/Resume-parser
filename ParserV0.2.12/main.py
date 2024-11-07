from flask import *
from ParserSample import DocumentReader
import os
from werkzeug.utils import secure_filename
from NLPLoader import ResumeParser
from flask_caching import Cache
import threading
import sys

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

app = Flask(__name__)
cache.init_app(app)


# To check if the parser is working fine.
@app.route('/parserId/<userId>', methods=['GET'])
def success(userId):
    return 'welcome %s' % userId


# To locate the analytics file from the Parser. NOT WORKING.
@app.route('/analytics/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='/Users/sraavanchevireddy/PycharmProjects/AI%20Resume%20Parser/filess',
                               filename=filename)

@app.route('/ExpressParse', methods=['POST'])
def expressParser():
    f = request.files['file']

    # Saving the resume in a local directory
    os.makedirs(os.path.join(app.instance_path, 'Resumes'), exist_ok=True)
    resume_path = os.path.join(app.instance_path, 'Resumes', secure_filename(f.filename))
    f.save(resume_path)

    # Reading and parsing resume
    try:
        resume_text = DocumentReader(resume_path).read_doc()
    except:
        return jsonify(errorMessage="Unable to read the resume format")
    threading.Thread(os.remove(resume_path)).start()

    parser = ResumeParser(resume_text)
    firstName = ""
    lastName = ""

    # Reading the Human names from docToken
    candidateName = parser.extract_humanNames()
    if candidateName:
        firstName = parser.extract_firstName(candidateName)
        lastName = parser.extract_last_name(candidateName)

    # Send the new json format here...
    return jsonify(
        QANotes={
            'firstName': f'{firstName}',
            'lastName': f'{lastName}',
            'resumeFileName': f'{f.filename}',
            'fullName': f'{candidateName}',
            'email': parser.extractEmail(),
            'mobile': f'{parser.extractPhoneNumber()}',
            'address': f'{parser.extract_address()}',
            'country': f'{parser.extract_country()}',
            'state': f'{parser.extract_gpe()}'
        },
        DicomImages=[

        ],
        Activity=[

        ]
    )


# To parse the resume
@app.route('/parse', methods=['POST'])
def parseResume():
    f = request.files['file']

    # Saving the resume in a local directory
    os.makedirs(os.path.join(app.instance_path, 'Resumes'), exist_ok=True)
    resume_path = os.path.join(app.instance_path, 'Resumes', secure_filename(f.filename))
    f.save(resume_path)

    # Reading and parsing resume
    try:
        resume_text = DocumentReader(resume_path).read_doc()
    except:
        return jsonify(errorMessage="Unable to read the resume format")

    threading.Thread(os.remove(resume_path)).start()

    parser = ResumeParser(resume_text)
    firstName = ""
    middleName = ""
    lastName = ""

    # Reading the Human names from docToken
    # candidateName = parser.extract_humanNames()
    # if candidateName:
    #     firstName = parser.extract_firstName(candidateName)
    #     lastName = parser.extract_last_name(candidateName)

    candidateName = parser.extract_humanNames()
    if candidateName:
        candidateName_str = candidateName.text  # Convert Span object to string
        word_list = candidateName_str.split()
        number_of_words = len(word_list)
        if number_of_words >= 3:
            firstName = parser.extract_firstName(candidateName)
            middleName = ""
            lastName = parser.extract_last_name(candidateName)
        else:
            if number_of_words == 1:
                firstName = parser.extract_firstName(candidateName)
            else:
                firstName = parser.extract_firstName(candidateName)
                lastName = parser.extract_last_name(candidateName)



    return jsonify(
        FirstName=f'{firstName}',
        MiddleNmae =f'{middleName}',
        LastName=f'{lastName}',
        ResumeFileName=f'{f.filename}',
        FullName=f'{candidateName}',
        Email=parser.extractEmail(),
        Mobile=f'{parser.extractPhoneNumber()}',
        Skills=f'{parser.extract_skill_set()}',
        linkedinId=f'{parser.extract_linkedin()}',
        VisaStatus=f'{parser.extract_visa_status()}',
        GapPeriod=f'{parser.extract_gap_period()}',
        Experience=f'{parser.extract_date()}',
        State=f'{parser.extract_gpe()}',
        Qualification=f'{parser.extract_qualification()}',
        JobProfile=f'{parser.extract_profession()}',
        EmploymentType=f'{parser.extract_employment_type()}',
        certifications=f'{parser.extract_certification()}',
        Address=f'{parser.extract_address()}',
        currentEmployer=f'{parser.extract_current_employer()}',
        Country=f'{parser.extract_country()}',
        Phone=f'{parser.extract_phone()}',
        City=f'{parser.extract_city()}',
        PinCode = f'{parser.extract_postalCode()}'
    )

# To parse the resume
@app.route('/bulkParse', methods=['POST'])
def bulkParse():
    f = request.files['file']

    # Saving the resume in a local directory
    os.makedirs(os.path.join(app.instance_path, 'BulkFolder'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, 'Responses'), exist_ok=True)

    resume_path = os.path.join(app.instance_path, 'BulkFolder', secure_filename(f.filename))
    destination = os.path.join(app.instance_path, 'BulkFolder', '12132021')
    response_path = os.path.join(app.instance_path, 'Responses', '12132021.json')

    f.save(resume_path)

    try:
        with zipfile.ZipFile(resume_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
    except:
        return jsonify(errorMessage="You should grow UP!! ")

    threading.Thread(os.remove(resume_path)).start()
    bulkFiles = os.listdir(destination)

    for eachFile in bulkFiles:
        va = os.path.join(destination, eachFile)
        print(f'This is something {va}')
        try:
            resume_text = DocumentReader(va).read_doc()
            write_data(response_path, parseValues(resume_text))
        except:
            print('Skipping file!')
            continue

    return jsonify(True)


if __name__ == '__main__':
    app.run(port='4432')
