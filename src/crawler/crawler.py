import queue as _queue
import secrets
import threading
from pathlib import Path
from time import sleep
from typing import Any, Dict, List, Literal, NoReturn

import pymongo.database as _database
from requests.sessions import Session

from src.general.create_file import create_file

from ..general import get_domain
from ..models import Crawled as _crawled_collection
from ..models import FailedCrawled as _failed_crawled_collection
from ..models import Pause as _pause_collection
from ..models import Queue as _queue_collection
from .check_robots_txt import check_robots_txt as _check_robots_txt
from .constants import BOT_NAME
from .get_robots_txt_url import get_robots_txt_url


# !This is the main crawler
class Crawler:
    """
    A class that implements a web crawler to fetch and store HTML content from specified URLs while adhering to the rules defined in robots.txt.
    """

    max_number_of_threads = 0
    to_parse_directory = ""
    db: _database.Database[Dict[str, Any]]
    queue: _queue_collection
    crawled: _crawled_collection
    pause: _pause_collection
    failed_crawled: _failed_crawled_collection
    threadTasks: _queue.Queue[float] = _queue.Queue()
    session = Session()

    def __init__(
        self,
        max_numbers_of_threads: int,
        to_parse_directory: str,
        db: _database.Database[Dict[str, Any]],
    ) -> None:
        """
        Initializes the Crawler with the specified parameters for concurrent web crawling.

        Args:
            max_numbers_of_threads (int): The maximum number of threads to use for crawling.
            to_parse_directory (str): The directory where crawled HTML files will be stored.
            db (Database): The database instance used for storing and retrieving URLs.
        """
        self.max_number_of_threads = max_numbers_of_threads
        self.to_parse_directory = to_parse_directory
        self.db = db

        self.queue_collection = _queue_collection(self.db)
        self.crawled_collection = _crawled_collection(self.db)
        self.paused_collection = _pause_collection(self.db)
        self.failed_crawled_collection = _failed_crawled_collection(self.db)

        # !Start the main crawling process
        self.main()

    def main(self) -> None:
        """Creates the threads needed by the crawler"""
        threading.Thread(target=self.work, daemon=True).start()
        for _ in range(self.max_number_of_threads - 1):
            threading.Thread(target=self.crawl_work, daemon=True).start()

    def work(self) -> NoReturn:
        """Assigns work for threads to do"""
        while True:
            # !Assigns the first 10 links in queue the crawler threads
            for i in range(10):
                try:
                    self.threadTasks.put(float(self.queue_collection.get()[i]["id"]))
                except IndexError:
                    break

            # !Waits for all tasks to be completed
            self.threadTasks.join()

            # !Waits for 10 seconds before continuing
            sleep(10)

    def crawl_work(self) -> NoReturn:
        """Continuously processes URLs from the queue for crawling"""

        while True:
            # !Get link from database
            link_in_db = self.queue_collection.get_one({"id": self.threadTasks.get()})

            # !Checks if link does not exist
            if link_in_db is None:
                self.complete_task()
                continue

            # !Checks if we are to pause on crawling the link
            if self.paused_collection.get_one({"url": get_domain(link_in_db["url"])}):
                self.complete_task()
                continue

            # !Check robot.txt
            robot_txt = self.get_robots_txt(str(link_in_db["url"]))
            if not isinstance(robot_txt, str):
                self.handle_error(robot_txt[0], link_in_db["url"])
                continue
            if not _check_robots_txt(str(link_in_db["url"]), robot_txt, BOT_NAME):
                self.queue_collection.remove({"url": link_in_db["url"]})
                self.complete_task()

            # !Get HTML
            response = self.crawl_link(link_in_db["url"])

            # !Error management
            if not isinstance(response, str):
                self.handle_error(response[0], link_in_db["url"])
                continue

            # !Save HTML
            self.save_html(response, link_in_db["url"])
            self.complete_task()

    def complete_task(self) -> None:
        """Marks the current task as completed"""
        self.threadTasks.task_done()

    def handle_error(
        self, error_message: Literal["Not found"] | Literal["Overload"] | Literal["Error"], url: str
    ) -> None:
        """Handles errors encountered during the crawling process.

        Args:
            error_message(str): The type of error encountered, which can be "Not found", "Overload", or "Error".
            url: The URL associated with the error.

        Returns:
            None
        """
        if error_message == "Overload":
            self.paused_collection.add(get_domain(url))
        elif error_message == "Error":
            self.queue_collection.remove({"url": url})
        elif error_message == "Not found":
            self.failed_crawled.add(url, "not found")
        self.complete_task()

    def crawl_link(self, url: str) -> str | List[Literal["Not found"] | Literal["Overload"] | Literal["Error"]]:
        """
        Crawls the given url

        Args:
            url(str): The URL to crawl.

        Returns:
            str or List[str]: The response of the provided url or error message
        """
        # !Send request
        response = self.session.get(url)

        # !Check status code
        status_code_map: Dict[int, str | List[Literal["Not found"] | Literal["Overload"] | Literal["Error"]]] = {
            200: response.text,
            201: response.text,
            **{code: ["Not found"] for code in range(400, 429)},
            **{code: ["Overload"] for code in range(429, 504)},
        }

        return status_code_map.get(response.status_code, ["Error"])

    # !Get robot.txt for the particular link
    def get_robots_txt(self, url: str) -> str | List[Literal["Overload"]]:
        """Gets the robots.txt content for a certain link
        Args:
            url(str): The URL to get robot.txt of.

        Returns:
            str | List[str]: The robot txt content or the error message
        """
        robots_txt_url = get_robots_txt_url(url)

        response = self.session.get(robots_txt_url)

        if response.status_code in (200, 201):
            return response.text

        if 400 <= response.status_code < 429:
            return ""

        return ["Overload"] if 429 <= response.status_code <= 503 else ""

    def save_html(self, response: str, url: str) -> None:
        """Saves the HTML response to a file and updates the crawling state.

        Args:
            response(str): The HTML content to be saved.
            url(str): The URL associated with the HTML content.

        Returns:
            None
        """
        file_name = self.get_filename()
        create_file(f"{file_name}.html", self.to_parse_directory, response)
        self.queue_collection.remove({"url": url})
        self.crawled_collection.add(url, "crawled", file_name)

    def get_filename(self) -> str:
        """Gets the filename for the crawled data to be stored"""
        while True:
            # !Generate random filename
            file_name = secrets.token_urlsafe(10)[:13]

            # !Check if already being used
            if not Path(f"{self.to_parse_directory}/{file_name}.txt").exists():
                return file_name
