import os
from html.parser import HTMLParser

def attrs_to_dict(attrs):
    result = {}
    for key, value in attrs:
        result[key] = value
    return result

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
        
        manipulate_tag(tag, attrs)
        
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
        
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_endtag(tag)
            return

        self.result.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        if self.engine_current_parser is not None:
            self.engine_current_parser.handle_startendtag(tag, attrs)
            return

        manipulate_tag(tag, attrs)

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
        
        attrs_dict = attrs_to_dict(attrs)
        
        for key, value in attrs:
            if key == "var":
                self.engine_current_parser = MyHTMLParser(self.include_dir)
                self.engine_var_parsers[value] = self.engine_current_parser
            elif key == "insert":
                if value == "file":
                    filename = attrs_dict["name"]
                    filepath = os.path.join(self.include_dir, filename)
                    parser = MyHTMLParser(self.include_dir)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        html_content = file.read()
                    parser.engine_var_parsers = self.engine_var_parsers
                    parser.feed(html_content)
                    self.result.append(parser.emit_html())
                elif value == "var":
                    name = attrs_dict["name"]
                    if name in self.engine_var_parsers:
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
    
def manipulate_tag(tag, attrs):
    if tag == "table":
        attrs_add(attrs, "border", "0")
        attrs_add(attrs, "cellspacing", "0")
        attrs_add(attrs, "cellpadding", "0")

def attrs_add(attrs, key, value, overwrite=False):
    for idx, item in enumerate(attrs):
        e_key, e_value = item
        if e_key == key:
            if not overwrite:
                return
            attrs[idx] = (key, value)
            return
    attrs.append((key, value))
    

def build_sig(filename, dir, include_dir, output_dir):
    file_path = os.path.join(dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    parser = MyHTMLParser(include_dir)
    parser.feed(html_content)
    output_content = parser.emit_html()
    outfile_path = os.path.join(output_dir, os.path.splitext(filename)[0]+".html")
    with open(outfile_path, 'w', encoding='utf-8') as file:
        file.write(output_content)
    

