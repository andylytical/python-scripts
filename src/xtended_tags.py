import logging
import mutagen.flac
import mutagen.mp3
import os
import pathlib


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
        parser.add_argument( '-t', '--tagname', default='datenight',
            help='tagname to search for' )
        parser.add_argument( dirpath,
            help='Top level directory of music files' )
        resources[key] = parser.parse_args()
    return resources[key]


def setup_logging():
    args = get_args()
    loglvl = logging.WARNING
    if args.verbose:
        loglvl = logging.INFO
    if args.debug:
        loglvl = logging.DEBUG
    fmtstr = '%(levelname)s:%(pathname)s.%(module)s.%(funcName)s[%(lineno)d] %(message)s'
    logging.basicConfig( level=loglvl, format=fmtstr )


def _ends_with( fn, suffix ):
    rv = False
    if fn.lower().endswith( suffix ):
        rv = True
    return rv


def is_flac( fn ):
    return _ends_with( fn, '.flac' )


def is_mp3( fn ):
    return _ends_with( fn, '.mp3' )


def is_tag_present( audiofile, tagname ):
    rv = False
    for k,v in audiofile.items():
        if 'datenight' in k.lower():
            rv = True
    return rv


def run():
    args = get_args()
    for root, dirs, files in os.walk( args.dirpath ):
        for fn in files:
            if is_flac( fn ):
                as_audio = mutagen.flac.FLAC
            elif is_mp3( fn ):
                as_audio = mutagen.mp3.MP3
            else:
                continue

            fullpath = pathlib.Path( root, fn )
            audiofile = as_audio( fullpath )
            if is_tag_present( audiofile, args.tagname ):
                print( fullpath )


if __name__ == '__main__':
    setup_logging()
    run()
