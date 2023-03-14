BASE_URL = r'https://www.kitsunekko.net'
PAGE_URL = rf'{BASE_URL}/dirlist.php?dir=subtitles%2F'
SUBTITLE_ZIP_OUTPUT = 'zips/'
SUBTITLE_EXTRACTS_OUTPUT = 'subs/'
MULTITHREAD = True
FILE_TITLES_BLACKLIST = ['font', '.txt', '.srt', '.ass', '.php', '.ssa']
POST_EXTRACTION_WHITELIST = ['.srt', '.ass', '.ssa']
OUTPUT_FILE = 'corpus.txt'
