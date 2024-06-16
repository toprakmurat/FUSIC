CC=gcc
CFLAGS=-D_FILE_OFFSET_BITS=64
LDFLAGS=-lfuse -lcjson -lcurl

TARGET_FUSE=src/fuse
MOUNTPOINT?=music/

.PHONY: all clean mount umount

all: $(TARGET_FUSE) $(TARGET_DATA)

$(TARGET_FUSE): fuse.o
	$(CC) $(CFLAGS) fuse.o -lfuse -o $@

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm -f *.o $(TARGET_FUSE)

# Mount the FUSE filesystem
mount: $(TARGET_FUSE)
	./$(TARGET_FUSE) $(MOUNTPOINT)

# Unmount the FUSE filesystem
umount:
	fusermount -u $(MOUNTPOINT)

