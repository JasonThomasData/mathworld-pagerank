#!/usr/bin/env python3

from unittest import TestCase, main, mock

from db_model import DB_MODEL
from db_manager import DBManager
from web_crawler import Crawler

class Testing(TestCase):

    def test_complete_links(self):
        crawler = Crawler("https://url.com", "https://url.com", None, None, None)
        
        expected = ["https://url.com/somepage.html", "https://url.com/topics/something", "https://url.com/somepage.html"]
        actual = crawler.complete_links(["https://url.com/somepage.html", "https://else.com", "topics/something", "/somepage.html", "#same-page"])

        self.assertEqual(expected, actual)

    def test_entry_created(self):
        mock_db_manager = mock.Mock(spec=DBManager)
        mock_db_manager.retrieve.return_value = None

        crawler = Crawler("https://url.com",
                          "https://url.com",
                          None,
                          None,
                          mock_db_manager)

        links = ["https://url.com/somepage.html"]
        crawler.enter_links_as_new_records(links)

        mock_db_manager.create.assert_called()

    def test_entry_not_created(self):
        mock_db_manager = mock.Mock(spec=DBManager)
        mock_db_manager.retrieve.return_value = DB_MODEL("url","",0,"")

        crawler = Crawler("https://url.com",
                          "https://url.com",
                          None,
                          None,
                          mock_db_manager)

        links = ["https://url.com/somepage.html"]
        crawler.enter_links_as_new_records(links)

        mock_db_manager.create.assert_not_called()

    def test_page_created(self):
        mock_db_manager = mock.Mock(spec=DBManager)
        mock_db_manager.retrieve.return_value = None

        crawler = Crawler("https://url.com",
                          "https://url.com",
                          None,
                          None,
                          mock_db_manager)

        links = ["https://url.com/somepage.html", "https://url.com/someother.html"]
        crawler.save_this_page("url", "type", links)

        mock_db_manager.create.assert_called()
        mock_db_manager.update.assert_not_called()

    def test_page_updated(self):
        mock_db_manager = mock.Mock(spec=DBManager)
        mock_db_manager.retrieve.return_value = DB_MODEL("url","",0,"")

        crawler = Crawler("https://url.com",
                          "https://url.com",
                          None,
                          None,
                          mock_db_manager)

        links = ["https://url.com/somepage.html", "https://url.com/someother.html"]
        crawler.save_this_page("url", "type", links)

        mock_db_manager.create.assert_not_called()
        mock_db_manager.update.assert_called()

    def test_page_not_created_or_updated(self):
        mock_db_manager = mock.Mock(spec=DBManager)
        mock_db_manager.retrieve.return_value = DB_MODEL("url","",1,"")

        crawler = Crawler("https://url.com",
                          "https://url.com",
                          None,
                          None,
                          mock_db_manager)

        links = ["https://url.com/somepage.html", "https://url.com/someother.html"]
        crawler.save_this_page("url", "type", links)

        mock_db_manager.create.assert_not_called()
        mock_db_manager.update.assert_not_called()

if __name__ == '__main__':
    main()
