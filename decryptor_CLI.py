# Dependencies: pycryptodome and biplist

import hashlib
import os
import sqlite3
import struct
from binascii import hexlify

import biplist  # pip install biplist
import Crypto.Cipher.AES  # pip install pycryptodome If you have issues refer to https://pycryptodome.readthedocs.io/en/latest/src/faq.html#why-do-i-get-the-error-no-module-named-crypto-on-windows
from aes_keywrap import aes_unwrap_key

# CLASSES AND FUNCTIONS
CLASSKEY_TAGS = [b"CLAS", b"WRAP", b"WPKY", b"KTYP", b"PBKY"]
# Different Keybag structures which exist. Ours is a Backup
KEYBAG_TYPES = ["System", "Backup", "Escrow", "OTA (icloud)"]
KEY_TYPES = ["AES", "Curve25519"]
PROTECTION_CLASSES = {
    1: "NSFileProtectionComplete",
    2: "NSFileProtectionCompleteUnlessOpen",
    3: "NSFileProtectionCompleteUntilFirstUserAuthentication",
    4: "NSFileProtectionNone",
    5: "NSFileProtectionRecovery?",
    6: "kSecAttrAccessibleWhenUnlocked",
    7: "kSecAttrAccessibleAfterFirstUnlock",
    8: "kSecAttrAccessibleAlways",
    9: "kSecAttrAccessibleWhenUnlockedThisDeviceOnly",
    10: "kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly",
    11: "kSecAttrAccessibleAlwaysThisDeviceOnly"
}
WRAP_DEVICE = 1
WRAP_PASSCODE = 2


class Keybag(object):
    def __init__(self, data):
        self.type = None
        self.uuid = None
        self.wrap = None
        self.deviceKey = None
        self.attrs = {}
        self.classKeys = {}
        self.KeyBagKeys = None
        self.parseBinaryBlob(data)

    # This breaks the tags up into a structure.
    def parseBinaryBlob(self, data):
        currentClassKey = None

        for tag, data in loopTLVBlocks(data):
            if len(data) == 4:
                data = struct.unpack(">L", data)[0]
            if tag == b"TYPE":
                self.type = data
                if self.type > 3:
                    print("FAIL: keybag type > 3 : %d" % self.type)
            elif tag == b"UUID" and self.uuid is None:
                self.uuid = data
            elif tag == b"WRAP" and self.wrap is None:
                self.wrap = data
            elif tag == b"UUID":
                if currentClassKey:
                    self.classKeys[currentClassKey[b"CLAS"]] = currentClassKey
                currentClassKey = {b"UUID": data}
            elif tag in CLASSKEY_TAGS:
                currentClassKey[tag] = data
            else:
                self.attrs[tag] = data
        if currentClassKey:
            self.classKeys[currentClassKey[b"CLAS"]] = currentClassKey

    def unlockWithPasscode(self, passcode):
        passcode1 = hashlib.pbkdf2_hmac('sha256', passcode,
                                        self.attrs[b"DPSL"],
                                        self.attrs[b"DPIC"], 32)
        passcode_key = hashlib.pbkdf2_hmac('sha1', passcode1,
                                           self.attrs[b"SALT"],
                                           self.attrs[b"ITER"], 32)

        for classkey in self.classKeys.values():
            k = classkey[b"WPKY"]
            if classkey[b"WRAP"] & WRAP_PASSCODE:
                k = aes_unwrap_key(passcode_key, classkey[b"WPKY"])
                if not k:
                    return False
                classkey[b"KEY"] = k
        return True

    def unwrapKeyForClass(self, protection_class, persistent_key):
        ck = self.classKeys[protection_class][b"KEY"]
        if len(persistent_key) != 0x28:
            raise Exception("Invalid key length")
        return aes_unwrap_key(ck, persistent_key)


def loopTLVBlocks(blob):
    i = 0
    while i + 8 <= len(blob):
        tag = blob[i:i+4]
        length = struct.unpack(">L", blob[i+4:i+8])[0]
        data = blob[i+8:i+8+length]
        yield (tag, data)
        i += 8 + length


def removePadding(data, blocksize=16):
    n = int(data[-1])  # RFC 1423: last byte contains number of padding bytes.
    if n > blocksize or n > len(data):
        raise Exception('Invalid CBC padding')
    return data[:-n]


ZEROIV = b"\x00"*16


def AESdecryptCBC(data, key, iv=ZEROIV, padding=False):
    if len(data) % 16:
        print("AESdecryptCBC: data length not /16, truncating")
        data = data[0:(len(data)/16) * 16]
    data = Crypto.Cipher.AES.new(
        key, Crypto.Cipher.AES.MODE_CBC, iv).decrypt(data)
    if padding:
        return removePadding(16, data)
    return data


def decryptBackup(output_path, manifest_file, passcode):
    """ Decrypts the backup and calls the necessary functions to process the backup """
    # Validate backup location input
    validated = False
    while validated == False:
        if os.path.exists(manifest_file):
            validated = True
        else:
            manifest_file = os.path.expanduser(manifest_file)
            if os.path.exists(manifest_file):
                validated = True
            else:
                print("That isn't a valid path. Please try again")
                validated = False
                manifest_file = str(input(
                    "Please enter the path to the backup folder: "))

    if "Manifest.plist" in manifest_file:
        pass
    else:
        manifest_file = manifest_file + "/Manifest.plist"
        if os.path.exists(manifest_file):
            pass
        else:
            manifest_file = manifest_file + "Manifest.plist"
    backup_path = manifest_file[:-14]
    manifest_db = backup_path + "Manifest.db"

    print("[STATUS] Decrypting Backup...")

    # Encode password input
    password = passcode.encode('utf-8')

    # Open the manifest.plist and dump keybag
    infile = open(manifest_file, 'rb')
    manifest_plist = biplist.readPlist(infile)
    keybag = Keybag(manifest_plist['BackupKeyBag'])

    # Unlock keybag with password
    passwordcorrect = False
    keybag.unlockWithPasscode(password)

    # Decrypt manifest.db
    # The key is everything after the first 4 bytes
    manifest_key = manifest_plist['ManifestKey'][4:]
    db = open(manifest_db, 'rb')  # Opens Manifest.db as readable binary object
    encrypted_db = db.read()
    manifest_class = struct.unpack('<l', manifest_plist['ManifestKey'][:4])[
        0]  # Gets manifest protection class
    # Unwrapped key to the manifest.db
    key = keybag.unwrapKeyForClass(manifest_class, manifest_key)
    decrypted_data = AESdecryptCBC(
        encrypted_db, key)  # Decrypts the manifest.db

    output_path = os.path.join(output_path, 'Decrypted')
    # This will write out the manifest.db
    db_filename = os.path.join(output_path, "db.sqlite3")
    db_file = open(db_filename, 'wb')
    db_file.write(decrypted_data)
    db_file.close()
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("""
        SELECT fileID, relativePath, file
        FROM Files
        WHERE flags=1 
        AND relativePath LIKE "%CallHistory.storedata" 
        OR relativePath LIKE "%ChatStorage.sqlite" 
        OR relativePath LIKE "%AddressBook.sqlitedb"
        OR relativePath LIKE "%Calendar.sqlitedb" 
        ORDER BY domain, relativePath""")
    results = c.fetchall()
    for item in results:
        fileID, relativePath, file_bplist = item
        # APFS allows colons in filenames but NTFS does not, so this replaces the colon with !-.
        if ':' in relativePath:
            relativePath = relativePath.replace(':', '!-')
        plist = biplist.readPlistFromString(file_bplist)
        file_data = plist['$objects'][plist['$top']['root'].integer]
        size = file_data['Size']
        relativePath = relativePath.split("/")
        relativePath = relativePath[len(relativePath) - 1]
        protection_class = file_data['ProtectionClass']
        encryption_key = plist['$objects'][file_data['EncryptionKey'].integer]['NS.data'][4:]
        backup_filename = os.path.join(backup_path, fileID[:2], fileID)
        infile = open(backup_filename, 'rb')
        data = infile.read()
        key = keybag.unwrapKeyForClass(protection_class, encryption_key)
        decrypted_data = AESdecryptCBC(data, key)[:size]
        # Replaces the | in the filename to fix an error where the program would crash when trying to make this file
        output_filename = os.path.join(
            output_path, relativePath).replace("|", "_")
        if not os.path.exists(os.path.dirname(output_filename)):
            try:
                os.makedirs(os.path.dirname(output_filename))
            except OSError as exc:
                if exc.errno != exc.errno.EEXIST:
                    raise
        outfile = open(output_filename, 'wb')
        outfile.write(decrypted_data)
        outfile.close()
        infile.close()
    return True
