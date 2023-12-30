from models import Author, Quote
import connect
import json

authors_list = []


def json_reader(filename):
    with open(filename, 'r') as f:
        result = json.load(f)
    return result


def authors_filler(filename):
    authors = json_reader(filename)
    for author in authors:
        author_obj = Author(fullname=author["fullname"],
                            born_date=author["born_date"],
                            born_location=author["born_location"],
                            description=author["description"])
        authors_list.append(author_obj)
        author_obj.save()


def quotes_filler(filename):
    quotes = json_reader(filename)
    for quote in quotes:
        for author in authors_list:
            if quote["author"] == author.fullname:
                quote_obj = Quote(tags=quote["tags"],
                                  author=author.id,
                                  quote=quote["quote"])
                quote_obj.save()


if __name__ == '__main__':
    authors_filler('authors.json')
    quotes_filler('quotes.json')
