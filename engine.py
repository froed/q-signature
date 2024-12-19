import os
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, include_dir):
        super().__init__()
        self.convert_charrefs = False
        self.result = []
        self.include_dir = include_dir
        self.engine_var_parsers = {}
        self.engine_current_parser = None

    def handle_starttag(self, tag, attrs):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_starttag(tag, attrs)
            return
        
        if tag == "engine":
            self.handle_engine_start(attrs)
            return

        attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs)
        if attrs_str:
            self.result.append(f"<{tag} {attrs_str}>")
        else:
            self.result.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag == "engine":
            self.handle_engine_end()
            return
        self.result.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_startendtag(tag, attrs)
            return

        if tag == "engine":
            self.handle_engine_start(attrs)
            self.handle_engine_end()
            return
        
        attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs)
        if attrs_str:
            self.result.append(f"<{tag} {attrs_str} />")
        else:
            self.result.append(f"<{tag} />")

    def handle_data(self, data):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_data(data)
            return
        
        self.result.append(data)

    def handle_entityref(self, name):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_entityref(name)
            return
        
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_charref(name)
            return
        
        self.result.append(f"&#{name};")

    def handle_engine_start(self, attrs):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_engine_start(attrs)
            return
        
        for key, value in attrs:
            if key == "var":
                self.engine_current_parser = MyHTMLParser(self.include_dir)
                self.engine_var_parsers[value] = self.engine_current_parser
            elif key == "insert":
                if value == "file":
                    filename = attrs["name"]
                    filepath = os.path.join(self.include_dir, filename)
                    parser = MyHTMLParser(self.include_dir)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        html_content = file.read()
                    parser.engine_var_parsers = self.engine_var_parsers
                    parser.feed(html_content)
                    self.result.append(parser.emit_ħtml())
                elif value == "var":
                    name = attrs["name"]
                    self.result.append(self.engine_var_parsers[name].emit_html())

    def handle_engine_end(self):
        if self.engine_current_parser is None:
            return False
        if self.engine_current_parser.handle_engine_end():
            return True
        self.engine_current_parser = None
        return True

    def emit_html(self):
        return "".join(self.result)

def parse_file(filename, dir, include_dir, output_dir):
    file_path = os.path.join(dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    parser = MyHTMLParser(include_dir)
    parser.feed(html_content)
    output_content = parser.emit_html()
    outfile_path = os.path.join(output_dir, filename)
    with open(outfile_path, 'w', encoding='utf-8') as file:
        file.write(output_content)
    

