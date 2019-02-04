
from datetime import timedelta
import datetime
import dateutil.parser


def interpretDatetime(strdate) :
    # transform format 2018-11-29T08:54:16.000Z in datetime
    return dateutil.parser.parse(strdate).replace(tzinfo=None)

def mainfunction(apis, logger, previous) :
    tomorow = (datetime.datetime.now().replace(tzinfo=None) + timedelta(days=1)).date()
    today = datetime.datetime.now().date()
    startWeek = today - timedelta(days=today.weekday())
    endWeek = startWeek + timedelta(days=6)
    # logger.log('{0}'.format(tomorow))
#    boards = [(board.id, board.name for board in apis['trello'].list_boards()]
    board = apis['trello'].get_board('5894b4f714a250f7fa32129d')
    lists =  board.list_lists()
    cards = [card for list in lists for card in list.list_cards()]
    
    cards = [ card for card in cards if (card.due)]
#    cards = [ interpretDatetime(card.due).isoformat() for card in cards if (card.due)]
    
    cards_delayed = [ card for card in cards if  interpretDatetime(card.due).date()<=tomorow]
    cards_week = [ card for card in cards if  (interpretDatetime(card.due).date()<=endWeek \
        and interpretDatetime(card.due).date()>=startWeek )]
    
    actions = board.fetch_actions('updateCard', action_limit=200)
    return {'delayed_cards':cards_delayed, 'week_cards':cards_week, 'actions':actions}








