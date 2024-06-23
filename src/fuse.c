#include "fuse.h"

// TODO: Make all content permanent, content is lost when disk is unmounted
// TODO: Automatically mount the installation folder

struct file {
    char *name;
    char *content;
    size_t size;
    struct file *next;
};

struct file *head = NULL;

// Helper logging function
void log_message(const char *format, ...) {
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    fprintf(stderr, "\n");
    va_end(args);
}

// Helper function to keep track of files
struct file* find_file(const char *name) {
    struct file *current = head;
    while (current != NULL) {
        if (strcmp(current->name, name) == 0) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

int remove_file(const char* fname) {
    struct file* current = head;
    struct file* prev = NULL;

    while (current) {
        if (strcmp(current->name, fname) == 0) {
            // Delete file
            if (prev != NULL) {
                prev->next = current->next;
            } else {    // deleting the head node
                head = current->next;
            }

            free(current->name);
            free(current->content);
            free(current);

            return 0;
        }

        prev = current;
        current = current->next;
    }

    return -ENOENT;
}

static int fusic_getattr(const char *path, struct stat *buf) {
    memset(buf, 0, sizeof(struct stat));
    if (strcmp(path, "/") == 0) {
        buf->st_mode = S_IFDIR | 0755;
        buf->st_nlink = 2;
    } else {
        struct file *file = find_file(path + 1);
        if (file == NULL) {
            log_message("File not found: %s", path + 1);
            return -ENOENT;
        }

        buf->st_mode = S_IFREG | 0666;
        buf->st_nlink = 1;
        buf->st_size = file->size;
    }
    return 0;
}

static int fusic_readdir(
    const char *path,
    void *buf,
    fuse_fill_dir_t filler,
    off_t offset,
    struct fuse_file_info *fi
) {
    if (strcmp(path, "/") != 0) {
        return -ENOENT;
    }

    filler(buf, ".", NULL, 0);
    filler(buf, "..", NULL, 0);

    struct file *current = head;
    while (current != NULL) {
        filler(buf, current->name, NULL, 0);
        current = current->next;
    }
    return 0;
}

static int fusic_open(const char *path, struct fuse_file_info *fi) {
    if (find_file(path + 1) == NULL) {
        log_message("File not found: %s", path + 1);
        return -ENOENT;
    }
    return 0;
}

static int fusic_read(
    const char *path,
    char *buf,
    size_t count,
    off_t offset,
    struct fuse_file_info *fi
) {
    struct file *file = find_file(path + 1);
    if (file == NULL) {
        log_message("File not found: %s", path + 1);
        return -ENOENT;
    }

    if (offset < file->size) {
        if (offset + count > file->size) {
            count = file->size - offset;
        }
        memcpy(buf, file->content + offset, count);
    } else {
        return 0;
    }

    return count;
}

static int fusic_write(
    const char *path,
    const char *buf,
    size_t size,
    off_t offset,
    struct fuse_file_info *fi
) {
    struct file *file = find_file(path + 1);
    if (file == NULL) {
        log_message("Could not find the file");
        return -ENOENT;
    }

    if (offset + size > file->size) {
        char *new_content = realloc(file->content, offset + size);
        if (new_content == NULL) {
            log_message("Memory allocation failed");
            return -ENOMEM;
        }
        file->content = new_content;
        file->size = offset + size;
    }
    memcpy(file->content + offset, buf, size);
    return size;
}

static int fusic_create(const char *path, mode_t mode, 
                        struct fuse_file_info *fi) {
    struct file *newFile = (struct file *)malloc(sizeof(struct file));
    if (newFile == NULL) {
        return -ENOMEM;
    }

    newFile->name = strdup(path + 1);
    if (newFile->name == NULL) {
        free(newFile);
        return -ENOMEM;
    }

    newFile->content = (char *)malloc(1);
    if (newFile->content == NULL) {
        free(newFile->name);
        free(newFile);
        return -ENOMEM;
    }
    newFile->content[0] = '\0';
    newFile->size = 0;
    newFile->next = head;
    head = newFile;

    return 0;
}

static int fusic_unlink(const char* path) {
    int res;
    const char* fname = path + 1;

    // remove_file function will look for whether file is existing or not
    // no need to check it one more time

    res = remove_file(fname);
    if (remove_file != 0)
        log_message("Could not delete the file");

    return res;
}

// Needed when opening a file that is already created in write mode
static int fusic_truncate(const char *path, off_t size) {
    int fd;
    
    fd = open(path + 1, O_WRONLY);
    if (fd == -1) {
        log_message("Could not open the file");
        return -errno;
    }

    int res = ftruncate(fd, size);
    if (res == -1) {
        log_message("File truncation failed");
        close(fd);
        return -errno;
    }

    close(fd);
    return 0;
}

static struct fuse_operations fusic_ops = {
    .getattr = fusic_getattr,
    .readdir = fusic_readdir,
    .open = fusic_open,
    .read = fusic_read,
    .write = fusic_write,
    .create = fusic_create,
    .unlink = fusic_unlink,
    .truncate = fusic_truncate,
};

int main(int argc, char *argv[]) {
    return fuse_main(argc, argv, &fusic_ops, NULL);
}
