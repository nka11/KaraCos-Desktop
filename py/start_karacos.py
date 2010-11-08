
import os, sys
import shutil

KcRoot = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
#print os.path.split(os.path.abspath(__file__))
print "KaraCos Desktop is starting on %s" % os.name
print "KaraCosRoot = %s" % KcRoot
sys.path.append(os.path.join(KcRoot,'py'))
sys.path.append(os.path.join(KcRoot,'lib','python'))
os.environ['KaraCosRoot'] = KcRoot
print os.environ['Path']
if not os.path.exists(os.path.join(KcRoot,'couch','data')):
    os.makedirs(os.path.join(KcRoot,'couch','data'))
if not os.path.exists(os.path.join(KcRoot,'couch','log')):
    os.makedirs(os.path.join(KcRoot,'couch','log'))

# Use my conf
shutil.copy2(os.path.join(KcRoot,'resources','conf','default.ini'), os.path.join(KcRoot,'lib','win32','CouchDB_server','etc','couchdb'))

if __name__ == '__main__':
    os.chdir(os.path.join(KcRoot,'lib','win32','CouchDB_server','bin'))
    L = ['werl.exe','-sasl', 'errlog_type', 'error','-s','couch',]
    print os.spawnve(os.P_WAIT,os.path.join(KcRoot,'lib','win32','CouchDB_server','bin','erl.exe'),L,os.environ)