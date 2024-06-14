from html.parser import HTMLParser

paragraphs = 0

class MyHTMLParser(HTMLParser):
    def handle_comment(self, data):
        print("Encountered a comment: ", data)
        pos = self.getpos()
        print("At line:", pos[0], " position: ", pos[1])
    
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag: ", tag)
        pos = self.getpos()
        print("At line:", pos[0], " position: ", pos[1])

        global paragraphs
        if tag == "p":
            paragraphs += 1

        if len(attrs) > 0:
            print("Attributes:")
            for a in attrs:
                print("\t",a[0], "=", a[1])
                

    def handle_data(self, data):
        if data.isspace():
            return
        else:
            print("Encountered text data: ", data)
            pos = self.getpos()
            print("At line:", pos[0], " position: ", pos[1])

def main():
    parser = MyHTMLParser()

    f = open("samplehtml.html")
    if f.mode == "r":
        contents = f.read()
        parser.feed(contents)

    print("Paragraph count: ", paragraphs)

if __name__ == "__main__":
    main()