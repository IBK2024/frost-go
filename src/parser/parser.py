import queue as _queue
from concurrent.futures import ThreadPoolExecutor
from os import listdir, remove
from time import sleep
from typing import Any, NoReturn

import pymongo.database as _database
from bs4 import BeautifulSoup

from ..general import get_domain, get_scheme, open_file, tokenize_string
from ..models import Crawled as _crawled_collection
from ..models import Queue as _queue_collection


class Parser:
    """Parser for processing HTML files and extracting links."""

    max_number_of_threads: int
    to_parse_directory: str
    db: _database.Database[dict[str, Any]]
    threadTasks: _queue.Queue[str] = _queue.Queue()
    crawled: _crawled_collection
    queue: _queue_collection

    def __init__(
        self,
        max_number_of_threads: int,
        to_parse_directory: str,
        db: _database.Database[dict[str, Any]],
    ) -> None:
        """Initializes the parser

        Args:
            max_number_of_threads (int): The maximum number of treads to be used.
            to_parse_directory (str): The directory where html files are stored
            db (_database.Database[dict[str, Any]]): Database class
        """
        self.max_number_of_threads = max_number_of_threads
        self.to_parse_directory = to_parse_directory
        self.db = db

        # !Get crawled and queue collections
        self.queue = _queue_collection(self.db)
        self.crawled = _crawled_collection(self.db)

        # !Create threads
        self.create_threads()

    # !Create threads
    def create_threads(self) -> None:
        """Creates threads"""
        with ThreadPoolExecutor(max_workers=self.max_number_of_threads) as executor:
            executor.submit(self.work)
            for _ in range(self.max_number_of_threads - 1):
                executor.submit(self.parse_work)

    # !Assigns work to threads
    def work(self) -> NoReturn:
        """Assigns work to threads"""
        while True:
            # !Assigns the first 10 files in to_parse directory to parser threads
            for i in range(10):
                try:
                    self.threadTasks.put(listdir(self.to_parse_directory)[i])
                except IndexError:
                    break

            # !Waits for all tasks to be completed
            self.threadTasks.join()

            # !Waits for 10 seconds before continuing
            sleep(10)

    # !Picks a downloaded html document and parse it
    def parse_work(self) -> NoReturn:
        """Continuously processes HTML files for parsing and link extraction"""
        while True:
            file_name = self.threadTasks.get()
            base_file_name = file_name.rstrip(".html")

            file = open_file(file_name, self.to_parse_directory, "utf8")

            soup = BeautifulSoup(file, "html.parser")

            # !Get links
            links = self.get_links(soup)

            # !Parse links
            current_page = self.crawled.get_one({"file_name": base_file_name})
            if not current_page:
                self.complete_task()
                continue

            accepted_links = self.parse_links(links, current_page["url"])

            # !Add accepted links to queue
            for link in accepted_links:
                if not self.crawled.get_one({"url": link}):
                    self.queue.add(link)

            # !Update crawled
            title = str((soup.title.string if soup.title else "No Title")).replace("\n", "").replace("  ", "")
            self.crawled.update({"file_name": base_file_name}, {"title": title})
            self.crawled.update({"file_name": base_file_name}, {"forward_links": accepted_links})

            # !Tokenize text
            tokens = tokenize_string(soup.get_text())
            self.crawled.update({"file_name": file_name.rstrip(".html")}, {"tokens": tokens})

            # !Convert links status to parsed
            self.crawled.update({"file_name": file_name.rstrip(".html")}, {"status": "parsed"})

            # !Done with task
            remove(f"{self.to_parse_directory}/{file_name}")
            self.complete_task()

    @staticmethod
    def get_links(soup: BeautifulSoup) -> list[str]:
        """Extracts links from the html

        Args:
            soup (BeautifulSoup): The beautiful soup html soup

        Returns:
            list[str]: List of links found
        """
        return [link for link in [link.get("href") for link in soup.find_all("a")] if link is not None if link != ""]

    def parse_links(self, links: list[str], current_page: str) -> list[str]:
        """Parses the provided links

        Args:
            links (list[str]): Links to parse
            current_page (str): The website where the links where found

        Returns:
            list[str]: A list of parsed links
        """

        def clean_link(link: str, scheme: str) -> str:
            return link.replace(f"{scheme}://", "").replace(" ", "").replace("\t", "").replace("\n", "")

        def is_non_html(link: str) -> bool:
            return link[-4:].lower() in [".jpg", ".png", ".gif", ".svg", ".pdf"]

        def is_malformed(link: str) -> bool:
            return not link.split("/")[0].replace(".", "").replace("-", "").isalnum() or link[0] in (
                "#",
                "(",
                "{",
                "?",
                "<",
                "\\",
            )

        def is_false_link(link: str) -> bool:
            return any(link.lower().startswith(prefix) for prefix in ("mailto:", "javascript:", "tel:", "./"))

        def standardize_link(link: str, domain: str) -> str:
            if link.startswith("//"):
                return link.replace("//", "").split(":")[0]
            elif link.startswith("/"):
                return domain + link
            return link

        accepted_links: list[str] = []
        domain = get_domain(current_page)

        for link in links:
            scheme = get_scheme(link) if link.startswith("http") else get_scheme(current_page)
            link = clean_link(link, scheme)

            if is_non_html(link) or is_malformed(link) or is_false_link(link):
                continue

            link = standardize_link(link, domain)
            if link[-1] == "/":
                link = link[:-1]

            accepted_links.append(f"{scheme}://{link}")

        return accepted_links

    def complete_task(self) -> None:
        """Complete task"""
        self.threadTasks.task_done()
