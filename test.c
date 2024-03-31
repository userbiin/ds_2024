#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define ListNode structure
typedef struct ListNode {
    char *data;
    struct ListNode *prev;
    struct ListNode *next;
} ListNode;

// Define CacheSimulator structure
typedef struct CacheSimulator {
    int cache_slots;
    int cache_hit;
    int tot_cnt;
    ListNode *head;
    ListNode *tail;
    ListNode **cache;
} CacheSimulator;

// Function to initialize CacheSimulator
CacheSimulator* initializeCacheSimulator(int cache_slots) {
    CacheSimulator *cache_sim = (CacheSimulator*)malloc(sizeof(CacheSimulator));
    cache_sim->cache_slots = cache_slots;
    cache_sim->cache_hit = 0;
    cache_sim->tot_cnt = 1;
    cache_sim->cache = (ListNode**)malloc(cache_slots * sizeof(ListNode*));
    cache_sim->head = NULL;
    cache_sim->tail = NULL;
    return cache_sim;
}

// Function to initialize ListNode
ListNode* initializeListNode(char *data, ListNode *prevNode, ListNode *nextNode) {
    ListNode *node = (ListNode*)malloc(sizeof(ListNode));
    node->data = strdup(data);
    node->prev = prevNode;
    node->next = nextNode;
    return node;
}

// Function to perform cache simulation
void do_sim(CacheSimulator *cache_sim, char *page) {
    cache_sim->tot_cnt += 1;
    int i;
    int found = -1;
    for (i = 0; i < cache_sim->cache_slots; i++) {
        if (cache_sim->cache[i] != NULL && strcmp(cache_sim->cache[i]->data, page) == 0) {
            found = i;
            break;
        }
    }
    if (found != -1) {
        // Cache hit
        cache_sim->cache_hit += 1;
        ListNode *Listnode = cache_sim->cache[found];
        if (Listnode != cache_sim->head) {
            // MRU
            if (Listnode == cache_sim->tail) {
                cache_sim->tail = Listnode->prev;
            } else {
                Listnode->next->prev = Listnode->prev;
            }
            Listnode->prev->next = Listnode->next;

            Listnode->next = cache_sim->head;
            Listnode->prev = NULL;
            cache_sim->head->prev = Listnode;
            cache_sim->head = Listnode;
        }
    } else {
        // Cache miss
        ListNode *node = initializeListNode(page, NULL, NULL);
        if (cache_sim->cache_slots <= cache_sim->tot_cnt) {
            // rm LRU
            free(cache_sim->tail->data);
            free(cache_sim->tail);
            cache_sim->tail = cache_sim->tail->prev;
            cache_sim->tail->next = NULL;
        }
        for (i = cache_sim->cache_slots - 1; i > 0; i--) {
            cache_sim->cache[i] = cache_sim->cache[i - 1];
        }
        cache_sim->cache[0] = node;
        if (!cache_sim->head) {
            cache_sim->head = node;
            cache_sim->tail = node;
        } else {
            // Add MRU
            node->next = cache_sim->head;
            cache_sim->head->prev = node;
            cache_sim->head = node;
        }
    }
}

// Function to print cache statistics
void print_stats(CacheSimulator *cache_sim) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n", cache_sim->cache_slots, cache_sim->cache_hit, (float)cache_sim->cache_hit / cache_sim->tot_cnt);
}

// Function to free memory allocated for CacheSimulator
void freeCacheSimulator(CacheSimulator *cache_sim) {
    int i;
    // Free nodes in the cache
    for (i = 0; i < cache_sim->cache_slots; i++) {
        if (cache_sim->cache[i] != NULL) {
            free(cache_sim->cache[i]->data); // Free data first
            free(cache_sim->cache[i]);
            cache_sim->cache[i] = NULL; // Set to NULL after freeing
        }
    }
    // Free the cache array itself
    free(cache_sim->cache);
    // Free the CacheSimulator structure
    free(cache_sim);
}

int main() {
    FILE *data_file;
    data_file = fopen("/workspaces/ds_2024/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    char line[256];
    int cache_slots;
    for (cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        CacheSimulator *cache_sim = initializeCacheSimulator(cache_slots);
        while (fgets(line, sizeof(line), data_file) != NULL) {
            char *page = strtok(line, " ");
            do_sim(cache_sim, page);
        }
        print_stats(cache_sim);
        freeCacheSimulator(cache_sim);
        fseek(data_file, 0, SEEK_SET);
    }

    fclose(data_file);
    return 0;
}
