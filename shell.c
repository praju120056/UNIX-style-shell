//this is a replication of the c shell in unix
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

#define MAX_CMD_LEN 1024
#define MAX_ARGS 100

typedef enum
{
    CMD_PWD,
    CMD_CP,
    CMD_MV,
    CMD_LN,
    CMD_CAT,
    CMD_EXTERNAL,
    CMD_UNKNOWN
} CommandType;

CommandType get_command_type(char *cmd);
void execute_command(CommandType cmd_type, char *args[]);
void execute_external(char *args[]);

int main()
{
    char input[MAX_CMD_LEN];

    while (1)
    {
        printf("myshell> ");
        if (!fgets(input, MAX_CMD_LEN, stdin))
            break;

        input[strcspn(input, "\n")] = '\0'; // Remove newline

        char *args[MAX_ARGS];
        char *token = strtok(input, " ");
        int i = 0;
        while (token != NULL)
        {
            args[i++] = token;
            token = strtok(NULL, " ");
        }
        args[i] = NULL;

        if (args[0] == NULL)
            continue; // Empty input

        CommandType cmd_type = get_command_type(args[0]);
        execute_command(cmd_type, args);
    }

    return 0;
}

CommandType get_command_type(char *cmd)
{
    if (strcmp(cmd, "pwd") == 0)
        return CMD_PWD;
    if (strcmp(cmd, "cp") == 0)
        return CMD_CP;
    if (strcmp(cmd, "mv") == 0)
        return CMD_MV;
    if (strcmp(cmd, "ln") == 0)
        return CMD_LN;
    if (strcmp(cmd, "cat") == 0)
        return CMD_CAT;
    return CMD_EXTERNAL;
}

void execute_command(CommandType cmd_type, char *args[])
{
    switch (cmd_type)
    {
        case CMD_PWD:
        {
            char cwd[1024];
            if (getcwd(cwd, sizeof(cwd)))
            {
                printf("%s\n", cwd);
            }
            else
            {
                perror("pwd");
            }
            break;
        }
        case CMD_CP:
            if (args[1] && args[2])
            {
                FILE *src = fopen(args[1], "r");
                FILE *dest = fopen(args[2], "w");
                if (!src || !dest)
                {
                    perror("cp");
                    return;
                }
                char buffer[1024];
                size_t bytes;
                while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0)
                {
                    fwrite(buffer, 1, bytes, dest);
                }
                fclose(src);
                fclose(dest);
            }
            else
            {
                printf("Usage: cp <source> <destination>\n");
            }
            break;
        case CMD_MV:
            if (args[1] && args[2])
            {
                if (rename(args[1], args[2]) != 0)
                {
                    perror("mv");
                }
            }
            else
            {
                printf("Usage: mv <source> <destination>\n");
            }
            break;
        case CMD_LN:
            if (args[1] && args[2])
            {
                if (link(args[1], args[2]) != 0)
                {
                    perror("ln");
                }
            }
            else
            {
                printf("Usage: ln <source> <destination>\n");
            }
            break;
        case CMD_CAT:
        {
            if (!args[1])
            {
                printf("Usage: cat <filename>\n");
                return;
            }
            FILE *file = fopen(args[1], "r");
            if (!file)
            {
                perror("cat");
                return;
            }
            char ch;
            while ((ch = fgetc(file)) != EOF)
            {
                putchar(ch);
            }
            fclose(file);
            break;
        }
        case CMD_EXTERNAL:
            execute_external(args);
            break;
        default:
            printf("Unknown command: %s\n", args[0]);
    }
}

void execute_external(char *args[])
{
    pid_t pid = fork();
    if (pid == 0)
    {
        execvp(args[0], args);
        perror("execvp");
        exit(1);
    }
    else if (pid > 0)
    {
        wait(NULL);
    }
    else
    {
        perror("fork");
    }
}
