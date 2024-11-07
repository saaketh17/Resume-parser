import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

state_matcher = Matcher(nlp.vocab, validate=True)
profession_matcher = Matcher(nlp.vocab, validate=True)
employment_matcher = Matcher(nlp.vocab, validate=True)
skills_matcher = Matcher(nlp.vocab, validate=True)

profession_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\profession_model_training')
gap_period_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\gap_period_model')
final_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\final_model_training')  # WORKING 100% for Skill.
pretrained_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\mondayModel')  # Trained with Spacy Pretrained PERSON and ACADEMIC entities
real_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\tuesdayModel') # Names and Addresses
fallback_nlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\tuesdayModelT')

allInNlp = spacy.load(r'C:\Users\saaketh\Desktop\intern project\ParserV0.2.12\extractor\ThuNERModel') # Person, Address, CurrentEmp, Gap


# Visa Status Patterns
green_card_pattern = [{"LOWER": "green"}, {"LOWER": "card"}, {"LOWER": "holder"}]
green_card_pattern_one = [{"TEXT": "GC"}]
usa_citizen_pattern = [{"LOWER": "usa"}, {"LOWER": "citizen"}]
h_one_b = [{"LOWER": "h1b"}]
opt = [{"TEXT": "OPT"}]
cpt = [{"TEXT": "CPT"}]
h_four_ead = [{"LOWER": "h4-ead"}]
ead = [{"TEXT": "ead"}]
h_one = [{"LOWER": "h1"}]

# +1-(609)-789-9773
# (214) 984-8166
emailPattern = [{"LIKE_EMAIL": True}]

usaRegexPattern = [
    {"TEXT": {"REGEX": r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}}
]

usaPatternOne = [ #+1-123-456-7890
    {"ORTH": "+1","OP":"?"},
    {"TEXT":"-","OP":"?"},
    {"SHAPE": "ddd"},
    {"TEXT": "-"},
    {"SHAPE": "ddd"},
    {"TEXT": "-"},
    {"SHAPE": "dddd"}
]

usaPatternTwo = [ # (123)-456-7890
    {"ORTH":"(", "OP": "?"},
    {"SHAPE": "ddd"},
    {"ORTH": ")", "OP": "?"},
    {"SHAPE": "ddd"},
    {"TEXT": "-", "OP": "?"},
    {"SHAPE": "dddd"}
]

indianPattern = [
    {"ORTH": "+91","OP": "?"},
    {"ORTH":" ","OP": "?"},
    {"SHAPE": "dddd","LENGTH":10}
]
predefinedPhonePattern = [{"LIKE_NUM": True}]


professionPattern = [{"ENT_TYPE": "JOBTITLE"}]
gapPeriodPattern = [{"TEXT": {"REGEX": "[a-zA-Z0-9]"}},
                    {"TEXT": "to", "OP": "?"},
                    {"TEXT": "-", "OP": "?"},
                    {"TEXT": {"REGEX": "[a-zA-Z]"}},
                    {"ENT_TYPE": "DATE"}]
qualification_pattern = [{"POS": "NOUN"}]

countries = ['United States of America', 'USA', 'US', 'CANADA', 'CA', 'INDIA', 'usa', 'Canada', 'United States']
states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky[D]",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts[D]",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY"
]

employment_types = [
    "Full-Time",
    "Full time",
    "Part-Time",
    "Part time",
    "Corp to Corp",
    "C2C",
    "Corp to Hire",
    "C2H",
    "1099",
    "W2"
]

unsequenced_professions = [
    "Oracle Applications Techno-Functional Consultant"
]



for each_state in states:
    pattern = [{"ORTH": each_state}]
    state_matcher.add("str",None, pattern)

for each_profession in unsequenced_professions:
    pattern = [{"TEXT": each_profession}]
    profession_matcher.add("pr",None,pattern)

for each_employment_type in employment_types:
    pattern = [{"ORTH": each_employment_type}]
    employment_matcher.add("type",None,pattern)

# skills_matcher.add("H",None,skill_pattern)
# skill_pattern = [{"TEXT": {"REGEX": r'[A-Za-z0-9]'},'ENT_TYPE':'ORG'}]
