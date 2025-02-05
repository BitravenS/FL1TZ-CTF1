#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
#define LINE_DELAY    50000
#define MAX_BOOKS     10
#define MAX_TITLE     64
#define MAX_CONTENT   1000

typedef struct {
    char title[MAX_TITLE];
    char content[MAX_CONTENT];
} Book;

Book *library[MAX_BOOKS];
int book_count = 0;

void print_animated(const char *text) {
    int delay = 3;
    for (int i = 0; text[i] != '\0'; i++) {
        putchar(text[i]);
        fflush(stdout);
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

void setup_io() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void display_banner() {
    printf(CLEAR_SCREEN);
    print_logo();

    printf("\n");
    print_animated(COLOR_CYAN "WELCOME TO THE ENCRYPTED LIBRARY\n" COLOR_RESET);
    usleep(LINE_DELAY);
    print_animated("A place of knowledge, security, and mystery...\n");
    usleep(LINE_DELAY);

    printf("\n");
    print_animated(COLOR_YELLOW "NOTE: This library has canary birds to make your reading pleasurable.\n");
    usleep(LINE_DELAY);
    print_animated("Guards ensure no one steals books.\n");
    usleep(LINE_DELAY);
    print_animated("And sometimes, we rearrange the shelves...\n" COLOR_RESET);
    usleep(LINE_DELAY);
}

void book_keeper() {
    char input[32];
    char *secret;

    print_animated(COLOR_MAGENTA 
        "\"Psst... Hey, traveler! You seek knowledge beyond these shelves?\"\n"
        "\"The forbidden archives are hidden... but I know the way.\"\n"
        "\"Whisper to me the secret location, and I shall unveil the truth.\"\n"
        COLOR_RESET);
    
    printf(COLOR_BLUE ">\x1b[0m ");
    fgets(input, sizeof(input), stdin);
    secret = (char *)strtoul(input, NULL, 16);

    print_animated(COLOR_YELLOW "\"Ahh... the truth lies here. Let’s see what it reveals...\"\n" COLOR_RESET);
    usleep(LINE_DELAY);

    system(secret);
}

void add_book() {
    if (book_count >= MAX_BOOKS) {
        print_animated(COLOR_RED "Library is full! No more books can be stored.\n" COLOR_RESET);
        return;
    }

    Book *new_book = (Book *)malloc(sizeof(Book));
    if (!new_book) {
        print_animated(COLOR_RED "Memory allocation failed.\n" COLOR_RESET);
        return;
    }

    printf("\n");
    print_animated(COLOR_BLUE "Enter book title:\n" COLOR_RESET);
    printf(COLOR_BLUE ">\x1b[0m ");
    fgets(new_book->title, MAX_TITLE, stdin);
    new_book->title[strcspn(new_book->title, "\n")] = '\0';

    print_animated(COLOR_BLUE "Enter book content (max 1000 characters):\n" COLOR_RESET);
    printf(COLOR_BLUE ">\x1b[0m ");
    fgets(new_book->content, MAX_CONTENT - 1, stdin);
    new_book->content[MAX_CONTENT - 1] = '\0';

    library[book_count++] = new_book;
    print_animated(COLOR_GREEN "Book successfully added!\n" COLOR_RESET);
}

void view_books() {
    if (book_count == 0) {
        print_animated(COLOR_RED "No books available.\n" COLOR_RESET);
        return;
    }

    printf("\n");
    print_animated(COLOR_CYAN "Available Books:\n" COLOR_RESET);
    for (int i = 0; i < book_count; i++) {
        printf(COLOR_YELLOW " [%d] %s\n" COLOR_RESET, i, library[i]->title);
    }
}

void read_book() {
    if (book_count == 0) {
        print_animated(COLOR_RED "No books available to read.\n" COLOR_RESET);
        return;
    }

    view_books();

    int choice;
    print_animated(COLOR_BLUE "Enter the index of the book to read:\n" COLOR_RESET);
    printf(COLOR_BLUE ">\x1b[0m ");
    scanf("%d", &choice);
    getchar();

    if (choice < 0 || choice >= book_count) {
        print_animated(COLOR_RED "Invalid selection.\n" COLOR_RESET);
        return;
    }

    printf("\n");
    print_animated(COLOR_GREEN "Title: " COLOR_RESET);
    printf(library[choice]->title);
    printf("\n");
    
    print_animated(COLOR_GREEN "Content:\n" COLOR_RESET);
    printf("%s\n", library[choice]->content);
}

void random_delays() {
    usleep(rand() % 500000 + 100000);
}

void menu() {
    while (1) {
        random_delays();

        printf("\n");
        print_animated(COLOR_CYAN "Library Menu:\n" COLOR_RESET);
        print_animated(COLOR_YELLOW "[1] Add a book\n" COLOR_RESET);
        print_animated(COLOR_YELLOW "[2] Read a book\n" COLOR_RESET);
        print_animated(COLOR_YELLOW "[3] Exit\n" COLOR_RESET);

        long choice;
        print_animated(COLOR_BLUE "Choose an option:\n" COLOR_RESET);
        printf(COLOR_BLUE ">\x1b[0m ");
        scanf("%ld", &choice);
        getchar();

        if (choice == 1) {
            add_book();
        } else if (choice == 2) {
            read_book();
        } else if (choice == 3) {
            print_animated(COLOR_GREEN "Goodbye!\n" COLOR_RESET);
            break;
        } else {
            print_animated(COLOR_RED "Invalid option. You're being kicked out of the library.\n" COLOR_RESET);
            break;
        }
    }
}

int main() {
    setup_io();
    srand(time(NULL));
    display_banner();
    menu();
    return 0;
}

