#ifndef FUSE_H
#define FUSE_H

// Helper Functions
void log_message(const char *format, ...);
struct file* find_file(const char *name);

// FUSE Functions
static int cats_getattr(const char *path, struct stat *buf);
static int cats_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi);
static int cats_open(const char *path, struct fuse_file_info *fi);
static int cats_read(const char *path, char *buf, size_t count, off_t offset, struct fuse_file_info *fi);
static int cats_write(const char *path, const char *buf, size_t size, off_t offset, struct fuse_file_info *fi); 
static int cats_create(const char *path, mode_t mode, struct fuse_file_info *fi);
static int cats_truncate(const char *path, off_t size);

#endif // FUSE_H
