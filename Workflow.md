# Workflow

## 1. Easy mode - initrd
### 1.1. Formatting HDD
 - Use `fdisk` to set one root partition (EXT4) (`> n`)
 - Make it bootable (`> a`)
 - Write changes and exit (`> w`)
 - Format it **WITH `-O ^64bit`** - `mkfs.ext4 -O ^64bit /dev/sda1`
 - Mount it - `sudo mount /dev/sda1 /mnt/sda1`

### 1.2. Download, install and configure Extlinux
 - Download extlinux - `tce-load -wi syslinux`
 - Make boot directory on HDD - `sudo mkdir /mnt/sda1/boot`
 - Install extlinux on HDD - `sudo extlinux --install /mnt/sda1/boot`
 - Configure extlinux - `sudo vi /mnt/sda1/boot/extlinux.conf`
```
DEFAULT linux
LABEL linux
  KERNEL /vmlinuz
  APPEND ro root=/dev/sda1 initrd=/core.gz
```
 - Unmount HDD - `sudo umount /dev/sda1`
 - Install MBR - `sudo cat /usr/local/share/syslinux/mbr.bin > /dev/sda`
 
### 1.3. Copy files
 - Mount HDD - `sudo mount /dev/sda1 /mnt/sda1`
 - Mount CDROM - `sudo mount /dev/sr0 /mnt/sr0`
 - Copy `core.gz` and `vmlinuz` from CDROM to HDD - `sudo cp /mnt/sr0/boot/* /mnt/sda1/`
 
### 1.4. Finish
 - Unmount HDD - `sudo umount /dev/sda1`
 - Synchronize - `sync`
 - Reboot - `sudo reboot`

## 2. Hard mode - raw rootfs on hard drive
> First and last step are the same!
### 2.1. Formatting HDD
 - Use `fdisk` to set one root partition (EXT4) (`> n`)
 - Make it bootable (`> a`)
 - Write changes and exit (`> w`)
 - Format it **WITH `-O ^64bit`** - `mkfs.ext4 -O ^64bit /dev/sda1`
 - Mount it - `sudo mount /dev/sda1 /mnt/sda1`

### 2.2. Download, install and configure Extlinux
 - Download extlinux - `tce-load -wi syslinux`
 - Make boot directory on HDD - `sudo mkdir /mnt/sda1/boot`
 - Install extlinux on HDD - `sudo extlinux --install /mnt/sda1/boot`
 - Configure extlinux - `sudo vi /mnt/sda1/boot/extlinux.conf`
```
DEFAULT linux
LABEL linux
  KERNEL /vmlinuz
  APPEND rw root=/dev/sda1 init=/init multivt
```
 - Unmount HDD - `sudo umount /dev/sda1`
 - Install MBR - `sudo cat /usr/local/share/syslinux/mbr.bin > /dev/sda`
 
### 2.3 Unpack `core.gz`, and modify init
 - Mount HDD - `sudo mount /dev/sda1 /mnt/sda1`
 - Mount CDROM - `sudo mount /dev/sr0 /mnt/sr0`
 - Copy `core.gz` and `vmlinuz` from CDROM to HDD - `sudo cp /mnt/sr0/boot/* /mnt/sda1/`
 - Unpack `core.gz` - `sudo gunzip core.gz` then `sudo cpio -idv < core`
 - Remove `core` - `sudo rm core`
 - Modify `init`:
   - Remove all lines
   - Write this:
```sh
#!/bin/sh
sed -i s/^#tty/tty/ /etc/inittab #OR simply modify /etc/inittab
exec /sbin/init
```
 - Modify `/etc/init.d/rcS`:
   - Comment out this line: `/bin/mount -o remount,rw /`
   - Write new line: `/bin/mount -o remount,rw /dev/sda1 /`
   
### 2.4 Finish
 - Unmount HDD - `sudo umount /dev/sda1`
 - Synchronize - `sync`
 - Reboot - `sudo reboot`
