from datetime import datetime


def not_regularly_updating(last_updated):
    today = datetime.now()
    return ((today - last_updated)/60).round > 10
