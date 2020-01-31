import os
import collections
import datetime

from exchangelib import Account, EWSTimeZone, EWSDateTime

from commons import load_configuration, process_messages, login, log


def backup_messages(account: Account, until: datetime.date, clean_up=False):
    base_dir = 'account'
    inbox_dir = os.path.join(base_dir, 'inbox')
    sent_dir = os.path.join(base_dir, 'sent')
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(inbox_dir, exist_ok=True)
    os.makedirs(sent_dir, exist_ok=True)

    tz = EWSTimeZone.localzone()
    start_date = tz.localize(EWSDateTime(2000, 1, 1))
    end_date = tz.localize(EWSDateTime(until.year, until.month, until.day))

    qs = account.inbox \
             .filter(datetime_received__range=(start_date, end_date)) \
             .order_by('datetime_received') \
             .only('mime_content', 'sender', 'subject', 'datetime_received')

    r1 = process_messages(qs, base_dir=inbox_dir, clean_up=clean_up, backup=True)

    qs = account.sent.all() \
             .filter(datetime_received__range=(start_date, end_date)) \
             .order_by('datetime_received') \
             .only('mime_content', 'sender', 'subject', 'datetime_received')

    r2 = process_messages(qs, base_dir=sent_dir, clean_up=clean_up, backup=True)

    counter = collections.Counter()
    for d in [r1, r2]:
        counter.update(d)

    return dict(counter)


if __name__ == '__main__':
    conf_file = 'conf.yml'
    conf = load_configuration(conf_file)
    if not conf:
        exit(1)

    months = int(conf['backup']['months'])
    delete_messages = conf['backup']['delete']
    date_limit = datetime.date.today() - datetime.timedelta(months * 365 / 12)

    log.info("Connecting...")
    account = login(conf)
    log.info("Downloading until %s..." % date_limit)
    tot = backup_messages(account, clean_up=delete_messages, until=date_limit)
    log.info("Done: %s" % tot)
