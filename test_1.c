#include <stdio.h>

int main() {
    FILE* data_file = fopen("/workspaces/ds_2024/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    int page;
    while (fscanf(data_file, "%d", &page) != EOF) {
        printf("%d\n", page);
    }

    fclose(data_file);
    return 0;
}
