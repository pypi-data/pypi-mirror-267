## IMPORTS
if 'Imports':

    if 'Standard Python Library':
        import os                                           # local file operations, mainly os.path.join
        from concurrent.futures import ThreadPoolExecutor   # handles concurrent download queue
        from concurrent.futures import as_completed         # handles the completion of items in queues

    if 'External Dependancy':
        import requests                                     # handles various web requests
        from tqdm import tqdm                               # handles progress bars for various operations

    if 'Local File':
        from .organize import Organize                       # podRacer lib - handles various organization tasks
        from .settings import Settings                       # podRacer lib - handles lib usage settings, such as error logging

## DOWNLOAD QUEUE FOR PODCAST AUDIO FILES
class AudioQueue:

    ## INITIALIZE THE QUEUE WITH A NUMBER OF WORKERS
    def __init__(self, max_workers=1):

        ## INIT CLASSES
        self.organize = Organize()
        self.settings = Settings()

        ## CREATE A THREAD POOL EXECUTOR
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        ## INITIALIZE A LIST TO TRACK FUTURE DOWNLOAD TASKS
        self.futures = []

    ## BENCHMARK DOWNLOAD
    def benchmark(self, episodes, audio_dir, total_episodes):

        ## GRAB THE 5 LATEST EPISODES TO BENCHMARK
        benchmark_episodes = episodes[:5]

        ## INITIALIZE FILE PATHS
        file_paths = []

        ## START PROGRESS BAR
        self.organize.text_newline(1)
        progress_bar = tqdm(
            total=len(benchmark_episodes),
            desc="\033[1;34mAnalyzing Server Response\033[0m",  # Blue and bold text
            ascii="►▻▸▹",
            unit="ep",
            ncols=40,
            bar_format="{l_bar}{bar}| {n_fmt}"
        )

        ## ITERATE THROUGH EACH EPISODE
        for i, episode in enumerate(benchmark_episodes):

            ## CORRECT EPISODE ORDER
            correct_episode_number = total_episodes - i

            ## START DOWNLOAD (RETURNS FILENAME)
            filename = self.start(episode, audio_dir, correct_episode_number, skip_existing=False)

            ## UPON A COMPLETED DOWNLOAD
            if filename:

                filename = self.organize.text_remove_specials(filename)
                filename = f"Episode {correct_episode_number} - {filename}"

                ## GET THE FULL FILE PATH
                file_path = os.path.join(audio_dir, filename + '.mp3')

                ## ADD THE FILE SIZE TO FILE SIZE LIST
                file_paths.append(file_path)

            ## UPDATE PROGRESS BAR
            progress_bar.update(1)

        ## END PROGRESS BAR
        progress_bar.close()

        ## GET THE TOTAL SIZE OF DOWNLOADED FILES
        file_sizes = self.organize.file_size(file_paths)

        ## SEND FILE SIZES TO CALCULATE WORKERS
        return self.calculate_workers(file_sizes)

    ## CALCULATES MAX THREAD WORKERS BASED ON FILE SIZE AVERAGE
    def calculate_workers(self, file_sizes):

        ## DEFAULT TO 1 WORKER IF NO FILES
        if not file_sizes:
            return 1

        ## AVERAGE FILE SIZE IN BYTES
        average_size_bytes = sum(file_sizes) / len(file_sizes)

        ## AVERAGE FILE SIZE IN MEGABYTES
        average_size_mb = average_size_bytes / (1024 * 1024)

        ## CALCULATE MAX WORKERS
        if average_size_mb < 10:     # 100
            max_workers = 100
        elif average_size_mb < 25:   # 50
            max_workers = 50
        elif average_size_mb < 50:   # 25
            max_workers = 25
        elif average_size_mb < 100:  # 10
            max_workers = 10
        elif average_size_mb < 300:  # 5
            max_workers = 5
        elif average_size_mb < 500:  # 2
            max_workers = 2
        else:
            max_workers = 1          # 1
        return max_workers

    ## DOWNLOAD AN INDIVIDUAL EPISODE
    def start(self, episode, audio_dir, episode_number, skip_existing=False):

        ## ATTEMPT DOWNLOAD
        try:
            ## EXTRACT THE EPISODE TITLE AND PREPARE THE FILENAME
            title = episode.title
            filename = self.organize.text_remove_specials(title)
            if episode_number:
                filename = f"Episode {episode_number} - {filename}"

            ## LOCATE THE AUDIO URL FROM THE EPISODE LINKS
            audio_url = None
            for link in episode.links:
                if 'audio' in link.type:
                    audio_url = link.href
                    break
            if not audio_url:
                return

            ## CHECK IF FILE ALREADY EXISTS
            full_save_path = os.path.join(audio_dir, filename + '.mp3')
            if skip_existing and os.path.exists(full_save_path):
                return title  # Return the title to indicate the file already exists

            ## DOWNLOAD THE EPISODE AND WRITE TO FILE
            response = requests.get(audio_url, stream=True)
            with open(full_save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            ## RETURN DOWNLOADED EPISODE TITLE
            if os.path.getsize(full_save_path) > 0:
                return title
            else:
                self.settings.error("Download completed, but file is empty!",
                        "Could happen if the download link wasn't parsed correctly, or if the server is unresponsive",
                        full_save_path,
                        "Title of the downloaded episode",
                        "Try running 'podRacer.Process.request()' and verify server response and check the audio links")
                return None

        ## HANDLE EXCEPTIONS
        except Exception as error:
            self.settings.error(error,
                    caught_input=f"Episode Number = {episode_number}, Audio Dir = {audio_dir}",
                message="Try running 'podRacer.Process.request()' and verify server response and check the audio links")
            return None

    ## ADD DOWNLOAD TO THE QUEUE
    def add(self, episode, audio_dir, episode_number, skip_existing=False):

        ## SUBMIT A DOWNLOAD TASK TO THE EXECUTOR
        future = self.executor.submit(self.start, episode, audio_dir, episode_number, skip_existing)

        ## APPEND THE FUTURE TO THE TRACKING LIST
        self.futures.append(future)

    ## DOWNLOAD PROGRESS BAR
    def progress_bar(self, total_episodes, desc):

        ## INITIALIZE A PROGRESS BAR
        progress_bar = tqdm(
            total=total_episodes,
            desc="\033[1;33m" + desc + "\033[0m",  # Yellow and bold text
            unit="ep"
        )

        ## WAIT FOR EACH FUTURE TO COMPLETE AND UPDATE PROGRESS BAR
        for future in as_completed(self.futures):
            result = future.result()  # OPTIONAL: HANDLE RESULT
            progress_bar.update(1)

        ## CLOSE THE PROGRESS BAR ONCE ALL DOWNLOADS ARE COMPLETE
        progress_bar.close()

## GENERAL DOWNLOAD QUEUE
class Queue:

    ## INITIALIZE THE QUEUE WITH A NUMBER OF WORKERS
    def __init__(self, max_workers=1):

        ## INIT CLASSES
        self.organize = Organize()
        self.settings = Settings()

        ## CREATE A THREAD POOL EXECUTOR
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        ## INITIALIZE A LIST TO TRACK FUTURE DOWNLOAD TASKS
        self.futures = []

    ## DOWNLOAD AN INDIVIDUAL FILE
    def start(self, url, path):

        ## ATTEMPT DOWNLOAD
        try:

            ## DOWNLOAD THE FILE
            response = requests.get(url, stream=True)
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            ## RETURN DOWNLOADED FILENAME
            if os.path.getsize(path) > 0:
                return str(url).split('/')[-1]
            else:
                self.settings.error("Download completed, but file is empty!",
                        "Could happen if the download link wasn't parsed correctly, or if the server is unresponsive",
                        path,
                        "Title of the downloaded file",
                        "Try running 'podRacer.Process.request()' and verify server response and check the links")
                return None

        ## HANDLE EXCEPTIONS
        except Exception as error:
            self.settings.error(error,
                    caught_input=f"-",
                message="Try running 'podRacer.Process.request()' and verify server response and check the links")
            return None

    ## ADD DOWNLOAD TO THE QUEUE
    def add(self, url, path):

        ## SUBMIT A DOWNLOAD TASK TO THE EXECUTOR
        future = self.executor.submit(self.start, url, path)

        ## APPEND THE FUTURE TO THE TRACKING LIST
        self.futures.append(future)

    ## DOWNLOAD PROGRESS BAR
    def progress_bar(self, total_files, desc):

        ## INITIALIZE A PROGRESS BAR
        progress_bar = tqdm(
            total=total_files,
            desc="\033[1;33m" + desc + "\033[0m",  # Yellow and bold text
            unit="ep"
        )

        ## WAIT FOR EACH FUTURE TO COMPLETE AND UPDATE PROGRESS BAR
        for future in as_completed(self.futures):
            result = future.result()  # OPTIONAL: HANDLE RESULT
            progress_bar.update(1)

        ## CLOSE THE PROGRESS BAR ONCE ALL DOWNLOADS ARE COMPLETE
        progress_bar.close()