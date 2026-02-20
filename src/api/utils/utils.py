from datetime import datetime

def parse_date(date_string, end_of_day=False):
    """
    utility for parsing date strings into YYYY-MM-DD format.
    
    :param date_str: date string to parse into YYYY-MM-DD format
    :param end_of_day: flag for setting time to 00:00:00 (False) or 23:59:59 (True)
    """

    if not date_string:
        return None
    
    formats = [
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%m.%d.%Y',
        '%m/%d/%Y',
        '%m-%d-%Y',
        '%Y.%m.%d',
        '%Y/%m/%d',
        '%Y-%m-%d',
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_string, fmt)
            if end_of_day:
                parsed = parsed.replace(hour=23, minute=59, second=59)
            else:
                parsed = parsed.replace(hour=0, minute=0, second=0)
            return parsed.isoformat()
        except ValueError:
            continue

    raise ValueError(f"Could not parse date: '{date_string}'")