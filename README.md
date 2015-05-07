# voting-machine

metrics rest service has following uri:

ip:port/metrics - retrieves all data from db

ip:port/metrics?date=2015-05-07 - retrieves data from db for specified date (date format 'YYYY-MM-DD')

ip:port/metrics?date=2015-05-01&dateTo=2015-05-07 - retrieves data from db for specified date range

ip:port/metrics/{persons_card_code} - retrieves all data from db for specific person

date query parameters are the same for specific person data uri
