from gensim.models import Doc2Vec
import gensim
import smart_open
import os
import collections

TRAINING_FILE="./training.txt"
hasLoadedModel = False

def read_corpus(fname):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
    
train_corpus = list(read_corpus(TRAINING_FILE))


model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=2, epochs=50, max_vocab_size=10000000)

def load_model():
    global model
    global hasLoadedModel
    if not os.path.isfile("./model.mdl"):
        print("Model not found on disk")
        return
    model = Doc2Vec.load("./model.mdl")
    print("Model loaded")
    hasLoadedModel = True

def init_model():
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples = model.corpus_count, epochs=model.epochs)
    model.save("./model.mdl")

def findMostSimilar(doc_id):
    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    inferred_vector = model.infer_vector(train_corpus[doc_id].words)
    sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

def searchBySimilarity(text):
    wordsList = gensim.utils.simple_preprocess(text)
    inferred_vector = model.infer_vector(wordsList)
    sims = model.dv.most_similar([inferred_vector], topn=min(5, len(model.dv)))
    print(u'\nSIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for i in range(0, min(5, len(sims))) :
        print(f"{sims[i]} {' '.join(train_corpus[sims[i][0]].words)}")
    print("")

def getInferredVector(text):
    return model.infer_vector(gensim.utils.simple_preprocess(text))

def assessModel():
    ranks = []
    second_ranks = []
    for doc_id in range(len(train_corpus)):
        inferred_vector = model.infer_vector(train_corpus[doc_id].words)
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)

        second_ranks.append(sims[1])
    counter = collections.Counter(ranks)
    
    print(sorted(counter.items()))

def prepare_system():
    load_model()
    if not hasLoadedModel:
        print("Creating new model from training data...")
        init_model()
        print("Model generated")
if __name__ == '__main__':
    prepare_system()
    ##assessModel()
    while True:
        searchString = input("Search for similar news stories\n")
        searchBySimilarity(searchString)
