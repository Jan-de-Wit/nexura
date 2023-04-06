import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transition_model = {}

    # Checks if there are any pages to visit from the current page
    if len(corpus[page]) == 0:
        # Calculates the probability distribution by splitting 1 over the amount of pages in the corpus
        # Note that the integer 10000 is used to counter floating point imprecision.
        probability = ((10000) / (len(corpus))) / 10000

        # Loops through the possible pages and adds the probabilty to it
        for page in corpus:
            transition_model[page] = transition_model.get(
                page, 0) + probability

        return transition_model

    # Initiates the list of links that can be visited
    currentOptions = [link for link in corpus[page]]

    # Calculates the probabilty of randomly accessing the page
    # Note that the integer 10000 is used to counter floating point imprecision.
    baseProbability = (((1 - damping_factor) * 10000) / (len(corpus))) / 10000

    # Iterates over all of the pages in the corpus and adds the base probability
    for page in corpus:
        transition_model[page] = transition_model.get(
            page, 0) + baseProbability

    # Calculates the probability of accessing a page via a link on the current page
    additionalProbability = damping_factor / len(currentOptions)

    # Iterates over the mentioned links and adds the probability in the transition model
    for link in currentOptions:
        transition_model[link] += additionalProbability

    return transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initiates a random sample
    pages = [page for page in corpus]
    sample = transition_model(
        corpus, pages[random.randint(0, len(pages) - 1)], damping_factor)

    # Initializes the pageRank dictionary and adds all of the pages into it.
    pageRank = {}
    for page in corpus:
        pageRank[page] = 0

    # Samples n times
    while n > 0:
        # Chooses a random page from the current sample
        choice = random.choices(list(sample.keys()), list(sample.values()))[0]

        # Adds the chosen page to the dictionary
        pageRank[choice] += 1

        # Creates a new sample
        sample = transition_model(corpus, choice, damping_factor)

        # Removes one from the loop, so that it doesn't loop infinitely
        n -= 1

    # Iterates over the pages and pagerank values to find what they sum up to
    pageRankSum = 0
    for value in pageRank.values():
        pageRankSum += value

    # Updates the values of the pageranks to let it all sum to 1
    if pageRankSum != 1:
        # Divides the value by the sum to get the sum to 1
        for page in pageRank:
            pageRank[page] /= pageRankSum
    
    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initializes the pageRank dictionary with a basic value of the pagerank
    # and adds all of the pages into it.
    # Also intializes the linkedBy dictionary, which is a reversed version of the corpus
    # used to easily fetch what pages the page has been linked by.
    pageRank = {}
    linkedBy = {page: set() for page in corpus}
    baseRank = 1 / len(corpus)
    for page in corpus:
        pageRank[page] = baseRank
        for link in corpus[page]:
            linkedBy[link].add(page)

    # Loops until the difference is less than or equal to 0.001
    difference = None
    while difference is None or difference > 0.001:
        difference = 0

        # Loops through all pages in the corpus
        for page in corpus:
            # Calculates the first part of the formula
            PR = (1 - damping_factor) / len(corpus)

            # Iterates over all pages that have linked to this page (part 2 of the formula)
            for link in linkedBy[page]:
                # Checks if there are any links on this page
                if len(corpus[link]) > 0:
                    # Calculates the second part of the formula
                    PR += damping_factor * sum([pageRank[link] / len(corpus[link])])
                else:
                    # Calculates the second part of the formula as a base value
                    PR += 1 / len(corpus)

            # Calculate the difference between the original and the new pagerank
            difference = max(difference, abs(pageRank[page] - PR))

            # Sets the new pagerank to the value in the dictionary
            pageRank[page] = PR

    # Iterates over the pages and pagerank values to find what they sum up to
    pageRankSum = 0
    for value in pageRank.values():
        pageRankSum += value

    # Updates the values of the pageranks to let it all sum to 1
    if pageRankSum != 1:
        # Divides the value by the sum to get the sum to 1
        for page in pageRank:
            pageRank[page] /= pageRankSum

    return pageRank


if __name__ == "__main__":
    main()
