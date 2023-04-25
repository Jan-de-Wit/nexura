import os
import string
import nltk
import math
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # Create a dictionary to store the files
    files = {}

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        # Open the file
        with open(os.path.join(directory, filename), "r", encoding="utf8") as file:
            # Read the contents of the file
            content = file.read()

            # Store the contents of the file in the dictionary
            files[filename] = content

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    # Tokenize the document
    tokens = nltk.word_tokenize(document.lower())

    cleaned = []

    # Remove punctuation and stopwords
    for token in tokens:
        if token in nltk.corpus.stopwords.words("english"):
            continue

        allPunctuation = True

        for char in token:
            if char not in string.punctuation:
                allPunctuation = False
                break

        if not allPunctuation:
            cleaned.append(token)

    return cleaned


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.

    """

    # Create a dictionary to store the idfs
    idfs = {}

    # Iterate through the documents
    for document in documents:

        # Iterate through the words in the document
        for word in set(documents[document]):

            # If the word is not in the idfs dictionary, add it
            if word not in idfs:
                idfs[word] = 0

            # Increment the word's idf
            idfs[word] += 1

    # Iterate through the idfs
    for word in idfs:

        # Calculate the idf
        idfs[word] = math.log(len(documents) / idfs[word])

    return idfs
    



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    
    # Create a dictionary to store the tf-idfs
    tf_idfs = {}

    # Iterate through the files
    for file in files:

        # Create a dictionary to store the tf-idfs for the file
        tf_idfs[file] = 0

        # Iterate through the words in the file
        for word in files[file]:

            # If the word is in the query, add its tf-idf to the file's tf-idf
            if word in query:
                tf_idfs[file] += (files[file].count(word) / len(files[file])) * idfs[word]

    # Sort the files by their tf-idfs
    sorted_files = sorted(tf_idfs, key=tf_idfs.get, reverse=True)

    # Return the top n files
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    # Create a dictionary to store the idfs
    sentence_idfs = {}

    # Iterate through the sentences
    for sentence in sentences:

        # Create a dictionary to store the idfs for the sentence
        sentence_idfs[sentence] = 0

        # Iterate through the words in the sentence
        for word in sentences[sentence]:

            # If the word is in the query, add its idf to the sentence's idf
            if word in query:
                sentence_idfs[sentence] += idfs[word]

    # Sort the sentences by their idfs
    sorted_sentences = sorted(sentence_idfs, key=sentence_idfs.get, reverse=True)

    # Return the top n sentences
    return sorted_sentences[:n]


if __name__ == "__main__":
    main()
