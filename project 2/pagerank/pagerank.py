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
    """
    num_pages = len(corpus)
    probabilities = dict()

    links = corpus[page]
    if links:
        for p in corpus:
            probabilities[p] = (1 - damping_factor) / num_pages
            if p in links:
                probabilities[p] += damping_factor / len(links)
    else:
        # Treat page as linking to all pages
        for p in corpus:
            probabilities[p] = 1 / num_pages

    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    page_rank = dict.fromkeys(corpus.keys(), 0)
    pages = list(corpus.keys())
    current_page = random.choice(pages)

    for _ in range(n):
        page_rank[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values()),
            k=1
        )[0]

    # Normalize results
    for page in page_rank:
        page_rank[page] /= n

    return page_rank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    N = len(corpus)
    pagerank = dict.fromkeys(corpus.keys(), 1 / N)
    threshold = 0.001

    # Handle dangling pages (no links)
    for page in corpus:
        if not corpus[page]:
            corpus[page] = set(corpus.keys())

    while True:
        new_rank = dict()
        for page in corpus:
            total = 0
            for potential_linker in corpus:
                if page in corpus[potential_linker]:
                    total += pagerank[potential_linker] / len(corpus[potential_linker])
            new_rank[page] = (1 - damping_factor) / N + damping_factor * total

        # Check convergence
        if all(abs(new_rank[page] - pagerank[page]) < threshold for page in pagerank):
            break
        pagerank = new_rank

    return pagerank



if __name__ == "__main__":
    main()
