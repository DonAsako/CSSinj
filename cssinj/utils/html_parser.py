from html.parser import HTMLParser
from cssinj.utils.dom import Element, Attribut


class HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attributs = []
        for attr in attrs:
            attributs.append(Attribut(name=attr[0], value=attr[1]))
        self.elements.append(Element(name=tag, attributs=attributs))

    def get_element_by_name(self, element_name) -> list:
        elements_by_name = []
        for element in self.elements:
            if element.name == element_name:
                elements_by_name.append(element)
        return elements_by_name

    def get_element_by_attr(self, attr_name) -> list:
        elements_by_attr = []
        for element in self.elements:
            for attr in element.attributs:
                if attr.name == attr_name:
                    elements_by_attr.append(element)

        return elements_by_attr

    def get_value_by_attr_name(self, attr_name) -> list:
        elements_by_attr = self.get_element_by_attr(attr_name)
        values = []
        for element in elements_by_attr:
            for attribut in element.attributs:
                if attribut.name == attr_name:
                    values.append(attribut.value)
        return values
