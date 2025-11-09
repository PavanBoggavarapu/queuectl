import datetime

def current_timestamp():
    return datetime.datetime.utcnow().isoformat()

def print_header(title):
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)
