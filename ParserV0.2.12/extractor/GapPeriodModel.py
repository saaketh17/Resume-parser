import spacy
import random
import json

nlp = spacy.blank('en')

labeled_data = []
with open(r"admin.jsonl", "r") as read_file:
    for line in read_file:
        data = json.loads(line)
        labeled_data.append(data)

with open(r"adminTwo.jsonl", "r") as read_file:
    for line in read_file:
        data = json.loads(line)
        labeled_data.append(data)

TRAINING_DATA = []
for entry in labeled_data:
    entities = []
    for e in entry['label']:
        entities.append((e[0], e[1],e[2]))
    spacy_entry = (entry['data'], {"entities": entities})
    TRAINING_DATA.append(spacy_entry)

print(labeled_data)

def load_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return (data)


def gap_period_model(train_data, iterations):
    # Remove all pipelines and add NER pipeline from the model
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        # adding NER pipeline to nlp model
        nlp.add_pipe(ner, last=True)
        ner = nlp.get_pipe('ner')
        ner.add_label('ADDRESS')
        ner.add_label('PERSON')
        ner.add_label('GAP')
        ner.add_label('CURRENT_EMPLOYER')
        ner.add_label('ROLE')


    # Remove other pipelines if they are there
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):  # train for 10 iterations
            print("Starting iteration " + str(itn))
            random.shuffle(train_data)
            losses = {}
            index = 0
            for text, annotations in train_data:
                try:
                    nlp.update(
                        [text],  # batch of texts
                        [annotations],  # batch of annotations
                        drop=0.2,  # dropout - make it harder to memorise data
                        sgd=optimizer,  # callable to update weights
                        losses=losses)
                except Exception as e:
                    pass

            print(losses)
    nlp.to_disk('./ThuNERModel')


gap_period_model(TRAINING_DATA, 25)
