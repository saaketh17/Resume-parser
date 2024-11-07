import spacy
import json
import random
from spacy.util import minibatch, compounding
from tqdm import tqdm
import pickle


def load_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return (data)


nlp = spacy.blank('en')


class ProfessionModelTraining:

    def __init__(self):
        self.train_data = load_file('training_data.json')
        self.pickle_training = pickle.load(open('train_data.pkl', 'rb'))

    def academic_model(self, train_data, iterations):
        # Remove all pipelines and add NER pipeline from the model
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            # adding NER pipeline to nlp model
            nlp.add_pipe(ner, last=True)

        # Add labels in the NLP pipeline
        for _, annotation in train_data:
            for ent in annotation.get('entities'):
                ner.add_label(ent[2])

        # Remove other pipelines if they are there
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
        with nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = nlp.begin_training()
            for itn in range(10):  # train for 10 iterations
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
        nlp.to_disk('./academic_model')

    def sample_training(self, trainingData, iterations):
        nlp = spacy.blank('en')
        nlp.add_pipe(nlp.create_pipe('ner'))
        ner = nlp.get_pipe('ner')

        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        for label in trainingData["classes"]:
            ner.add_label(label)

        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        with nlp.disable_pipes(*other_pipes):
            sizes = compounding(1.0, 4.0, 1.001)
            optimizer = nlp.begin_training()
            for iter in range(iterations):
                random.shuffle(trainingData["annotations"])
                batches = minibatch(trainingData["annotations"], size=sizes)
                for batch in tqdm(batches):
                    texts, annotations = zip(*batch)
                    nlp.update(texts, annotations, drop=0.2, sgd=optimizer)

        nlp.to_disk('./profession_model')


modelTrainer = ProfessionModelTraining()
modelTrainer.sample_training(modelTrainer.train_data, 10)
modelTrainer.academic_model(modelTrainer.pickle_training, 10)
