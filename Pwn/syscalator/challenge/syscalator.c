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

typedef void (*func_ptr)(const char*, int, int);

void setup_io() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
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
    printf("██╗  ██╗       █████╗ ██████╗\n");
    printf("╚██╗██╔╝      ██╔══██╗██╔══██╗\n");
    printf(" ╚███╔╝ █████╗██║  ██║██████╔╝\n");
    printf(" ██╔██╗ ╚════╝██║  ██║██╔══██╗\n");
    printf("██╔╝╚██╗      ╚█████╔╝██║  ██║\n");
    printf("╚═╝  ╚═╝       ╚════╝ ╚═╝  ╚═╝\n");
    printf(COLOR_RESET);
    usleep(LINE_DELAY);
}

void print_banner() {
    printf(CLEAR_SCREEN);
    print_logo();

    printf("\n");
    print_animated(COLOR_GREEN "Welcome to the Syscalator!\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("This program performs magical computations using your inputs.\n");
    usleep(LINE_DELAY);
    print_animated("Let's get started!\n");
    usleep(LINE_DELAY);
}

void print_addresses_and_descriptions_animated(func_ptr functions[], const char* descriptions[], int count) {
    printf("\n");
    print_animated(COLOR_BLUE "Here are the available functions you can call:\n" COLOR_RESET);
    usleep(LINE_DELAY);
    printf("--------------------------------------------\n");
    usleep(LINE_DELAY);
    for (int i = 0; i < count; i++) {
        printf("Function %d: Address = ", i + 1);
        printf("%p", functions[i]);
        printf("  |  ");
        usleep(LINE_DELAY);
        print_animated(COLOR_MAGENTA);
        print_animated(descriptions[i]);
        printf(COLOR_RESET "\n");
        usleep(LINE_DELAY);
    }
    printf("--------------------------------------------\n");
    usleep(LINE_DELAY);
}

void print_sum(const char* str, int a, int b) {
    print_animated(COLOR_CYAN "Hi ");
    print_animated(str);
    print_animated(", watch the magic of computation!\n" COLOR_RESET);
    print_animated("Sum of ");
    printf("%d", a);
    print_animated(" and ");
    printf("%d", b);
    print_animated(" is ");
    printf("%d\n", a + b);
}

void print_product(const char* str, int a, int b) {
    print_animated(COLOR_CYAN "Hi ");
    print_animated(str);
    print_animated(", watch the magic of computation!\n" COLOR_RESET);
    print_animated("Product of ");
    printf("%d", a);
    print_animated(" and ");
    printf("%d", b);
    print_animated(" is ");
    printf("%d\n", a * b);
}

void print_difference(const char* str, int a, int b) {
    print_animated(COLOR_CYAN "Hi ");
    print_animated(str);
    print_animated(", watch the magic of computation!\n" COLOR_RESET);
    print_animated("Difference between ");
    printf("%d", a);
    print_animated(" and ");
    printf("%d", b);
    print_animated(" is ");
    printf("%d\n", a - b);
}

void deprecated_utility() {
    asm("syscall");
}

int ask_for_review() {
    int review;
    printf("\n");
    print_animated(COLOR_BLUE "Rate your experience with the Syscalator so far!" COLOR_RESET);
    printf("\n");
    printf(COLOR_BLUE "> " COLOR_RESET);
    scanf("%d", &review);
    printf("\n");
    return review;
}

void get_user_input(char *name, unsigned long *func_addr, int *param1, int *param2) {
    print_animated(COLOR_BLUE "What's your name" COLOR_RESET);
    printf("\n");
    printf(COLOR_BLUE "> " COLOR_RESET);
    scanf("%s", name);

    print_animated(COLOR_BLUE "Enter the address of the function you'd like to call (in hex, e.g., 0x401530)" COLOR_RESET);
    printf("\n");
    printf(COLOR_BLUE "> " COLOR_RESET);
    scanf("%lx", func_addr);

    print_animated(COLOR_BLUE "Enter the first integer value to use for the calculations" COLOR_RESET);
    printf("\n");
    printf(COLOR_BLUE "> " COLOR_RESET);
    scanf("%d", param1);

    print_animated(COLOR_BLUE "Enter the second integer value to use for the calculations" COLOR_RESET);
    printf("\n");
    printf(COLOR_BLUE "> " COLOR_RESET);
    scanf("%d", param2);
}

void display_farewell() {
    printf("\n");
    print_animated(COLOR_GREEN "Thank you for using the Syscalator!\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

int main() {
    setup_io();

    func_ptr functions[] = {
        print_sum,
        print_product,
        print_difference,
    };

    const char* function_descriptions[] = {
        "Calculates the sum of two integers.",
        "Calculates the product of two integers.",
        "Calculates the difference between two integers.",
    };

    print_banner();
    print_addresses_and_descriptions_animated(functions, function_descriptions, sizeof(functions) / sizeof(functions[0]));

    char name[10];
    unsigned long func_addr;
    int param1, param2;

    get_user_input(name, &func_addr, &param1, &param2);

    func_ptr func = (func_ptr)func_addr;
    int review = ask_for_review();

    func(name, param1, param2);

    display_farewell();

    return 0;
}
