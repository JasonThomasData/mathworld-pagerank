from time import sleep

from db_model import DB_MODEL

class Crawler:
    def __init__(self, url_no_path, seed_url, browser, parser, db_manager):
        self.url_no_path = url_no_path
        self.seed_url = seed_url
        self.browser = browser
        self.parser = parser
        self.db_manager = db_manager

    def complete_links(self, links):
        completed_links = []
        for link in links:
            if link.find("/") == 0:
                link = self.url_no_path + link
                completed_links.append(link)
            elif link.find("topics") == 0:
                link = self.url_no_path + "/" + link
                completed_links.append(link)
            elif link.find("#") == 0:
                print("same page link, ignore")
                continue
            elif link.find(self.url_no_path) != -1:
                completed_links.append(link)
        return completed_links

    def enter_links_as_new_records(self, links):
        for link in links:
            record = self.db_manager.retrieve(link)
            if record is None:
                self.db_manager.create(DB_MODEL(link, "unknown", 0, ""))

    def save_this_page(self, url, type, links):
        record = self.db_manager.retrieve(url)
        links = ", ".join(links)
        if record is None:
            self.db_manager.create(DB_MODEL(url, type, 1, links))
        elif record.visited == 0:
            self.db_manager.update(DB_MODEL(url, type, 1, links))

    def process_page(self, url):
        content = self.browser.get_content(url)

        categories_selector = "#categories"
        topics_selector = ".topics-list"
        entry_selector = ".entry-content"
        cross_ref_selector = ".CrossRefs"

        links = []
        type = ""
        if self.parser.is_selector_found(content, categories_selector):
            links = self.parser.get_all_links(content, categories_selector)
            type = "category"
        elif self.parser.is_selector_found(content, topics_selector):
            links = self.parser.get_all_links(content, topics_selector)
            type = "topic"
        elif self.parser.is_selector_found(content, entry_selector):
            links = self.parser.get_all_links(content, entry_selector)
            type = "entry"
        elif self.parser.is_selector_found(content, cross_ref_selector):
            links = self.parser.get_all_links(content, cross_ref_selector)
            type = "cross-reference"
        else:    
            print(url)
            raise Exception("NOT a topic, category, entry or cross ref")

        completed_links = self.complete_links(links)
        self.enter_links_as_new_records(completed_links)
        self.save_this_page(url, type, completed_links)        

    def crawl(self):
        if self.db_manager.count() == 0:
            self.db_manager.create(DB_MODEL(self.seed_url, "unknown", 0, ""))

        while True:
            model = self.db_manager.retrieve_one_unvisited()
            if model is None:
                break

            self.process_page(model.url)
            print(model.url)
            sleep(1)

        


        
        # scrape page, collect links, save all links as records unvisited (if not in DB), save all links to url and mark as visited
        # record can be in db unvisited, in db visited.

        
        # start from the base page, add it to the db topics table
        # get content from page
            # if content has "entry-content" then collect links and enter to DB as type:entry
            # else if content has "<h2>See</h2>" then this links to another entry, enter this link as type:link
            # else if content has "topics list" then collect links and enter to DB as type:topic
            # else raise error
        # if the href is of form #<link> then it is a same page link and need not bother