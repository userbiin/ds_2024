#include <stdio.h>
#include <stdlib.h>

// 노드 구조체 정의
typedef struct ListNode {
    int data;
    struct ListNode* next;
    struct ListNode* prev;
} ListNode;

// Circular Linked List 구조체 정의
typedef struct CircularLinkedListBasic {
    ListNode* tail;
} CircularLinkedListBasic;

// Cache 시뮬레이터 구조체 정의
typedef struct CacheSimulator {
    int cache_slots;
    int cache_hit;
    int tot_cnt;
    ListNode* head;
    ListNode* tail;
    ListNode** cache;
} CacheSimulator;

// ListNode 생성 함수
ListNode* createListNode(int data, ListNode* nextNode, ListNode* prevNode) {
    ListNode* newNode = (ListNode*)malloc(sizeof(ListNode));
    newNode->data = data;
    newNode->next = nextNode;
    newNode->prev = prevNode;
    return newNode;
}

// Circular Linked List 초기화 함수
void initializeCircularLinkedList(CircularLinkedListBasic* list) {
    list->tail = createListNode('dummy', NULL, NULL); // dummy node 생성
    list->tail->next = list->tail;
    list->tail->prev = list->tail;
}

// Cache 시뮬레이터 초기화 함수
void initializeCacheSimulator(CacheSimulator* cacheSimulator, int cache_slots) {
    cacheSimulator->cache_slots = cache_slots;
    cacheSimulator->cache_hit = 0;
    cacheSimulator->tot_cnt = 1;
    cacheSimulator->head = NULL;
    cacheSimulator->tail = NULL;
    cacheSimulator->cache = (ListNode**)malloc(cache_slots * sizeof(ListNode*));
    for (int i = 0; i < cache_slots; ++i) {
        cacheSimulator->cache[i] = NULL;
    }
}

// Cache 시뮬레이터 동작 함수
void do_sim(CacheSimulator* cacheSimulator, int page) {
    cacheSimulator->tot_cnt++;
    int idx = page % cacheSimulator->cache_slots;

    if (cacheSimulator->cache[idx] != NULL && cacheSimulator->cache[idx]->data == page) {
        // Cache hit
        cacheSimulator->cache_hit++;
        ListNode* Listnode = cacheSimulator->cache[idx];
        if (Listnode != cacheSimulator->head) {
            // MRU
            if (Listnode == cacheSimulator->tail) {
                cacheSimulator->tail = Listnode->prev;
            } else {
                Listnode->next->prev = Listnode->prev;
            }
            Listnode->prev->next = Listnode->next;

            Listnode->next = cacheSimulator->head;
            Listnode->prev = NULL;
            cacheSimulator->head->prev = Listnode;
            cacheSimulator->head = Listnode;
        }
    } else {
        // Cache miss
        ListNode* node = createListNode(page, NULL, NULL);
        cacheSimulator->cache[idx] = node;
        if (cacheSimulator->tail == NULL) {
            cacheSimulator->head = node;
            cacheSimulator->tail = node;
        } else {
            // Add MRU
            node->next = cacheSimulator->head;
            cacheSimulator->head->prev = node;
            cacheSimulator->head = node;
        }

        if (cacheSimulator->cache_slots < cacheSimulator->tot_cnt) {
            // rm LRU
            ListNode* temp = cacheSimulator->tail;
            cacheSimulator->tail = cacheSimulator->tail->prev;
            cacheSimulator->tail->next = NULL;
            int temp_idx = temp->data % cacheSimulator->cache_slots;
            free(cacheSimulator->cache[temp_idx]);
            cacheSimulator->cache[temp_idx] = NULL;
            // free(temp);
        }
    }
}

// 통계 출력 함수
void print_stats(CacheSimulator* cacheSimulator) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %.2f\n", cacheSimulator->cache_slots, cacheSimulator->cache_hit, (float)cacheSimulator->cache_hit / cacheSimulator->tot_cnt);
}

int main() {
    FILE* data_file = fopen("/workspaces/ds_2024/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    char line[100];
    CacheSimulator cacheSim;
    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        initializeCacheSimulator(&cacheSim, cache_slots);
        while (fgets(line, sizeof(line), data_file)) {
            int page;
            sscanf(line, "%d", &page);
            do_sim(&cacheSim, page);
        }
        print_stats(&cacheSim);
        rewind(data_file);
    }

    fclose(data_file);
    return 0;
}
