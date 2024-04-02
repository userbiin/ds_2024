#include <stdio.h>
#include <stdlib.h>

// Define ListNode structure
typedef struct ListNode {
    int data;
    struct ListNode* next;
} ListNode;

// Define CacheSimulator structure
typedef struct CacheSimulator {
    int cache_slots;
    int cache_hit;
    int tot_cnt;
    ListNode* cache;
    ListNode* head;
} CacheSimulator;

// Function to create a new ListNode
ListNode* newListNode(int data) {
    ListNode* node = (ListNode*)malloc(sizeof(ListNode));
    node->data = data;
    node->next = NULL;
    return node;
}

// Function to initialize CacheSimulator
CacheSimulator* newCacheSimulator(int cache_slots) {
    CacheSimulator* cache_sim = (CacheSimulator*)malloc(sizeof(CacheSimulator));
    cache_sim->cache_slots = cache_slots;
    cache_sim->cache_hit = 0;
    cache_sim->tot_cnt = 1;
    cache_sim->cache = NULL;
    cache_sim->head = NULL;
    return cache_sim;
}

// Function to perform simulation
void do_sim(CacheSimulator* cache_sim, int page) {
    cache_sim->tot_cnt++;
    ListNode* node = cache_sim->cache;
    while (node != NULL) {
        if (node->data == page) {
            // Cache hit
            cache_sim->cache_hit++;
            if (node != cache_sim->head) {
                // Move the node to the head
                ListNode* prev_node = cache_sim->head;
                while (prev_node->next != node) {
                    prev_node = prev_node->next;
                }
                prev_node->next = node->next;
                node->next = cache_sim->head;
                cache_sim->head = node;
            }
            return;
        }
        node = node->next;
    }

    // Cache miss
    node = newListNode(page);
    node->next = cache_sim->head;
    cache_sim->head = node;

    // Add the new node to cache
    if (cache_sim->cache == NULL) {
        cache_sim->cache = node;
    }
    else {
        ListNode* last_node = cache_sim->cache;
        while (last_node->next != NULL) {
            last_node = last_node->next;
        }
        last_node->next = node;
    }

    // If cache size exceeds cache_slots, remove the LRU node
    if (cache_sim->cache_slots > 0) {
        ListNode* prev_node = NULL;
        ListNode* curr_node = cache_sim->head;
        while (curr_node->next != NULL) {
            prev_node = curr_node;
            curr_node = curr_node->next;
        }
        free(curr_node);
        if (prev_node != NULL) {
            prev_node->next = NULL;
        }
        else {
            cache_sim->head = NULL;
            cache_sim->cache = NULL;
        }
    }
}

// Function to print statistics
void print_stats(CacheSimulator* cache_sim) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n", cache_sim->cache_slots, cache_sim->cache_hit, (float)cache_sim->cache_hit / cache_sim->tot_cnt);
}

int main() {
    FILE* data_file = fopen("/workspaces/ds_2024/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    int page;
    CacheSimulator* cache_sim;

    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        cache_sim = newCacheSimulator(cache_slots);
        while (fscanf(data_file, "%d", &page) != EOF) {
            do_sim(cache_sim, page);
        }
        print_stats(cache_sim);
        rewind(data_file); // Reset file pointer to beginning
        free(cache_sim->cache); // Free memory allocated for cache
        free(cache_sim); // Free memory allocated for CacheSimulator
    }

    fclose(data_file);
    return 0;
}
