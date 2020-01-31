
import yaml
import re
import os
import logging.config

from exchangelib import Credentials, Account, Configuration, DELEGATE, EWSTimeZone, EWSDateTime, Message
import exchangelib.services

logging.config.fileConfig('logging.conf')
log = logging.getLogger()

# Dump EWS SOAP
# from exchangelib.util import PrettyXmlHandler
# logging.basicConfig(level=logging.DEBUG, handlers=[PrettyXmlHandler()])


def load_configuration(conf_file):
    with open(conf_file, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError:
            log.error('Problem loading configuration from "%s"' % conf_file, exc_info=True)
    return conf


def login(conf):
    user = "%s\\%s" % (conf['account']['domain'], conf['account']['user'])
    passw = conf['account']['password']
    primary_email_address = conf['account']['email']
    server = conf['ews']['server']
    chunk_size = conf['ews']['chunk']

    exchangelib.services.CHUNK_SIZE = chunk_size
    credentials = Credentials(username=user, password=passw)
    config = Configuration(server=server, credentials=credentials)
    account = Account(primary_email_address, config=config, autodiscover=False, access_type=DELEGATE)
    return account


def safe_file_name(s):
    s = str(s).strip().replace(' ', '_').replace('0000.', '.')
    return re.sub(r'(?u)[^-\w.]', '', s)


def write_eml(msg: Message, base_dir: str):
    msg_date_time = str(msg.datetime_received)[:17]  # strip millis
    filename = safe_file_name("%s___%s.eml" % (msg_date_time, msg.subject))
    path = os.path.join(base_dir, msg_date_time[:4], msg_date_time[5:7])
    if 'sent' not in path:
        path = os.path.join(path, msg.sender.email_address)
    path = path.lower()
    os.makedirs(path, exist_ok=True)
    output_file = os.path.join(path, filename).lower()
    with open(output_file, 'wb') as f:
        f.write(msg.mime_content)


def process_messages(qs, base_dir, clean_up=False, backup=False):
    local_backup = 0
    ignored = 0
    deleted = 0
    errors = 0
    processing_date = '1900-01-01'

    for msg in qs:
        msg_date = str(msg.datetime_received)[:10]

        if processing_date != msg_date:
            processing_date = msg_date
            log.info('Processing %s: %s' % (base_dir, processing_date))

        try:
            if backup and isinstance(msg, Message):
                write_eml(msg, base_dir)
                local_backup += 1
            else:
                ignored += 1

            if clean_up:
                msg.delete()
                deleted += 1

        except Exception:
            errors += 1
            log.error("Error processing message", exc_info=True)

    return {'downloaded': local_backup, 'ignored': ignored, 'deleted': deleted, 'errors': errors}
