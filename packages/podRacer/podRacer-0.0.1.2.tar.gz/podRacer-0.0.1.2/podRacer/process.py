## IMPORTS
if 'Imports':

    if 'Standard Python Library':
        import feedparser                   # parses rss feed
        import os                           # local file operations, mainly os.path.join
        from datetime import datetime       # formats dates, such as podcast episode pubDates

    if 'External Dependancy':
        import validators                   # validates links to see if they're valid URL's

    if 'Local File':
        from ._appdata import *                    # stores local application data, like global variables
        from .organize import Organize       # podRacer lib - handles various organization tasks
        from .settings import Settings       # podRacer lib - handles lib usage settings, such as error logging

## HANDLES FETCH REQUESTS
class Process:

    ## INITIALIZE CLASS
    def __init__(self):
        self.organize = Organize()
        self.settings = Settings()

    ## PARSES RSS FEED
    def parse_feed(self, feed):
        if validators.url(feed):
            rss_feed = feedparser.parse(feed)
            if rss_feed['bozo']:
                self.settings.error("Invalid 'feed'", "The URL is either invalid or unreachable", f"{feed}", "https://rss.nytimes.com/services/xml/rss/nyt/US.xml")
                return None
            return rss_feed
        elif str(feed).endswith(('.xml', '.rss')):
            with open(feed, 'r', encoding='utf-8') as file:
                content = file.read()
            return feedparser.parse(content)
        else:
            return None

    ## RUN A FETCH REQUEST
    def request(self, rss_feeds):

        ## CHECK IF STRING OR A LIST
        if isinstance(rss_feeds, str):
            rss_feeds = [rss_feeds]

        ## ITERATE THROUGH RSS FEEDS
        for rss_feed in rss_feeds:

            ## PARSE RSS FEED
            rss_data = self.parse_feed(rss_feed)

            ## GATHER DATA
            self.metadata = self.get_show_metadata(rss_data)
            self.episodes = self.get_episodes_metadata(rss_data)
            self.links = self.get_episode_links(rss_data)

            ## SHOW DIRECTORIES
            self.show_directories = self.get_show_dirs(self.metadata['title'])

            ## CLEAR METADATA DIRECTORY
            self.organize.dir_clear(self.show_directories['metadata_dir'], metadata_only=True)

            ## WRITE SHOW INFO FILE
            self.write_metadata('info',
                (
                    "<Title>\n"
                    f"{self.metadata['title']}\n\n"
                    "<Author>\n"
                    f"{self.metadata['author']}\n\n"
                    "<Latest Episode>\n"
                    f"{self.metadata['latest_ep']}\n\n"
                    "<Description>\n"
                    f"{self.metadata['description']}\n\n"
                )
            )

            ## WRITE METADATA TO FILE
            for x in range(len(self.episodes)):

                ## DETERMINE EPISODE NUMBER
                ep_num = len(self.episodes) - x

                ## EPISODE TITLES
                ep_title = self.organize.text_strip_tags(self.episodes[x]['title'])
                self.write_metadata('episode_titles', str(ep_title).strip() + "\n")

                ## EPISODE DESCRIPTIONS
                ep_desc = self.organize.text_strip_tags(self.episodes[x]['description'])
                self.write_metadata('episode_descriptions', f"-\nEpisode {ep_num}: {str(ep_title)}\n-\n{str(ep_desc).strip()}" + "\n")

                ## EPISODE LINKS
                ep_link = self.links[x]
                self.write_metadata('links', f"{ep_link}\n")

    ## CREATES AND RETURNS SHOW DIRS
    def get_show_dirs(self, show_title):

        ## INITIALIZE DICT
        show_dirs = {}

        ## CLEAN SHOW TITLE
        show_title = self.organize.text_remove_specials(show_title)

        ## SHOW DIRECTORIES
        show_dirs['show_dir'] = os.path.join(APP_DIR, show_title)
        show_dirs['audio_dir'] = os.path.join(show_dirs['show_dir'], 'audio')
        show_dirs['metadata_dir'] = os.path.join(show_dirs['show_dir'], 'metadata')

        ## CREATE DIRECTORIES
        self.organize.dir_create(APP_DIR, show_dirs['show_dir'], audio_dir=False, metadata_dir=True)

        ## RETURN SHOW DIRS
        return show_dirs

    ## RETURNS SHOW METADATA DICT
    def get_show_metadata(self, feed):

        ## INITIALIZE DICT
        metadata = {}

        ## INITIALIZE CHANNEL
        channel = feed.get('channel', {})

        ## READ METADATA
        metadata['title'] = channel.get('title', 'Unknown')
        metadata['author'] = channel.get('itunes_author') or channel.get('author', 'Unknown')
        metadata['description'] = channel.get('description')
        metadata['latest_ep'] = self.get_latest_episode_date(feed)

        ## RETURN METADATA DICT
        return metadata

    ## RETURNS EPISODES LIST
    def get_episodes_metadata(self, feed):

        ## INITIALIZE LIST
        episodes = []

        ## ITERATE THROUGH EVERY EPISODE
        for entry in feed.entries:
            episode = {}
            episode['title'] = self.organize.text_clean_metadata(entry.title)
            episode['description'] = self.organize.text_clean_metadata(entry.description)
            episode['pubdate'] = entry.get('published', 'Unknown')
            episodes.append(episode)

        ## RETURN LIST
        return episodes

    ## GETS THE DATE OF THE MOST RECENT EPISODE
    def get_latest_episode_date(self, feed):

        ## INITIALIZE LATEST PUB DATE
        latest_pub_date = None

        ## ITERATE THROUGH FEED ENTRIES
        for entry in feed.entries:

            ## TRY TO PARSE 'PUBDATE'
            if 'pubDate' in entry:
                try:
                    latest_pub_date = datetime.strptime(entry.pubDate, '%a, %d %b %Y %H:%M:%S %z')
                except (TypeError, ValueError):
                    pass

            ## OTHERWISE, TRY TO PARSE 'PUBLISHED'
            if not latest_pub_date and 'published' in entry:
                try:
                    latest_pub_date = entry.published
                except (TypeError, ValueError):
                    pass

        ## RETURN LATEST EPISODE DATE
        return latest_pub_date

    ## RETURNS LIST OF EPISODE LINKS
    def get_episode_links(self, feed):

        ## INITIALIZE LIST
        links = []

        ## FIND URL
        for x in range(len(feed.entries)):
            for link in feed.entries[x].links:
                if 'audio' in link.type:
                    links.append(link.href)
                    break

        ## RETURN LIST OF LINKS
        return links

    ## WRITES METADATA TO TEXT FILE
    def write_metadata(self, data_type, text):

        ## FORMAT SHOW TITLE
        show_title = str(self.organize.text_remove_specials(self.metadata['title'])).lower()
        show_title = self.organize.text_replace_spaces(show_title)

        ## METADATA FILE
        metadata_file = os.path.join(self.show_directories['metadata_dir'], f'{show_title}_{data_type}.txt')

        ## WRITE TO FILE
        with open(metadata_file, "a+") as file:
            file.write(text)
