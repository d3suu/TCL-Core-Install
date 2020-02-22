# Workflow

## 1. Formatting HDD
 - Use `fdisk` to set one root partition (EXT4) (`> n`)
 - Make it bootable (`> a`)
 - Write changes and exit (`> w`)
 - Format it **WITH `-O ^64bit`** - `mkfs.ext4 -O ^64bit /dev/sda1`
 - Mount it - `sudo mount /dev/sda1 /mnt/sda1`

## 2. Download, install and configure Extlinux
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
 
## 3. Copy files
 - Mount HDD - `sudo mount /dev/sda1 /mnt/sda1`
 - Mount CDROM - `sudo mount /dev/sr0 /mnt/sr0`
 - Copy `core.gz` and `vmlinuz` from CDROM to HDD - `sudo cp /mnt/sr0/boot/* /mnt/sda1/`
 
## 4. Finish
 - Unmount HDD - `sudo umount /dev/sda1`
 - Synchronize - `sync`
 - Reboot - `sudo reboot`
