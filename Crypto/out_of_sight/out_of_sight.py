#!/usr/bin/env python3

import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from datetime import datetime
from random import randint
from time import sleep
import base64
import sys

SEED = os.urandom(16)
COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_BLUE = "\x1b[34m"
COLOR_RESET = "\x1b[0m"

ASCII_ART = r""" 
           ▄▄                                                      
▀███▀▀▀██▄ ██   ██                                                 
  ██    ██      ██                                                 
  ██    █████ ██████▀███▄███ ▄█▀██▄ ▀██▀   ▀██▀  ▄▄█▀██▀████████▄  
  ██▀▀▀█▄▄ ██   ██    ██▀ ▀▀██   ██   ██   ▄█   ▄█▀   ██ ██    ██  
  ██    ▀█ ██   ██    ██     ▄█████    ██ ▄█    ██▀▀▀▀▀▀ ██    ██  
  ██    ▄█ ██   ██    ██    ██   ██     ███     ██▄    ▄ ██    ██  
▄████████▄████▄ ▀████████▄  ▀████▀██▄    █       ▀█████▀████  ████▄

"""

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


class SecureSystem:
    def __init__(self):
        self.seed = os.urandom(16)

    def secure_hash(self, data):
        return hashlib.sha256(data).digest()

    def generate_secure_key(self):
        return self.secure_hash(self.seed)[:16]

    def secure_random(self):
        return os.urandom(16)

    def secure_encrypt(self, plaintext):
        Logger = SecureLog()
        seed, time = Logger.secure_timing()
        print("Updating time...")
        sys.stdout.flush()
        time = datetime.now().strftime("%H:%M:%S")
        self.log_secure_event(f"Encrypting data at {time}")
        sys.stdout.flush()
        key = long_to_bytes(randint(1, seed)).ljust(16, b"\x00")
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    def secure_decrypt(self, ciphertext, key):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.decrypt(ciphertext)

    def log_secure_event(self, event, time=None):
        if not time:
            time = datetime.now().strftime("%H:%M:%S")
        print(f"{COLOR_GREEN}[{time} SECURE LOG] {COLOR_RESET}{event}")

    def secure_cleanup(self):
        print("Performing secure cleanup...")
        sys.stdout.flush()

    def validate_secure_system(self):
        print("Validating secure system...")
        sys.stdout.flush()
        if len(self.seed) == 16:
            print("Secure system validation passed.")
        else:
            print("Secure system validation failed.")

        sys.stdout.flush()


class SecureBackup(SecureSystem):
    def __init__(self):
        super().__init__()
        self.backup_seed = os.urandom(16)

    def secure_backup(self):
        print("Performing secure backup...")
        sys.stdout.flush()

    def secure_restore(self):
        print("Performing secure restore...")
        sys.stdout.flush()


class SecureMonitor(SecureSystem):
    def __init__(self):
        super().__init__()
        self.monitor_seed = os.urandom(16)

    def secure_monitor(self):
        print("Performing secure monitoring...")
        sys.stdout.flush()

    def secure_alert(self):
        print("Performing secure alerting...")
        sys.stdout.flush()


class SecureLog(SecureSystem):
    def __init__(self):
        super().__init__()
        self.now = datetime.now().second
        self.log_seed = os.urandom(16)

    def secure_log(self):
        print("Performing secure logging...")
        sys.stdout.flush()

    def secure_analyze(self):
        print("Performing secure analysis...")
        sys.stdout.flush()

    def secure_timing(self):
        return self.now, self.log_seed


class SecureReport(SecureSystem):
    def __init__(self):
        super().__init__()
        self.report_seed = os.urandom(16)

    def secure_report(self):
        print("Performing secure reporting...")
        sys.stdout.flush()

    def secure_audit(self):
        print("Performing secure auditing...")
        sys.stdout.flush()


class SecureCompliance(SecureSystem):
    def __init__(self):
        super().__init__()
        self.compliance_seed = os.urandom(16)

    def secure_compliance(self):
        print("Performing secure compliance...")
        sys.stdout.flush()

    def secure_test(self):
        print("Performing secure testing...")
        sys.stdout.flush()


class SecureDeploy(SecureSystem):
    def __init__(self):
        super().__init__()
        self.deploy_seed = os.urandom(16)

    def secure_deploy(self):
        print("Performing secure deployment...")
        sys.stdout.flush()

    def secure_rollback(self):
        print("Performing secure rollback...")
        sys.stdout.flush()


class SecureScale(SecureSystem):
    def __init__(self):
        super().__init__()
        self.scale_seed = os.urandom(16)

    def secure_scale(self):
        print("Performing secure scaling...")
        sys.stdout.flush()

    def secure_migrate(self):
        print("Performing secure migration...")
        sys.stdout.flush()


class SecureRecover(SecureSystem):
    def __init__(self):
        super().__init__()
        self.recover_seed = os.urandom(16)

    def secure_recover(self):
        print("Performing secure recovery...")
        sys.stdout.flush()

    def secure_archive(self):
        print("Performing secure archiving...")
        sys.stdout.flush()


class SecureCompress(SecureSystem):
    def __init__(self):
        super().__init__()
        self.compress_seed = os.urandom(16)

    def secure_compress(self):
        print("Performing secure compression...")
        sys.stdout.flush()

    def secure_decompress(self):
        print("Performing secure decompression...")
        sys.stdout.flush()


def main():
    print(f"{COLOR_BLUE}{ASCII_ART}{COLOR_RESET}")
    # A lot of irrelevant code to distract the solver
    print("Welcome to the ultra-secure encryption service!")
    sys.stdout.flush()
    sleep(1)
    print("We use state-of-the-art cryptography to keep your data safe.")
    sys.stdout.flush()
    sleep(1)
    print(
        f"{COLOR_GREEN}Our seed is generated using a secure random number generator.{COLOR_RESET}"
    )
    sys.stdout.flush()
    sleep(1)
    print("You can trust us with your data!")
    sys.stdout.flush()
    print(f"{'-'*50}\n")

    # Initialize the secure system
    secure_system = SecureSystem()
    secure_backup = SecureBackup()
    secure_monitor = SecureMonitor()
    secure_report = SecureReport()
    secure_compliance = SecureCompliance()
    secure_deploy = SecureDeploy()
    secure_scale = SecureScale()
    secure_recover = SecureRecover()
    secure_compress = SecureCompress()

    # Getting up to some secure business
    secure_system.validate_secure_system()
    sleep(0.1)
    secure_system.log_secure_event("System initialized and validated.")
    sleep(0.1)
    secure_backup.secure_backup()
    sleep(0.1)
    secure_monitor.secure_monitor()
    sleep(0.1)
    secure_monitor.secure_alert()
    sleep(0.1)
    secure_report.secure_report()
    sleep(0.1)
    secure_report.secure_audit()
    sleep(0.1)
    secure_compliance.secure_compliance()
    sleep(0.1)
    secure_compliance.secure_test()
    sleep(0.1)
    secure_deploy.secure_deploy()
    sleep(0.1)
    secure_deploy.secure_rollback()
    sleep(0.1)
    secure_scale.secure_migrate()
    sleep(0.1)
    secure_recover.secure_recover()
    sleep(0.1)
    secure_recover.secure_archive()
    sleep(0.1)
    secure_compress.secure_compress()
    sleep(0.1)
    secure_compress.secure_decompress()
    sleep(0.1)
    print(f"{'-'*50}\n")

    encrypted_flag = secure_system.secure_encrypt(FLAG)
    print(
        f"Here is your encrypted flag:{COLOR_RED} {base64.b64encode(encrypted_flag).decode()}{COLOR_RESET}"
    )
    sys.stdout.flush()

    # Perform secure cleanup
    secure_system.secure_cleanup()

    print(f"{'-'*50}\n")
    print("Thank you for using our secure encryption service!")
    sys.stdout.flush()
    print(f"Remember, {COLOR_YELLOW}security {COLOR_RESET}is our top priority!")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
