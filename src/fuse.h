#ifndef FUSE_H
#define FUSE_H

#define FUSE_USE_VERSION 26

// Include Statements
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <errno.h>
#include <string.h>
#include <fuse.h>
#include <fcntl.h>
#include <unistd.h>

// Helper Functions
void log_message(const char *format, ...);
struct file* find_file(const char *name);
int remove_file(const char* fname);

// FUSE Functions
static int fusic_getattr(const char *path, struct stat *buf);
static int fusic_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi);
static int fusic_open(const char *path, struct fuse_file_info *fi);
static int fusic_read(const char *path, char *buf, size_t count, off_t offset, struct fuse_file_info *fi);
static int fusic_write(const char *path, const char *buf, size_t size, off_t offset, struct fuse_file_info *fi); 
static int fusic_create(const char *path, mode_t mode, struct fuse_file_info *fi);
static int fusic_truncate(const char *path, off_t size);

#endif // FUSE_H
