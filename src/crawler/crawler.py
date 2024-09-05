import time as _time
import queue as _queue
import typing as _typing
import string
import random
import threading as _threading
from typing import Literal
import pymongo.database as _database
from requests.sessions import Session
from pathlib import Path
from ..models import (
    Queue as _queue_collection,
    Crawled as _crawled_collection,
    Pause as _pause_collection,
    FailedCrawled as _failed_crawled,
)
from .constants import BOT_NAME
from .check_robots_txt import check_robots_txt as _check_robots_txt
from .get_robots_txt_url import get_robots_txt_url


# !This is the main crawler
class Crawler:
    """
    This is the main crawler.
    """

    # !Variables
    max_number_of_threads = 0
    to_parse_directory = ""
    db: _database.Database[_typing.Dict[str, _typing.Any]]
    queue: _queue_collection
    crawled: _crawled_collection
    pause: _pause_collection
    failed_crawled: _failed_crawled
    threadTasks: _queue.Queue[float] = _queue.Queue()
    session = Session()

    def __init__(
        self,
        max_numbers_of_threads: int,
        to_parse_directory: str,
        db: _database.Database[_typing.Dict[str, _typing.Any]],
    ) -> None:
        """Initializes the crawler"""
        self.max_number_of_threads = max_numbers_of_threads
        self.to_parse_directory = to_parse_directory
        self.db = db

        # !Get items in crawled and queue collections
        self.queue = _queue_collection(self.db)
        self.crawled = _crawled_collection(self.db)
        self.pause = _pause_collection(self.db)
        self.failed_crawled = _failed_crawled(self.db)

        # !Create the threads
        self.main()

    # !Create the threads
    def main(self) -> None:
        """Creates the threads needed by the crawler"""
        _threading.Thread(target=self.work, daemon=True).start()
        for _ in range(self.max_number_of_threads - 1):
            _threading.Thread(target=self.crawl_work, daemon=True).start()

    # !Assign work for treads to do
    def work(self) -> _typing.NoReturn:
        """Assigns work for treads to do"""
        while True:
            # !Iterates over 100 links in queue assigns them to the crawler thread
            for item in self.queue.get()[:10]:
                self.threadTasks.put(float(item["id"]))

            # !Waits for all tasks to be completed
            self.threadTasks.join()

            # !Waits for 10 seconds before continuing
            _time.sleep(10)

    # !Pick a website from queue and crawl it
    def crawl_work(self) -> _typing.NoReturn:
        """Picks a website from queue and crawl it"""
        while True:
            link_in_db = self.queue.get_one({"id": self.threadTasks.get()})

            if link_in_db is None:
                continue

            if self.pause.get_one({"url": link_in_db["url"]}):
                self.queue.remove({"url": link_in_db["url"]})
                self.threadTasks.task_done()
                continue

            robot_txt = self.get_robots_txt(str(link_in_db["url"]))

            if not isinstance(robot_txt, str):
                if robot_txt[0] == "Overload":
                    self.pause.add(str(link_in_db["url"]))
                    self.queue.remove({"url": link_in_db["url"]})
                self.threadTasks.task_done()
                continue

            if not _check_robots_txt(str(link_in_db["url"]), robot_txt, BOT_NAME):
                self.queue.remove({"url": link_in_db["url"]})
                self.threadTasks.task_done()

            response = self.crawl_link(link_in_db["url"])

            if not isinstance(response, str):
                if response[0] == "Overload":
                    self.pause.add(str(link_in_db["url"]))
                    self.queue.remove({"url": link_in_db["url"]})

                if response[0] == "Error":
                    self.queue.remove({"url": link_in_db["url"]})
                if response[0] == "Not found":
                    self.failed_crawled.add(link_in_db["url"], "not found")

                self.threadTasks.task_done()
                continue

            file_name = self.get_filename()
            with open(f"{self.to_parse_directory}/${file_name}.html", "w", encoding="utf8") as file:
                file.write(response)

            self.queue.remove({"url": link_in_db["url"]})
            self.crawled.add(link_in_db["url"], "crawled", file_name)
            self.threadTasks.task_done()

    def crawl_link(self, url: str) -> str | list[Literal["Not found"] | Literal["Overload"] | Literal["Error"]]:
        """Crawls the given url"""
        response = self.session.get(url)

        if response.status_code in (200, 201):
            html = response.text
            return html

        if response.status_code < 429 and response.status_code >= 400:
            return ["Not found"]
        if response.status_code <= 503 and response.status_code >= 429:
            return ["Overload"]

        return ["Error"]

    # !Get robot.txt for the particular link
    def get_robots_txt(self, url: str) -> str | list[Literal["Overload"]]:
        """Gets the robots.txt for a certain link"""
        robots_txt_url = get_robots_txt_url(url)

        response = self.session.get(robots_txt_url)

        if response.status_code in (200, 201):
            return response.text

        if response.status_code < 429 and response.status_code >= 400:
            return ""

        if response.status_code <= 503 and response.status_code >= 429:
            return ["Overload"]

        return ""

    def get_filename(self) -> str:
        """Gets the filename for the crawled data to be stored"""
        while True:
            file_name = "".join(
                random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                for _ in range(13)
            )

            if not Path(f"{self.to_parse_directory}/{file_name}.txt").exists():
                return file_name
