import time as _time
import queue as _queue
import typing as _typing
import threading as _threading
import pymongo.database as _database
import models.queue as _queue_collection
import models.crawled as _crawled_collection


# !This is the main crawler
class Crawler:
    """
    This is the main crawler.
    """

    # !Variables
    max_number_of_threads = 0
    to_parse_directory = ""
    db: _database.Database[_typing.Dict[str, _typing.Any]]
    queue: _typing.List[_typing.Dict[str, str | float]] = []
    crawled: _typing.List[_typing.Dict[str, str | float]] = []
    threadTasks: _queue.Queue[float] = _queue.Queue()

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
        queue = _queue_collection.Queue(self.db)
        crawled = _crawled_collection.Crawled(self.db)

        self.queue = queue.get()
        self.crawled = crawled.get()

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
            for item in self.queue[:10]:
                print(item)
                self.threadTasks.put(float(item["id"]))

            # !Waits for all tasks to be completed
            self.threadTasks.join()

            # !Waits for 10 seconds before continuing
            _time.sleep(10)

    # !Pick a website from queue and crawl it
    def crawl_work(self) -> _typing.NoReturn:
        """Picks a website from queue and crawl it"""
        while True:
            link_in_db = [item for item in self.queue if item["id"] == self.threadTasks.get()][0]

            print(link_in_db)

            self.threadTasks.task_done()
