from one.models import Book

def todatabase(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            path ,name = line.strip().split('||')
            book = Book(bookpath=path, bookname=name)
            book.save()
            print(name)

