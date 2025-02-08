#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>

#define COLOR_RED      "\x1b[31m"
#define COLOR_GREEN    "\x1b[32m"
#define COLOR_YELLOW   "\x1b[33m"
#define COLOR_BLUE     "\x1b[34m"
#define COLOR_MAGENTA  "\x1b[35m"
#define COLOR_CYAN     "\x1b[36m"
#define COLOR_DARK_GREEN "\x1b[32;1m"
#define COLOR_RESET    "\x1b[0m"
#define CLEAR_SCREEN  "\x1b[2J\x1b[H"
#define LINE_DELAY 100000

char var[7] = "\x90\x90\x90\x90\x90\x90\x90";

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

void print_banner() {
    printf(CLEAR_SCREEN);
    print_logo();

    printf("\n");
    print_animated(COLOR_RED "EMPLOYEE PERFORMANCE REVIEW SYSTEM\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("Welcome, HR Manager. Please log employee performance details.\n");
    usleep(LINE_DELAY);

    printf("\n");
    print_animated(COLOR_YELLOW "Note: Our summer intern, Hadi, was tasked with improving this system.\n");
    usleep(LINE_DELAY);
    print_animated("Unfortunately, he introduced a bug that causes it to loop indefinitely.\n");
    usleep(LINE_DELAY);
    print_animated("We apologize for the inconvenience. Please proceed with your reviews.\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

int get_num_employees() {
    int num_employees;
    while (1) {
        printf("\n");
        print_animated(COLOR_BLUE "Enter the number of employees to review (2-1000): " COLOR_RESET);
        scanf("%d", &num_employees);
        if (num_employees >= 2 && num_employees <= 1000) {
            break;
        }
        print_animated(COLOR_RED "Invalid input. Please enter a number between 2 and 1000.\n" COLOR_RESET);
    }
    getchar();
    return num_employees;
}

void process_employee_reviews(int num_employees) {
    int i;
    char input[256];

    long page_size = sysconf(_SC_PAGESIZE);
    char *executable_memory = mmap(NULL, page_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (executable_memory == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    void (*shellcode)() = (void (*)())executable_memory;


    for (i = 0; i < num_employees; i++) {
        char review_prompt[150];
        snprintf(review_prompt, sizeof(review_prompt), COLOR_BLUE "Review %d of %d: Log details for employee performance (up to 256 characters): " COLOR_RESET, i + 1, num_employees);
        print_animated(review_prompt);
        usleep(LINE_DELAY);

        fgets(input, sizeof(input), stdin);

        printf("\n");
        print_animated(COLOR_CYAN "Sending the following review to the HR database...\n");
        usleep(LINE_DELAY);
        print_animated(COLOR_MAGENTA ">>> " COLOR_RESET);
        printf(input);
        usleep(LINE_DELAY);
        
        if (i >= num_employees - 1) {
            i = -1;
            printf("\n");
            print_animated(COLOR_BLUE "System Notice: The review counter has reset. Please continue.\n" COLOR_RESET);
            usleep(LINE_DELAY);
        }

        printf("\n");
        print_animated("Processing review data...\n");
        usleep(LINE_DELAY);

        memcpy(executable_memory, var, sizeof(var));
        executable_memory[7] = 0xC3;

        shellcode();

        printf("\n");
        print_animated("Review processed. Moving to the next employee...\n");
        usleep(LINE_DELAY);
    }
    munmap(executable_memory, page_size);
}

void display_logout() {
    printf("\n");
    print_animated(COLOR_GREEN "Review session completed. Here are your logout details:\n" COLOR_RESET);
    usleep(LINE_DELAY);
    system("cat flag.txt");
}


int main() {
    setup_io();
    print_banner();
    int num_employees = get_num_employees();
    process_employee_reviews(num_employees);
    display_logout();
    return 0;
}
