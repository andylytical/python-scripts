# Build a layered cake

import libutil
import random
import argparse
import logging
import pprint


# module level resources
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
        resources[key] = parser.parse_args()
    return resources[key]


def mk_candles( qty=0, num_lit=0, width=0 ):
    ''' Make a string that represents candles.
        qty = total number of candles
        num_lit = number of candles that should be burning
    '''
    if qty < 0:
        raise UserWarning( 'num candles cant be less than 0' )
    if num_lit > qty:
        raise UserWarning( 'num_lit cannot be > than total candles' )
    if width < 1:
        width = (qty * 2) + 2
    lines = []
    # initially, all flames are empty (not lit)
    flames = [' '] * qty
    # create list of possible flame positions
    available_positions = [ x for x in range( qty ) ]
    # choose random positions to be lit
    for i in random.sample( available_positions, num_lit ):
        flames[i] = '@'
    lines.append( f" {' '.join( flames )}" )
    sticks = ' |' * qty
    lines.append( sticks )
    for l in lines:
        print( l.center( width ) )


def test_candles():
    print()
    logging.debug( 'test no candles' )
    mk_candles()

    print()
    logging.debug( 'test no candles lit' )
    for i in (3,5):
        mk_candles(i)

    print()
    logging.debug( 'test all candles lit' )
    for vals in ( (2,2), (4,4) ):
        mk_candles( *vals )

    # test random candle placement
    test_tuples = ( (5,3), (8,5), (12,4), (15,2) )
    for vals in test_tuples:
        print()
        logging.debug( f'test random lit candles {vals}' )
        for i in range(3):
            mk_candles( *vals )


def mk_header( width, char, bookends='' ):
    edge_size = len( bookends ) * 2
    width_size = width - edge_size
    parts = [ bookends ]
    parts.append( char * width_size )
    parts.append( bookends )
    print( ''.join( parts ) )


def mk_meat( width ):
    mk_header( width, ' ', bookends='|' )


def mk_icing( width ):
    mk_header( width, '<' )


def mk_layer( width ):
    mk_icing( width )
    mk_meat( width )


def mk_bottom( width ):
    mk_header( width, '=' )


def mk_cake( num_guests=2, layers=1, num_candles=1, lit_candles=1 ):
    if num_guests < 1:
        raise UserWarning( 'num_guests cannot be less than 1' )
    if layers < 1:
        raise UserWarning( 'layers cannot be less than 1' )
    if num_candles < 1:
        raise UserWarning( 'num_candles cannot be less than 1' )
    if lit_candles < 0:
        raise UserWarning( 'lit_candles cannot be less than 0' )
    if lit_candles > num_candles:
        raise UserWarning( 'num_candles cannot be greater than total candles' )
    width = 6 + ( num_guests * 2 )
    mk_candles( num_candles, lit_candles, width )
    for i in range( layers ):
        mk_layer( width )
    mk_bottom( width )


if __name__ == '__main__':
    args = get_args()
    libutil.setup_logging( args )

    # test_candles()

    # test cake
    for i in range(3):
        guests = random.randint(1,10)
        candles = random.randint( 1, guests+2 )
        parms = {
            'layers': random.randint(1,6),
            'num_guests': guests,
            'num_candles': candles,
            'lit_candles': random.randint( 1, candles ),
            }
        logging.debug( pprint.pformat( parms ) )
        mk_cake( **parms )


