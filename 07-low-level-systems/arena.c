#include <stdio.h>
#include <stddef.h>

#define SIZE 65536
static unsigned char buf[SIZE];
static size_t off = 0;

void *arena_alloc(size_t n) {
    if (off + n > SIZE) return NULL;
    void *p = buf + off;                 /* hand out the next locker */
    off += n;
    return p;
}

void arena_reset(void) { off = 0; }      /* free the whole row */

int main(void) {
    char *a = arena_alloc(8);
    char *b = arena_alloc(8);
    printf("a at offset %ld, b at offset %ld, used %zu\n",
           (long)(a - (char *)buf), (long)(b - (char *)buf), off);
    arena_reset();
    printf("after reset, used %zu\n", off);
    return 0;
}
