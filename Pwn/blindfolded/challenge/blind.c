#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_RESET   "\x1b[0m"
#define CLEAR_SCREEN  "\x1b[2J\x1b[H"

void setup_io() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void print_logo() {
    printf(COLOR_GREEN);
    printf("██╗  ██╗       █████╗ ██████╗\n");
    printf("╚██╗██╔╝      ██╔══██╗██╔══██╗\n");
    printf(" ╚███╔╝ █████╗██║  ██║██████╔╝\n");
    printf(" ██╔██╗ ╚════╝██║  ██║██╔══██╗\n");
    printf("██╔╝╚██╗      ╚█████╔╝██║  ██║\n");
    printf("╚═╝  ╚═╝       ╚════╝ ╚═╝  ╚═╝\n");
    printf(COLOR_RESET);
}

const char *format_specifiers[] = {
    "%d", "%i", "%u", "%o", "%x", "%X", "%p", "%f", "%e", "%E", "%g", "%G", "%c", "%s", "%n", "%%",
    "%hd", "%hu", "%ho", "%hx", "%hX", "%hf", "%he", "%hE", "%hg", "%hG", 
    "%lld", "%llu", "%llx", "%llX", "%llf", "%lle", "%llE", "%llg", "%llG",
    "%jd", "%ju", "%jo", "%jx", "%jX", "%jf", "%je", "%jE", "%jg", "%jG",
    "%zd", "%zu", "%zo", "%zx", "%zX", "%zf", "%ze", "%zE", "%zg", "%zG",
    "%td", "%tu", "%to", "%tx", "%tX", "%tf", "%te", "%tE", "%tg", "%tG",
    "%Lf", "%Le", "%LE", "%Lg", "%LG",
    "%*d", "%*s", "%.*f", "%.*s", "%*.*f", "%*.*s",
    "$d", "$i", "$u", "$o", "$x", "$X", "$p", "$f", "$e", "$E", "$g", "$G", "$c", "$s", "$n", "$$",
    "$hd", "$hu", "$ho", "$hx", "$hX", "$hf", "$he", "$hE", "$hg", "$hG", 
    "$lld", "$llu", "$llx", "$llX", "$llf", "$lle", "$llE", "$llg", "$llG",
    "$jd", "$ju", "$jo", "$jx", "$jX", "$jf", "$je", "$jE", "$jg", "$jG",
    "$zd", "$zu", "$zo", "$zx", "$zX", "$zf", "$ze", "$zE", "$zg", "$zG",
    "$td", "$tu", "$to", "$tx", "$tX", "$tf", "$te", "$tE", "$tg", "$tG",
    "$Lf", "$Le", "$LE", "$Lg", "$LG",
    "$*d", "$*s", "$.*f", "$.*s", "$*.*f", "$*.*s"
};

int contains_format_specifier(const char *input) {
    for (int i = 0; i < sizeof(format_specifiers) / sizeof(format_specifiers[0]); i++) {
        if (strstr(input, format_specifiers[i]) != NULL) {
            return 1;
        }
    }
    return 0;
}

void sanitize_input(char *input) {
    char *src = input, *dst = input;
    while (*src) {
        if (isprint((unsigned char)*src)) {
            *dst++ = *src;
        }
        src++;
    }
    *dst = '\0';
}

void win() {
    printf(COLOR_YELLOW "Message from Hadi: Congrats on finding the secret codes! God, I hate this company—here’s your reward while I go hide in the server room." COLOR_RESET);
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) {
        printf(COLOR_RED "Error: Could not open flag.txt. Please contact an administrator.\n" COLOR_RESET);
        return;
    }

    char flag[100];
    if (fgets(flag, sizeof(flag), file) == NULL) {
        printf(COLOR_RED "Error: Could not read flag.txt. Please contact an administrator.\n" COLOR_RESET);
        fclose(file);
        return;
    }

    fclose(file);
    printf(COLOR_YELLOW "%s" COLOR_RESET, flag);
}

void print_banner() {
    printf(CLEAR_SCREEN);
    print_logo();

    printf("\n");
    printf("Welcome to the Data Purification and Storage System (DPSS)\n");
    printf("This system ensures that all stored data is clean and free of non-printable characters.\n");
    printf(COLOR_YELLOW "Note: Our intern Hadi left some... interesting code in the binary.\n");
    printf(COLOR_YELLOW "He claims it's 'essential for debugging,' but honestly, we're not sure what it does.\n");
    printf(COLOR_YELLOW "Just ignore it and focus on the data purification process.\n\n" COLOR_RESET);
}

void process_input() {
    printf(COLOR_BLUE "Please enter the data you wish to store. DPSS will automatically purify it.\n");
    printf("> " COLOR_RESET);

    char user_input[256];
    if (gets(user_input) == NULL) {
        printf(COLOR_RED "Error reading input. Please try again.\n" COLOR_RESET);
        return;
    }

    user_input[strcspn(user_input, "\n")] = '\0';

    if (contains_format_specifier(user_input)) {
        printf("\n");
        printf(COLOR_RED "Haha! You really thought you could leak data using format strings? Nice try!\n");
        printf("But seriously, don't do that. This system is for purifying data, not exploiting it.\n" COLOR_RESET);
    } else {
        sanitize_input(user_input);

        printf("\n");
        printf(COLOR_GREEN "Data purified successfully. Stored data:\n");
        printf(COLOR_RESET);
        printf(user_input);
        printf("\n");
        printf(COLOR_GREEN "Thank you for using the Data Purification and Storage System.\n" COLOR_RESET);
    }
}

int main() {
    setup_io();
    print_banner();

    while (1) {
        process_input();
    }

    return 0;
}
