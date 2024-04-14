## IMPORTS
if 'Imports':

    if 'Standard Python Library':
        import html                         # used to unescape characters from rss feed
        import os                           # local file operations, mainly os.path.join
        import re                           # regular expression, used for string manipulation
        import unicodedata                  # used in tandem with html to fix unicode characters
        from pathlib import Path as Dir     # handles various local dir operations

## HANDLES ORGANIZATION
class Organize:

    if 'Dirs':

        ## CLEARS THE CONTENT WITHIN A DIRECTORY OR A LIST OF DIRECTORIES
        def dir_clear(self, dir_paths, metadata_only=False):

            ## ENSURE DIR_PATHS IS A LIST IF IT IS A SINGLE STRING
            if not isinstance(dir_paths, list):
                dir_paths = [dir_paths]

            ## ITERATE OVER EACH DIRECTORY PATH
            for dir_path in dir_paths:

                ## READ THE CONTENTS OF DIR_PATH
                for root, dirs, files in os.walk(dir_path):
                    for file in files:

                        ## CONSTRUCT FULL PATH TO FILE
                        file_path = os.path.join(root, file)

                        ## CHECK IF WE SHOULD ONLY DELETE METADATA FILES
                        if metadata_only and file.endswith('.txt'):
                            os.remove(file_path)

                        ## DELETE EVERY FILE IN DIRECTORY
                        elif not metadata_only:
                            os.remove(file_path)

        ## CREATES A DIRECTORY OR A LIST OF DIRECTORIES
        def dir_create(self, dir_path, dir_name, audio_dir=False, metadata_dir=False):

            ## CREATES AUDIO / METADATA SUB DIRS
            def create_sub_dirs(base_dir):
                if audio_dir:
                    Dir(base_dir, 'audio').mkdir(parents=True, exist_ok=True)
                if metadata_dir:
                    Dir(base_dir, 'metadata').mkdir(parents=True, exist_ok=True)

            ## SINGLE DIRECTORY
            if isinstance(dir_path, str) and isinstance(dir_name, str):
                base_dir = Dir(dir_path, dir_name)
                base_dir.mkdir(parents=True, exist_ok=True)
                create_sub_dirs(base_dir)

            ## MULTIPLE PATHS, SINGLE DIRECTORY
            elif isinstance(dir_path, list) and isinstance(dir_name, str):
                for path in dir_path:
                    base_dir = Dir(path, dir_name)
                    base_dir.mkdir(parents=True, exist_ok=True)
                    create_sub_dirs(base_dir)

            ## SINGLE PATH, MULTIPLE DIRECTORIES
            elif isinstance(dir_path, str) and isinstance(dir_name, list):
                for name in dir_name:
                    base_dir = Dir(dir_path, name)
                    base_dir.mkdir(parents=True, exist_ok=True)
                    create_sub_dirs(base_dir)

            ## MULTIPLE PATHS, MULTIPLE DIRECTORIES
            elif isinstance(dir_path, list) and isinstance(dir_name, list) and len(dir_path) == len(dir_name):
                for path, name in zip(dir_path, dir_name):
                    base_dir = Dir(path, name)
                    base_dir.mkdir(parents=True, exist_ok=True)
                    create_sub_dirs(base_dir)

            ## ERROR
            else:
                raise ValueError("The path and name of directories must be either both strings or both lists with the same length.")

        def dir_paths(self, dir_path, *create_dirs):

            ## INITIALIZE DICTIONARY
            dir_paths = {}

            ## ROOT DIRECTORY
            dir_paths['root'] = dir_path

            ## MAIN SUBDIRECTORIES
            dir_paths['audio'] = os.path.join(dir_path, 'audio')
            dir_paths['images'] = os.path.join(dir_path, 'images')
            dir_paths['metadata'] = os.path.join(dir_path, 'metadata')

            ## METADATA SUBDIRECTORIES
            dir_paths['links'] = os.path.join(dir_paths['metadata'], 'links')

            ## CHECK IF CREATION ARGS ARE PROVIDED
            if create_dirs:

                ## INITIALIZE SET
                dirs_to_create = set()

                ## HANDLE BOTH LISTS AND SINGLE STRING ARGUMENTS
                flattened_args = [item for sublist in create_dirs for item in (sublist if isinstance(sublist, list) else [sublist])]

                ## CHECK IF ALL DIRECTORIES SHOULD BE CREATED
                if 'all' in flattened_args:
                    dirs_to_create = dir_paths.values()

                ## CREATE SPECIFIC DIRECTORIES
                else:
                    dirs_to_create = {dir_paths[arg] for arg in flattened_args if arg in dir_paths}

                ## CREATE DIRECTORIES
                for path in dirs_to_create:
                    os.makedirs(path, exist_ok=True)

            ## RETURN DICTIONARY
            return dir_paths

    if 'Lists':

        ## GENERATES A FLAT LIST OF EPISODES TO DOWNLOAD
        def list_episodes_to_download(self, episode_args, total_episodes):

            ## INITIALIZE LIST
            flat_list = []

            ## ITERATE THROUGH ALL EPISODES
            for item in episode_args:
                if isinstance(item, list) or isinstance(item, tuple):
                    flat_list.extend(item)
                elif isinstance(item, str) and '-' in item:
                    start, end = map(int, item.split('-'))
                    flat_list.extend(range(start, min(end + 1, total_episodes + 1)))
                else:
                    flat_list.append(int(item))

            ## ENSURES UNIQUE EPISODES
            return [max(1, min(ep, total_episodes)) for ep in set(flat_list)]

    if 'Files':

        ## CHECKS IF FILES EXIST
        def file_exists(self, file_paths, diff_extension=None, require_all=False):

            ## SINGLE FILE
            if not isinstance(file_paths, list):

                ## CHECK IF FILE EXISTS
                if not diff_extension:
                    return os.path.exists(file_paths)

                ## CHECK WITH DIFFERENT EXTENSION
                else:
                    base_path = os.path.splitext(file_paths)[0]
                    new_path = f"{base_path}.{diff_extension}"
                    return os.path.exists(new_path)

            ## LIST OF FILES
            else:

                ## CHECK IF ALL FILES EXIST
                if require_all:
                    return all(
                        os.path.exists(f"{os.path.splitext(file_path)[0]}.{diff_extension}" if diff_extension else file_path)
                        for file_path in file_paths
                    )

                ## RETURN A LIST OF BOOLEAN VALUES
                else:
                    files_exist_list = [
                        os.path.exists(f"{os.path.splitext(file_path)[0]}.{diff_extension}" if diff_extension else file_path)
                        for file_path in file_paths
                    ]
                    return files_exist_list

        ## RETURNS FILE EXTENSIONS
        def file_extension(self, file_paths, include_period=False):

            ## SINGLE FILE
            if not isinstance(file_paths, list):
                return file_paths.split('.')[-1] if '.' in file_paths else ''

            ## LIST OF FILES
            else:

                ## INITIALIZE LIST
                extensions = []

                ## ITERATE THROUGH FILEPATHS
                for file_path in file_paths:
                    extension = file_path.split('.')[-1] if '.' in file_path else ''
                    if include_period:
                        extension = '.' + extension
                    extensions.append(extension)

                ## RETURN LIST
                return extensions

        ## RETURNS FILE SIZE
        def file_size(self, file_paths):

            ## SINGLE FILE
            if not isinstance(file_paths, list):
                return os.path.getsize(file_paths) if os.path.exists(file_paths) else 0

            ## LIST OF FILES
            file_sizes_list = []
            for file_path in file_paths:
                size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                file_sizes_list.append(size)
            return file_sizes_list

    if 'Text':

        ## FIXES EPISODE DESC. FORMATTING
        def text_clean_metadata(self, text):

            ## NORMALIZE UNICODE CHARACTERS
            text = unicodedata.normalize('NFKD', text)

            ## UNESCAPE HTML ENTITITES
            text = html.unescape(text)

            ## REPLACE BACKSLASHES
            text = text.replace("\\", "")

            ## REPLACE NON-BREAKING SPACES AND OTHER WHITESPACES
            text = re.sub(r'\s+', ' ', text)

            ## RETURN TEXT
            return text.strip()

        ## FILTERS OUT A LIST OF SUBSTRINGS
        def text_filter(self, Text: str, Filter: list):
            clean = re.compile('|'.join(map(re.escape, Filter)))
            filtered_Text = clean.sub("", Text).replace('  ', ' ')
            return filtered_Text.strip()

        ## PRINTS A NEWLINE
        def text_newline(self, count):
            for x in range(count):
                print()

        ## REPLACE SPACES WITH UNDERSCORE
        def text_replace_spaces(self, text):
            return str(text).replace(' ', '_')

        ## REMOVES SPECIAL CHARACTERS AND DOUBLE SPACES
        def text_remove_specials(self, text):
            text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        ## STRIPS HTML TAGS FROM TEXT
        def text_strip_tags(self, text):

            ## PREVENT CDATA CONTENT FROM BEING STRIPPED
            text = self.text_filter(text, ['<![CDATA[', ']]>'])

            ## STRIP HTML TAGS
            clean = re.compile('<.*?>')

            ## RETURN (REMOVE WHITESPACE)
            return re.sub(clean, '', text).strip()