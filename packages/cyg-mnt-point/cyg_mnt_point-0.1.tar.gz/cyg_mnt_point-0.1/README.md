# cyg_mnt_point

Search for the mount point in Cygwin by UUID disk partition

## Installation

```
pip install cyg_mnt_point
```

As of now, the functionality has been tested in the CYGWIN_NT-10.0-19044 3.5.3-1.x86_64 environment on Windows 10 LTSC 21H2.

Prerequisits:
 - Python3 installation (>= 3.8)


# Usage
Input: UUID of the target disk partition

Output: Mount point in UNIX style format  - /cygdrive/d/

```
from cyg_mnt_point import mnt 
UUID="ABCD12345678"
mnt = mnt.get_cygwin_mount_point(UUID)
if mnt is not None:
    print(mnt)
else:
    raise RuntimeError('The target disk was not found')

--------------------------------------------------------
print(mnt) --> /cygdrive/c/
```