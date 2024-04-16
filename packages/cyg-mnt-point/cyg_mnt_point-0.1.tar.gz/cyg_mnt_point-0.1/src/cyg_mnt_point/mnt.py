import subprocess
from typing import Union

def get_cygwin_mount_point(uuid_drive: str) -> Union[None, str]:
    """
    Retrieves the mount point of a drive identified by its UUID on Cygwin.

    Parameters:
        uuid_drive (str): The UUID of the drive.

    Returns:
        Union[None, str]: The mount point of the drive, or None if the drive is not found.

    Raises:
        subprocess.CalledProcessError: If an error occurs while running subprocess commands.
    """

    # Get information about the block device with the specified UUID
    block_dev = subprocess.run(['blkid', '--uuid', uuid_drive], capture_output=True, text=True) #stdout: /dev/sda1\n

    if block_dev.returncode != 0:
        return None
    else:
        # Extract the block device name (e.g., sda1) from the output
        part_blk_dev = block_dev.stdout.strip('\n').split('/dev/')[1]

        ps_cat = subprocess.run(['cat', '/proc/partitions'], capture_output=True, check=True, text=True)
        
        # Use awk to find the partition corresponding to the block device
        ps_awk = subprocess.run(['awk', '$4 == "' + part_blk_dev + '"' + ' {print $5}'], 
                                input=ps_cat.stdout, capture_output=True, text=True, check=True) # stdout: D:\
        
        mnt_point = subprocess.run(['cygpath', '--unix', ps_awk.stdout.strip('\n')], capture_output=True, text=True)
        
        return mnt_point.stdout.strip('\n')