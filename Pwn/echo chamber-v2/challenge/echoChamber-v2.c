#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>

#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
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
    print_animated(COLOR_RED "SECURE MESSAGE ENCRYPTION SERVICE\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("Welcome to the Secure Message Encryption Service.\n");
    usleep(LINE_DELAY);
    print_animated("This service uses state-of-the-art encryption algorithms to protect your messages.\n");
    usleep(LINE_DELAY);
    printf("\n");
    print_animated(COLOR_YELLOW "WARNING: This system is highly secure.\n");
    usleep(LINE_DELAY);
    print_animated("Any unauthorized access will be logged and reported.\n");
    usleep(LINE_DELAY);
    print_animated("Please enter your message below to encrypt it...\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

void pass_through(const char* input) {

}

void encrypt_message(const char *input) {
    printf("\n");
    print_animated(COLOR_CYAN "Encrypting your message...\n" COLOR_RESET);
    usleep(LINE_DELAY);

    char encrypted[256];
    for (int i = 0; input[i] != '\0'; i++) {
        encrypted[i] = input[i] ^ 0xAA;
    }
    encrypted[strlen(input)] = '\0';

    printf(COLOR_MAGENTA "Encrypted Message: ");
    printf(COLOR_RESET);
    puts(encrypted);
    pass_through(encrypted);
}

void vulnerable_function() {
    char buffer[64];
    printf("\n");
    print_animated(COLOR_CYAN "Enter your message to encrypt:\n" COLOR_RESET);
    printf(COLOR_BLUE ">\x1b[0m ");
    gets(buffer);
    encrypt_message(buffer);
}

void logout_message() {
    printf("\n");
    print_animated(COLOR_GREEN "Your message has been encrypted. Thank you for using our service.\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("Logging out...\n");
    usleep(LINE_DELAY);
}

int main() {
    setup_io();
    display_banner();
    vulnerable_function();
    logout_message();
    return 0;
}
