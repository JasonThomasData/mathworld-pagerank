from bs4 import BeautifulSoup

class Parser:
    def get_by_class_name(self, html_content, class_name):
        soup = BeautifulSoup(html_content, features="html.parser")
        return soup.find(class_=class_name)

    def get_by_id_name(self, html_content, id_name):
        soup = BeautifulSoup(html_content, features="html.parser")
        return soup.find(id=id_name)

    def get_by_selector(self, html_content, selector):
        soup = BeautifulSoup(html_content, features="html.parser")
        return soup.select_one(selector)

    def get_all_links(self, html_content, selector):
        soup = self.get_by_selector(html_content, selector)
        all_links = []
        for link in soup.find_all("a"):
            all_links.append(link.get("href"))
        return all_links

    def is_class_name_found(self, html_content, class_name):
        return (self.get_by_class_name(html_content, class_name) is not None)

    def is_selector_found(self, html_content, selector):
        return (self.get_by_selector(html_content, selector) is not None)

    def is_element_found(self, html_content, element_html):
        return (html_content.find(element_html) != -1)
