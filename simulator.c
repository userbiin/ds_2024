#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define ListNode structure
typedef struct ListNode {
    char data[100];
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

// Initialize CacheSimulator
CacheSimulator *initializeCacheSimulator(int cache_slots) {
    CacheSimulator *cache_sim = (CacheSimulator *)malloc(sizeof(CacheSimulator));
    cache_sim->cache_slots = cache_slots;
    cache_sim->cache_hit = 0;
    cache_sim->tot_cnt = 1;
    cache_sim->cache = (ListNode **)malloc(cache_slots * sizeof(ListNode *));
    cache_sim->head = NULL;
    cache_sim->tail = NULL;
    return cache_sim;
}

// Function to create a new ListNode
ListNode *createListNode(char *data) {
    ListNode *newNode = (ListNode *)malloc(sizeof(ListNode));
    strcpy(newNode->data, data);
    newNode->next = NULL;
    return newNode;
}

// Function to add a new ListNode to the front of the list
void addListNodeToFront(ListNode **head, ListNode *node) {
    if (*head == NULL) {
        *head = node;
    } else {
        node->next = *head;
        *head = node;
    }
}

// Function to remove the tail ListNode from the list
void removeTailListNode(ListNode **head) {
    if (*head == NULL)
        return;
    ListNode *current = *head;
    while (current->next->next != NULL) {
        current = current->next;
    }
    free(current->next);
    current->next = NULL;
}

// Function to simulate cache
void do_sim(CacheSimulator *cache_sim, char *page) {
    cache_sim->tot_cnt += 1;
    int i;
    for (i = 0; i < cache_sim->cache_slots; i++) {
        if (cache_sim->cache[i] != NULL && strcmp(cache_sim->cache[i]->data, page) == 0) {
            // Cache hit
            cache_sim->cache_hit += 1;
            ListNode *listnode = cache_sim->cache[i];
            if (listnode != cache_sim->head) {
                // MRU
                ListNode *temp = cache_sim->head;
                cache_sim->head = listnode;
                listnode->next = temp;
            }
            return;
        }
    }
    // Cache miss
    ListNode *node = createListNode(page);
    if (cache_sim->cache_slots > 0) {
        removeTailListNode(&(cache_sim->head));
    }
    addListNodeToFront(&(cache_sim->head), node);
    cache_sim->cache[cache_sim->cache_hit % cache_sim->cache_slots] = node;
}

// Function to print cache statistics
void print_stats(CacheSimulator *cache_sim) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n", cache_sim->cache_slots, cache_sim->cache_hit,
           (float)cache_sim->cache_hit / cache_sim->tot_cnt);
}

// Main function
int main() {
    FILE *data_file = fopen("/workspaces/ds_2024/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }
    char line[100];
    int cache_slots;
    for (cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        CacheSimulator *cache_sim = initializeCacheSimulator(cache_slots);
        while (fgets(line, sizeof(line), data_file)) {
            // Remove newline character
            line[strcspn(line, "\n")] = 0;
            char *token = strtok(line, " ");
            while (token != NULL) {
                do_sim(cache_sim, token);
                token = strtok(NULL, " ");
            }
        }
        print_stats(cache_sim);
        free(cache_sim);
        // Reset file pointer to the beginning of the file
        fseek(data_file, 0, SEEK_SET);
    }
    fclose(data_file);
    return 0;
}

