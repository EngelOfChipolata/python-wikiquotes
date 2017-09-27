from itertools import islice
from lxml import etree

MAIN_PAGE = "Wikiquote:Accueil"


def extract_quotes(tree, max_quotes):
    # French wiki uses a "citation" HTML class
    node_list = tree.xpath('//p/span[@class="citation"]')
    quotes = list(islice((span.text_content()
                          for span in node_list),
                         max_quotes))

    return quotes


def extract_quotes_and_authors(tree):
    WAIT_FOR_h3 = 0
    WAIT_FOR_a = 1
    state = WAIT_FOR_h3
    current_character = None
    quotes = {}
    for element in tree.iter():
        if state == WAIT_FOR_h3:
            if element.tag == "h3":
                current_character = None
                state = WAIT_FOR_a
                continue
            if element.tag == "span" and "class" in element.attrib and element.attrib["class"] == "citation":
                quotes[element.text] = current_character
                continue
        if state == WAIT_FOR_a:
            if element.tag == "a" and "class" in element.attrib and element.attrib["class"] == "extiw":
                current_character = element.text
                state = WAIT_FOR_h3
            continue
    return quotes
    # author_nodes = tree.xpath('//h3/span[@class="mw-headline"]')
    # print(author_nodes)
    # authors = list(islice((span.text_content()
    #                       for span in author_nodes),
    #                      max_quotes))
    # print(authors)


def qotd(html_tree):
    tree = html_tree.get_element_by_id('mf-cdj')
    tree = tree.xpath('div/div')[1].xpath('table/tr/td')[1]

    quote = tree.xpath('div/i')[0].text_content().replace(u'\xa0', u' ')
    author = tree.xpath('div/a')[0].text_content()
    return quote, author
