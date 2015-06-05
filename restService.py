import sqlite3
import web
import json
import mimerender
import datetime
import os
from parse import *

mime = mimerender.WebPyMimeRender()

dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date)
    else None)
render_json = lambda result: json.dumps(result, default=dthandler)
render_xml = lambda result: '<message>%s</message>' % result

urls = (
    '/metrics', 'Metrics',
    '/metrics/(.*)', 'MetricsSpecificRfId'
)
app = web.application(urls, globals())

def error_processor(handler):
    try:
        return handler()
    except Exception as e:
        return {'error_message': e.message}

app.add_processor(error_processor)

db_path = os.path.dirname(os.path.abspath(__file__)) + '/user_votes.db'
print('DB path: ' + db_path)
db = web.database(dbn='sqlite', db=db_path)


class Metrics:
    @mime(
        default='json',
        json=render_json,
        xml=render_xml
    )
    def GET(self):
        params = web.input()
        date = None
        date_to = None
        if 'date' in params:
            date = params.date
        if 'dateTo' in params:
            date_to = params.dateTo
        return lookup_data(None, date, date_to)


class MetricsSpecificRfId:
    @mime(
        default='json',
        json=render_json,
        xml=render_xml
    )
    def GET(self, rf_id):
        params = web.input()
        date = None
        date_to = None
        if 'date' in params:
            date = params.date
        if 'dateTo' in params:
            date_to = params.dateTo
        return lookup_data(rf_id, date, date_to)

def check_date(arg, name):
    result = parse('{:ti}', arg)
    if not result or type(result[0]) is not datetime.datetime:
        raise TypeError(name + ' has incorrect format')

def lookup_data(rf_id=None, date=None, date_to=None):
    if date:
        check_date(date, 'date')
    if date_to:
        check_date(date_to, 'date_to')

    var_dict = dict(rf_id=rf_id, date=date, date_to=date_to)
    rf_id_part = ''
    if rf_id:
        rf_id_part = 'rf_id = $rf_id '

    date_part = ''
    if date_to and date:
        date_part = 'vote_timestamp between $date and $date_to '
    elif date:
        date_part = 'date(vote_timestamp) = $date '

    where_part = ''
    if rf_id_part or date_part:
        where_part = 'where '

    and_part = ''
    if rf_id_part and date_part:
        and_part = 'and '

    results = db.query(
        'select rf_id, vote, vote_timestamp from user_votes ' + where_part +
        rf_id_part + and_part + date_part, var_dict)

    new_dict = []
    for single in results.list():
        new_dict.append(dict(rf_id=single.rf_id, vote=single.vote, timestamp=str(single.vote_timestamp)))

    print(new_dict)

    return dict(result=new_dict)


if __name__ == '__main__':
    app.run()