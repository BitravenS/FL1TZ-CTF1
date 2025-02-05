#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
#define COLOR_DARK_GREEN "\x1b[32;1m"
#define COLOR_RESET   "\x1b[0m"
#define CLEAR_SCREEN  "\x1b[2J\x1b[H"
#define LINE_DELAY 100000

void setup_io() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void print_animated(const char *text) {
    int delay = 5;
    for (int i = 0; text[i] != '\0'; i++) {
        putchar(text[i]);
        usleep(delay * 1000);
    }
}

void print_logo() {
    printf(COLOR_DARK_GREEN);
    printf("██╗  ██╗       █████╗ ██████╗\n");
    printf("╚██╗██╔╝      ██╔══██╗██╔══██╗\n");
    printf(" ╚███╔╝ █████╗██║  ██║██████╔╝\n");
    printf(" ██╔██╗ ╚════╝██║  ██║██╔══██╗\n");
    printf("██╔╝╚██╗      ╚█████╔╝██║  ██║\n");
    printf("╚═╝  ╚═╝       ╚════╝ ╚═╝  ╚═╝\n");
    printf(COLOR_RESET);
    usleep(LINE_DELAY);
}

char *flag;
int *system_status;
char *system_name;

void read_flag() {
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) {
        perror("Error opening flag.txt");
        exit(1);
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    flag = (char *)malloc(file_size + 1);
    if (flag == NULL) {
        perror("Error allocating memory for flag");
        fclose(file);
        exit(1);
    }

    fread(flag, 1, file_size, file);
    flag[file_size] = '\0';

    fclose(file);
}

void initiate_system() {
    read_flag();
    system_status = (int *)malloc(sizeof(int));
    system_name = (char *)malloc(50);

    *system_status = 0xDEADC0DE;
    strcpy(system_name, "Critical System v2.0");
}

void delete_addresses() {
    printf("\n\n");
    print_animated(COLOR_RED "Initiating address deletion protocol...\n");
    usleep(LINE_DELAY);
    print_animated("Deleting addresses from local machine...\n");
    usleep(LINE_DELAY);

    if (flag) {
        free(flag);
        flag = NULL;
    }
    if (system_status) {
        free(system_status);
        system_status = NULL;
    }
    if (system_name) {
        free(system_name);
        system_name = NULL;
    }

    print_animated(COLOR_GREEN "Address deletion complete. Memory purged.\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

void randomize_addresses() {
    srand(time(NULL));

    free(flag);
    flag = (char *)malloc(rand() % 100 + 20);
    free(system_status);
    system_status = (int *)malloc(sizeof(int));
    free(system_name);
    system_name = (char *)malloc(rand() % 100 + 20);

    read_flag();
    *system_status = 0x5AFE;
    strcpy(system_name, "Critical System v2.0");
}

void print_banner() {
    printf(CLEAR_SCREEN);
    print_logo();

    printf("\n");
    print_animated(COLOR_RED "CRITICAL SYSTEM ADDRESS LEAK DETECTED!\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("The following addresses have been leaked to the web:\n");
    usleep(LINE_DELAY);

    printf(COLOR_YELLOW);
    usleep(LINE_DELAY);
    printf("| ");
    printf("%p ", (void *)system_status);
    printf("| ");
    printf("%p ", (void *)flag);
    printf("| ");
    printf("%p ", (void *)system_name);
    printf("|\n" COLOR_RESET);
    usleep(LINE_DELAY);

    printf("\n");
    print_animated(COLOR_BLUE "Enter the 'Quantum Reboot Code' to restart the system\n");
    usleep(LINE_DELAY);
    print_animated("and randomize the leaked addresses.\n");
    usleep(LINE_DELAY);
    printf("> " COLOR_RESET);
}

void process_input() {
    char user_input[100];
    fgets(user_input, sizeof(user_input), stdin);
    user_input[strcspn(user_input, "\n")] = '\0';

    if (strcmp(user_input, "X-0R.FL1TZ") == 0) {
        printf("\n");
        print_animated(COLOR_GREEN "Special sequence detected! Initiating address randomization...\n" COLOR_RESET);
        usleep(LINE_DELAY);
        randomize_addresses();
        printf("\n");
        print_animated(COLOR_BLUE "System rebooting...\n");
        usleep(LINE_DELAY);
        print_animated("New addresses have been randomized. Leak mitigated.\n" COLOR_RESET);
        usleep(LINE_DELAY);
    } else {
        printf("\n");
        print_animated(COLOR_RED "Reboot code invalid. System terminating...\n");
        usleep(LINE_DELAY);
        print_animated("WARNING: Addresses remain exposed. Critical failure imminent.\n" COLOR_RESET);
        usleep(LINE_DELAY);
    }

    printf("\n");
    print_animated("The codes entered are:\n");
    usleep(LINE_DELAY);
    printf(COLOR_MAGENTA);
    printf(user_input);
    printf(COLOR_RESET);
}

int main() {
    setup_io();
    initiate_system();
    print_banner();
    process_input();
    delete_addresses();
    return 0;
}
