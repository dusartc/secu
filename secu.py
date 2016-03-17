import os
import gnupg

cwd = os.getcwd()
gpg = gnupg.GPG(gnupghome=cwd)

def clean():
    li = ['pubring.gpg', 'pubring.gpg~', 'random_seed', 'secring.gpg', 'trustdb.gpg']
    global cwd
    for l in li:
        string = cwd + "/" + l
        os.remove(string)

def gen_gpg():
    input_data = gpg.gen_key_input(key_type="RSA", key_length=4096, name_email="dusartc@Debian")
    print "gen key"
    key = gpg.gen_key(input_data)
    print "gen key done"
    #export(key)
    encrypt("toto");

def encrypt(f):
    for files in os.listdir(cwd):
        if os.path.isfile(files):
            print files
    with open(f,"rb") as files:
        data = gpg.encrypt_file(files, recipients=["dusartc@Debian"], output="bonjour.txt")
    print "ok: ", data.ok
    print "status: ", data.status
    print "stderr: ", data.stderr

def export(k):
    pub = gpg.export_keys(k.__str__)
    priv = gpg.export_keys(k.__str__, True)
    with open('key.asc', 'w') as f:
        f.write(pub)
        f.write(priv)

