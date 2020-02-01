
from exchangelib import Account, Folder
from commons import load_configuration, login, process_messages
import os

a = login(load_configuration('conf.yml'))
a.root.refresh()
# print(a.root.tree())

source_folder = a.root / 'Top of Information Store' / 'Cronologia conversazioni'
destination = os.path.join('account', 'lync-chats')

process_messages(source_folder.all(), destination, do_log=True,
                    do_delete=False, do_backup=False)

# f = Folder(parent=a.root, name='ExchangeSyncData')
# f.empty(delete_sub_folders=True)
