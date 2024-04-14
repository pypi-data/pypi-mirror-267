## IMPORTS
if 'Imports':

    if 'Standard Python Library':
        import os                           # local file operations, mainly os.path.join
        from urllib.parse import urlparse

    if 'Local File':
        from ._appdata import *                  # stores local application data, like global variables
        from .download_queue import AudioQueue, Queue   # podRacer lib - handles queues for download operations
        from .organize import Organize       # podRacer lib - handles various organization tasks
        from .process import Process         # podRacer lib - processes requests for rss feeds
        from .settings import Settings       # podRacer lib - handles lib usage settings, such as error logging

## HANDLES DOWNLOADS
class Download:

    ## INITIALIZE CLASS
    def __init__(self):
        self.process = Process()
        self.organize = Organize()
        self.settings = Settings()

    ## DOWNLOAD A PODCAST
    def podcast(self, feed:str, queue_size:int=None, destination:str=APP_DIR):
        """
        Downloads all episodes from a podcast feed.

        Parameters:
            feed (str): URL or local file path to the podcast feed.
            queue_size (int): Number of concurrent downloads.
            destination (str): Path to the directory where the podcast will be saved.

        Examples:
            >>> # Automatically set concurrent downloads
            >>> podcast('https://example.com/podcast.xml')
            >>> # Download 5 episodes concurrently
            >>> podcast('https://example.com/podcast.xml', 5)
            >>> # Save podcast to a specific directory
            >>> podcast('https://example.com/podcast.xml', destination='~/Downloads')

        Notes:
            - By default, the '~/podRacer' directory is used as the destination.
            - Files are separated into their own sub-directories based on their kind ['audio', 'metadata', 'images', etc.]
        """

        ## PARSE RSS FEED
        rss = self.process.parse_feed(feed)

        ## VALID RSS
        if rss:

            ## CLEAN SHOW TITLE
            show_title = self.organize.text_remove_specials(rss.feed.title)

            ## SET SHOW DIRECTORY (AND CREATE IMAGES DIR)
            show_dir = self.organize.dir_paths(os.path.join(destination, show_title), 'audio')

        ## INVALID RSS
        else:
            self.settings.error("Invalid 'feed'",
                                "The URL is either invalid or unreachable",
                                f"{feed}",
                                "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
                                "If the URL is correct, check to see if it requires any special type of access, like a password or API key")
            return None

        ## GET ALL EPISODES
        total_episodes = len(rss.entries)

        ## START DOWNLOAD
        queue = AudioQueue(max_workers=10)  # Initial max workers

        ## BENCHMARK DOWNLOAD QUEUE AND ADJUST MAX WORKERS ACCORDINGLY
        if not queue_size:
            max_workers_after_benchmark = queue.benchmark(rss.entries, show_dir['audio'], total_episodes)
            queue.executor._max_workers = max_workers_after_benchmark
        else:
            try:
                queue.executor._max_workers = int(queue_size)
            except ValueError:
                self.settings.error("Invalid 'queue_size'", "Your 'queue_size' is not a valid integer", f"{queue_size}", "1, 5, 12, 26, 154, [etc.]")
                return None

        ## ADD EPISODES TO DOWNLOAD QUEUE
        for episode_number, episode in enumerate(rss.entries, start=1):
            correct_episode_number = total_episodes - episode_number + 1
            queue.add(episode, show_dir['audio'], correct_episode_number, skip_existing=True)

        ## START PROGRESS BAR
        queue.progress_bar(total_episodes, desc=f"Downloading Podcast - {rss.feed.title}")

    ## DOWNLOAD SELECT EPISODES FROM A PODCAST
    def episode(self, feed:str, *episode_args, destination:str=APP_DIR):
        """
        Downloads specific episodes from a podcast feed.

        Parameters:
            feed (str): URL or local file path to the podcast feed.
            episode_args (list): List of episode numbers or ranges to download.
            destination (str): Path to the directory where the podcast will be saved.

        Examples:
            >>> # Download a single episode
            >>> episode('https://example.com/podcast.xml', 20)
            >>> # Download episodes 20, 25, 10 through 15, 100, 102, and 150 through 180
            >>> episode('https://example.com/podcast.xml', 20, '25', '10-15', [100, 102, '150-180'])
            >>> # Save podcast to a specific directory
            >>> episode('https://example.com/podcast.xml', 20, destination='~/Downloads')

        Notes:
            - By default, the '~/podRacer' directory is used as the destination.
            - Files are separated into their own sub-directories based on their kind ['audio', 'metadata', 'images', etc.]
        """

        ## PARSE RSS FEED
        rss = self.process.parse_feed(feed)

        ## VALID RSS
        if rss:

            ## TOTAL NUMBER OF EPISODES
            total_episodes = len(rss.entries)

            ## CLEAN SHOW TITLE
            show_title = self.organize.text_remove_specials(rss.feed.title)

            ## SET SHOW DIRECTORY (AND CREATE AUDIO DIR)
            show_dir = self.organize.dir_paths(os.path.join(destination, show_title), 'audio')

        ## INVALID RSS
        else:
            self.settings.error("Invalid 'feed'",
                                "The URL is either invalid or unreachable",
                                f"{feed}",
                                "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
                                "If the URL is correct, check to see if it requires any special type of access, like a password or API key")
            return None

        ## CREATE EPISODE LIST
        try:
            episode_numbers = self.organize.list_episodes_to_download(episode_args, total_episodes)
        except ValueError as error:
            self.settings.error(error,
                                'Invalid episode number or range',
                                f"{episode_args}",
                                "20, '20', '10-15', [1, 2, '3-5']",
                                'Use integers, strings, or ranges')
            return None

        ## UPDATE PROGRESS BAR TEXT IF MORE THAN ONE EPISODE
        desc = f"{rss.feed.title} | Downloading {len(episode_numbers)} Episodes" if len(episode_numbers) > 1 else f"{rss.feed.title} | Episode {episode_numbers[0]} - {rss.entries[total_episodes - episode_numbers[0]]['title']}"

        ## START DOWNLOAD QUEUE
        queue = AudioQueue(max_workers=10)
        for episode_number in episode_numbers:
            episode_index = total_episodes - episode_number
            episode = rss.entries[episode_index]
            queue.add(episode, show_dir['audio'], episode_number, skip_existing=True)

        ## START PROGRESS BAR
        queue.progress_bar(len(episode_numbers), desc=desc)

    ## DOWNLOAD IMAGES FROM A PODCAST
    def images(self, feed:str, destination:str=APP_DIR):

        ## PARSE RSS FEED
        if not type(feed).__name__ == 'FeedParserDict':
            rss = self.process.parse_feed(feed)
        else:
            rss = feed

        ## VALID RSS
        if rss:

            ## CLEAN SHOW TITLE
            show_title = self.organize.text_remove_specials(rss.feed.title)

            ## SET SHOW DIRECTORY (AND CREATE IMAGES DIR)
            show_dir = self.organize.dir_paths(os.path.join(destination, show_title), 'images')

        ## INVALID RSS
        else:
            self.settings.error("Invalid 'feed'",
                                "The URL is either invalid or unreachable",
                                f"{feed}",
                                "If the URL is correct, check to see if it requires any special type of access, like a password or API key")
            return None

        ## GET ALL EPISODES
        total_episodes = len(rss.entries)

        ## START DOWNLOAD
        queue = Queue(max_workers=10)  # Initial max workers

        ## ADD EPISODES TO DOWNLOAD QUEUE
        for episode_number, entry in enumerate(rss.entries, start=1):
            correct_episode_number = total_episodes - episode_number + 1
            title = entry.title if hasattr(entry, 'title') else f"Episode {episode_number}"
            image_elem = entry.get('image', None)
            if image_elem:
                image_url = image_elem.get('href')
                if image_url:
                    image_file_name = f"Episode {correct_episode_number} - {title}" + os.path.splitext(urlparse(image_url).path)[-1]
                    image_path = os.path.join(show_dir['images'], image_file_name)
                    queue.add(image_url, image_path)

        ## START PROGRESS BAR
        queue.progress_bar(total_episodes, desc=f"Downloading Images - {rss.feed.title}")
