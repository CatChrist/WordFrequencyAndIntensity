from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

def importDocument(subredditName = 0):
    if (subredditName == 0):
        return 0
    document = subredditName + "_comment_data.csv"
    with open(document) as rf:
        rf.readline() #gets rid of our key line
        unformatted_document = rf.readlines()
        formatted_document = []
        for text in tqdm(unformatted_document):
            temp_text = text.split(",")
            content = temp_text[2]
            formatted_document.append(content + "\n")
        formatted_document = "".join(formatted_document)

    print(subredditName + " returned.")
    return formatted_document

def getStopWords(stopWordsFile):
    with open(stopWordsFile) as rf:
        rawStopWords = rf.readlines()
        stopWords = []
        for word in rawStopWords:
            word = word.replace('\n','')
            stopWords.append(word)
    return stopWords

coronavirusDocument = importDocument("coronavirus")
coronavirusDocuments = coronavirusDocument.split("\n")

conspiracyDocument = importDocument("conspiracy")
conspiracyDocuments = conspiracyDocument.split("\n")

askRedditDocument = importDocument("askReddit")
askRedditDocuments = askRedditDocument.split("\n")

# formatted_corpus = [coronavirusDocument, conspiracyDocument, askRedditDocument]

print("Creating vectorizer.")
vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=100,
    max_df=0.8,
    min_df=0.010,
    ngram_range = (1,3),
    stop_words=getStopWords('uselesswords.txt')
)
print("Fitting data.")
# vector = vectorizer.fit_transform(formatted_corpus)

def tfidf(documents):
    vector = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names()
    dense = vector.todense()
    denselist = dense.tolist()

    all_keywords = []

    for description in denselist:
        x = 0
        keywords = []
        for word in description:
            if word > 0:
                keywords.append(feature_names[x])
            x+=1
        all_keywords.append(keywords)

    true_keywords = []
    for keywords in all_keywords:
        for keyword in keywords:
            if (keyword in true_keywords):
                pass
            else:
                true_keywords.append(keyword)

    return true_keywords

coronavirusKeywords = tfidf(coronavirusDocuments)
conspiracyKeywords = tfidf(conspiracyDocuments)
# askRedditKeywords = tfidf(askRedditDocuments)

keywords = []
# for keyword in askRedditKeywords:
#     if not (keyword in keywords):
#         if ((keyword in coronavirusKeywords) or (keyword in conspiracyKeywords)):
#             keywords.append(keyword)

for keyword in coronavirusKeywords:
    if not (keyword in keywords):
        if (keyword in conspiracyKeywords):
            keywords.append(keyword)

keywords.sort()
for keyword in keywords:
    print (keyword)



