from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.convert_charrefs = False
        self.result = []

    def handle_starttag(self, tag, attrs):
        attrs_str = " ".join(f'{name}="{value}"' for name, value in attrs)
        if attrs_str:
            self.result.append(f"<{tag} {attrs_str}>")
        else:
            self.result.append(f"<{tag}>")

    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        attrs_str = " ".join(f'{name}="{value}"' for name, value in attrs)
        if attrs_str:
            self.result.append(f"<{tag} {attrs_str} />")
        else:
            self.result.append(f"<{tag} />")

    def handle_data(self, data):
        self.result.append(data)

    def handle_entityref(self, name):
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        self.result.append(f"&#{name};")

    def emit_html(self):
        return "".join(self.result)


# Read an HTML file
file_path = 'signature.html'  # Replace with your file path
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create an instance of the parser and feed the content
parser = MyHTMLParser()
parser.feed(html_content)

emit_file_path = 'signature_emit.html'  # Replace with your file path
with open(emit_file_path, 'w', encoding='utf-8') as file:
    html_content = parser.emit_html()
    print("this is sick: " + html_content + ". yes.")
    file.write(html_content)


