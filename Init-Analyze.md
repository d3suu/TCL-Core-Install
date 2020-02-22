# `/init` Analyze

```sh
 1: #!/bin/sh
 2: mount proc
 3: grep -qw multivt /proc/cmdline && sed -i s/^#tty/tty/ /etc/inittab
 4: if ! grep -qw noembed /proc/cmdline; then
 5:   inodes=`grep MemFree /proc/meminfo | awk '{print $2/3}' | cut -d. -f1`
 6:   mount / -o remount,size=90%,nr_inodes=$inodes
 7:   umount proc
 8:   exec /sbin/init
 9: fi
10: umount proc
11: if mount -t tmpfs -o size=90% tmpfs /mnt; then
12:   if tar -C / --exclude=mnt -cf - . | tar -C /mnt/ -xf - ; then
13:     mkdir /mnt/mnt
14:     exec /sbin/switch_root mnt /sbin/init
15:   fi
16: fi
17: exec /sbin/init
```

## Workflow
 - Line 2 mounts /proc
 - Line 3 is basically if statement. If we have `multivt` anywhere in our cmdline (boot options in syslinux), sed overwrites `/etc/inittab`, so that it uses all the tty's
 - Line 4-9 runs, if we did not specify `noembed` in our cmdline:
   - Line 5 sets `${inodes}` value, which is `MemFree` value in `/proc/meminfo`
   - Line 6 mounts rootfs (of type none) with options `remount`, `size=90%` (Size of tmpfs is equal to 90% of RAM), `nr_inodes=$inodes` (Sets maximum number of inodes for this instance)
   - Line 7 unmounts `/proc` since we are ending life of this script in next line
   - Line 8 executes /sbin/init which is binary init which works on `/etc/inittab`
 - Line 10 unmounts `/proc` since we don't need it anymore
 - Line 11 checks if we can mount tmpfs of size=90% of RAM as /mnt
   - If yes, script checks if it creates tar in directory / excluding /mnt (?)
   #FINISHME
