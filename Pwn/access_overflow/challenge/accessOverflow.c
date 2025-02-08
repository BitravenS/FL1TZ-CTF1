#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_DARK_GREEN "\x1b[32;1m"
#define COLOR_RESET   "\x1b[0m"
#define CLEAR_SCREEN  "\x1b[2J\x1b[H"
#define LINE_DELAY    100000

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
    printf("██╗  ██╗       █████╗ ██████╗\n");
    printf("╚██╗██╔╝      ██╔══██╗██╔══██╗\n");
    printf(" ╚███╔╝ █████╗██║  ██║██████╔╝\n");
    printf(" ██╔██╗ ╚════╝██║  ██║██╔══██╗\n");
    printf("██╔╝╚██╗      ╚█████╔╝██║  ██║\n");
    printf("╚═╝  ╚═╝       ╚════╝ ╚═╝  ╚═╝\n");
    printf(COLOR_RESET);
    usleep(LINE_DELAY);
}

void display_banner() {
    printf(CLEAR_SCREEN);
    print_logo();
    printf("\n");
    print_animated(COLOR_YELLOW "Welcome to the Secure Access Control System\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

void prompt_for_credentials() {
    print_animated(COLOR_BLUE "Please provide your ID credentials for verification:\n" COLOR_RESET);
    printf(COLOR_BLUE ">\x1b[0m ");
}

void verify_credentials() {
    print_animated("\nVerifying credentials");
    for (int i = 0; i < 3; i++) {
        printf(".");
        usleep(LINE_DELAY);
    }
    printf("\n");
}

void grant_access() {
    print_animated(COLOR_GREEN "Access granted! Retrieving flag...\n" COLOR_RESET);
    system("cat flag.txt");
}

void deny_access() {
    print_animated(COLOR_RED "You do not have access permission.\n" COLOR_RESET);
}

int main() {
    int hasAccess = 0;
    char userCredentials[100];

    setup_io();
    display_banner();
    prompt_for_credentials();

    gets(userCredentials);

    verify_credentials();

    if (hasAccess) {
        grant_access();
    } else {
        deny_access();
    }

    return 0;
}
