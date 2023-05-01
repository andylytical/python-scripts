import argparse
import libutil
import logging
import mutagen
import mutagen.asf
import mutagen.flac
import mutagen.mp3
import mutagen.oggvorbis
import mutagen.wave
import os
import pathlib
import sys
import unicodedata


# Module level resources
resources = {}


def get_args():
    key = 'args'
    if key not in resources:
        constructor_args = {
            'formatter_class': argparse.RawDescriptionHelpFormatter,
            'description': 'Find files having the given extended tag',
            }
        parser = argparse.ArgumentParser( **constructor_args )
        parser.add_argument( '-d', '--debug', action='store_true' )
        parser.add_argument( '-v', '--verbose', action='store_true' )
        parser.add_argument( '-P', '--show-progress', action='store_true' )
        parser.add_argument( '-t', '--tagname', default='datenight',
            help='tagname to search for' )
        parser.add_argument( '-p', '--prefix', default='//depot/music/Shared',
            help='prefix to add to filenames in the M3U8 playlist output file' )
        parser.add_argument( 'dirpath',
            help='Top level directory of music files' )
        resources[key] = parser.parse_args()
    return resources[key]


def ignore_suffixes():
    key = 'ignore_suffixes'
    if key not in resources:
        resources[key] = [
            '.jpg',
            '.txt',
            '.lrc',
            '.db',
            '.thm',
            ]
    return resources[key]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def update_progress( msg=None ):
    args = get_args()
    if args.show_progress:
        end = ''
        if msg:
            end = ' . '
        eprint( msg, end=end )


def end_progress():
    args = get_args()
    if args.show_progress:
        eprint( '' )


def has_tag( self, tagname ):
    rv = False
    for k,v in self.items():
        if 'datenight' in k.lower():
            rv = True
    return rv
mutagen.asf.ASF.has_tag = has_tag
mutagen.flac.FLAC.has_tag = has_tag
mutagen.mp3.MP3.has_tag = has_tag
mutagen.oggvorbis.OggVorbis.has_tag = has_tag
mutagen.wave.WAVE.has_tag = has_tag


def raiseme( error ):
    raise error


def run():
    args = get_args()
    matches = []
    count = 0
    stop = False
    for root, dirs, files in os.walk( args.dirpath, onerror=raiseme ):
        for fn in files:
            fullpath = pathlib.Path( root, fn )
            if fullpath.suffix in ignore_suffixes():
                logging.debug( f"Skip: {fullpath}" )
                continue
            count = count + 1
            if count % 100 == 0:
                update_progress( count )
            # if count % 300 == 0:
            #     stop = True
            logging.debug( fullpath )
            audiofile = mutagen.File( fullpath )
            if audiofile.has_tag( args.tagname ):
                relpath = fullpath.relative_to( args.dirpath )
                uncpath = pathlib.PureWindowsPath( args.prefix, relpath )
                matches.append( uncpath )
        if stop:
            break
    end_progress()
    for f in map( str, matches ):
        print(f)

if __name__ == '__main__':
    args = get_args()
    libutil.setup_logging( args )
    run()
