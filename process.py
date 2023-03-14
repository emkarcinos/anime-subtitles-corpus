import os
import shutil
import itertools
import zipfile
import re
import gzip
from tqdm import tqdm
from pyunpack import Archive
from config import SUBTITLE_ZIP_OUTPUT, SUBTITLE_EXTRACTS_OUTPUT, POST_EXTRACTION_WHITELIST, OUTPUT_FILE
from scrape import preprare_folder
from pysubparser import parser
from pysubparser.cleaners import brackets, formatting, lower_case
import pysubparser.classes.exceptions as parser_exceptions


def extract_all(path: str, output_dir: str):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in tqdm(files):
        try:
            archive = Archive(f'{path}{file}')
            archive.extractall(output_dir)
        except zipfile.BadZipFile:
            pass


def flatten_directory(folder: str):
    all_files = []
    for root, _, files in itertools.islice(os.walk(folder), 1, None):
        for filename in files:
            all_files.append(os.path.join(root, filename))
    for filename in all_files:
        try:
            shutil.move(filename, folder)
        except shutil.Error:
            # There are some duplicates - they don't matter as much, omitting them
            pass


def cleanup_folders(folder: str, whitelist: list[str]):
    for root, _, files in os.walk(folder):
        if root != folder:
            shutil.rmtree(root)
        else:
            for file in files:
                if all(white not in file.lower() for white in whitelist):
                    os.remove(os.path.join(root, file))


CURLY_BRACERS_CLEANER = re.compile(r"\{[^{]*\}", re.UNICODE)
def clean_curly_bracers(subtitles):
    for subtitle in subtitles:
        subtitle.lines = list(
            map(
                lambda line: CURLY_BRACERS_CLEANER.sub("", line).strip(),
                subtitle.lines,
            )
        )

        yield subtitle


def parse(source_file_path: str) -> list[str]:
    try:    
        subtitles = parser.parse(source_file_path)
    except parser_exceptions.InvalidSubtitleTypeError:
        print(f'Unsupported file: {source_file_path}. Skipping.')
        return []
    
    try:
        clean_subtitles = clean_curly_bracers(
            brackets.clean(
                lower_case.clean(
                    formatting.clean(
                        subtitles
                    )
                )
            )
        )
        return [subtitle.text for subtitle in clean_subtitles]
    except (UnicodeDecodeError, ValueError):
        print(f'Error processing file {source_file_path}. Skipping.')
        return []


def create_corpus(sources_dir: str, output_file: str):

    with open(output_file, 'a') as f:
        for root, _, files in os.walk(sources_dir):
            for file in files:
                text_content = parse(os.path.join(root, file))
                for line in text_content:
                    f.write(line + '\n')


def compress_corpus(file_path: str):
    with open(file_path, 'rb') as f:
        with gzip.open(f'{file_path}.gz', 'wb') as f_out:
            f_out.writelines(f)


def main():
    preprare_folder(SUBTITLE_EXTRACTS_OUTPUT)

    print('Extracting acrhives...')
    extract_all(SUBTITLE_ZIP_OUTPUT, SUBTITLE_EXTRACTS_OUTPUT)
    print('Flattening the directory tree...')
    flatten_directory(SUBTITLE_EXTRACTS_OUTPUT)

    print('Cleaning up the directory tree...')
    cleanup_folders(SUBTITLE_EXTRACTS_OUTPUT, POST_EXTRACTION_WHITELIST)
    print('Parsing subtitle files and writing to output file...')
    create_corpus(SUBTITLE_EXTRACTS_OUTPUT, OUTPUT_FILE)
    print('Compressing...')
    compress_corpus(OUTPUT_FILE)


if __name__ == '__main__':
    main()
