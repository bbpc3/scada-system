import subprocess
import sys

import config
import log

logger = log.get_module_logger("client")
latestTime = ''

# Creating mountpoint
def init():
    try:
        # Checking if folder mountpoint (0) if mountpoint exists
        mountpointExists = subprocess.check_output(f'test -d {config.mountpoint} ; echo $?', shell=True).decode().strip() == '0'
        if mountpointExists:
            logger.info("sshclient initialized and ready...")
            return

        subprocess.check_output(f'mkdir {config.mountpoint}', shell=True)
        logger.info("sshclient initialized and ready...")
    except Exception as e:
        logger.critical(f"Failed to initialize. No data can be retrieved : {e}")
        sys.exit(1)

def getData():
    global latestFilename
    try:
        # Mounting the sdcard
        logger.debug("Mounting /dev/sda1...")
        subprocess.check_output(f'mount /dev/sda1 {config.mountpoint}', shell=True)

        # Getting last filename in the folder (latest)
        latestFilename=subprocess.check_output(f'ls {config.basepath} | grep DAT | tail -n 1', shell=True).decode().strip()
        logger.debug(f"Latest filename: {latestFilename}")

        # Getting LAST line in the file
        content=subprocess.check_output(f'cat {config.basepath + latestFilename} | tail -n 1', shell=True).decode().strip()
        logger.debug(f"Retrieved content: {content}")


        logger.info("Successfully retrieved data")
        return content
    except Exception as e:
        logger.error(f"Unable to retrieve data {e}")
    finally:
        try:
            # Unmounting the sdcard
            logger.debug("Unmounting /dev/sda1...")
            subprocess.check_output(f'umount /mnt/usb', shell=True)
        except Exception as e:
            logger.error(f"Unable to unmount {e}")


init()

if __name__ == '__main__':
    print(getData())