import difflib

from ai.commands import (
    ask_command,
    explain_command,
    fix_command,
    review_command,
    generate_command,
    save_command,
    run_command,
    models_command,
    model_command,
    use_command,
    ai_status_command,
    config_command,
    help_command,
    install_command,
    savecode_command,
    plugins_command,
    load_command,
    unload_command,
    exec_command,
    plugin_info_command,
    plugin_create_command,
    plugin_edit_command,
    plugin_show_command,
    edit_command,
    view_command,
    reload_command,
    find_command,
    theme_command,
    history_command,
    history_clear_command,
    stats_command,
    reload_all_command,
    which_command,
    alias_command,
    aliases_command,
    unalias_command,
    autoload_command,
    unautoload_command,
    autoload_list_command,
    version_command,
    sysinfo_command,
    backup_config_command,
)

COMMANDS = [
    "ls",
    "cd",
    "pwd",
    "cat",
    "mkdir",
    "touch",
    "rm",
    "astrafetch",
    "clear",
    "exit",

    "/help",
    "/ask",
    "/explain",
    "/fix",
    "/review",
    "/generate",

    "/models",
    "/model",
    "/use",
    "/save",
    "/savecode",
    "/run",
    "/install",
    "/plugins",
    "/plugin-info",
    "/plugin-create",
    "/plugin-edit",
    "/plugin-show",
    "/load",
    "/unload",
    "/exec",

    "/ai-status",
    "/config",
    "/edit",
    "/view",
    "/reload",
    "/reload-all",
    "/which",
    "/find",
    "/theme",
    "/history",
    "/history-clear",
    "/stats",
    "/alias",
    "/aliases",
    "/unalias",
    "%who",
    "%reset",
    "%time",
    "/autoload",
    "/unautoload",
    "/autoload-list",
    "%history",
    "//",
    "/version",
    "/sysinfo",
    "/backup-config",
    "%whos",
    "%env",
    "%mem",
    "%bench",
    "%sys",
    "%save-session",
    "%load-session",
    "%del",
    "%rename",
    "%copy",
    "%vars",
    "%clear-vars",
    "%json",
    "%csv",
]


def handle_command(command):

    command = command.strip()

    parts = command.split(maxsplit=1)

    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""
    
    if cmd == "//":

        print(
"""
Quick Commands
==============

/help
/stats
/plugins
/find
/theme

/alias
/aliases

/reload-all
/autoload-list

%who
%history
"""
        )

        return True
    
    if cmd == "/theme":
        return theme_command(arg)

    if cmd == "/ask":
        return ask_command(arg)

    if cmd == "/explain":
        return explain_command(arg)

    if cmd == "/edit":
        return edit_command(arg)
        
    if cmd == "/which":
        return which_command(arg)    

    if cmd == "/view":
        return view_command(arg)
    
    if cmd == "/fix":
        return fix_command(arg)

    if cmd == "/review":
        return review_command(arg)

    if cmd == "/generate":
        return generate_command(arg)

    if cmd == "/save":
        return save_command(arg)
        
    if cmd == "/savecode":
        return savecode_command(arg)

    if cmd == "/use":
        return use_command(arg)
        
    if cmd == "/run":
        return run_command(arg)
        
    if cmd == "/install":
        return install_command(arg)
        
    if cmd == "/load":
        return load_command(arg)

    if cmd == "/find":
        return find_command(arg)

    if cmd == "/unload":
        return unload_command(arg)

    if cmd == "/exec":
        return exec_command(arg)

    if cmd == "/unalias":
        return unalias_command(arg)

    if cmd == "/plugin-info":
        return plugin_info_command(arg)

    if cmd == "/plugin-create":
        return plugin_create_command(arg)

    if cmd == "/plugin-edit":
        return plugin_edit_command(arg)
                
    if cmd == "/plugin-show":
        return plugin_show_command(arg)
    
    if cmd == "/reload":
        return reload_command(arg)
    
    if cmd == "/alias":
        return alias_command(arg)

    if cmd == "/autoload":
        return autoload_command(arg)

    if cmd == "/unautoload":
        return unautoload_command(arg)

    if cmd == "/autoload-list":
        return autoload_list_command()

    if cmd == "/aliases":
        return aliases_command()
    
    if cmd == "/stats":
        return stats_command()
    
    if cmd == "/plugins":
        return plugins_command()

    if cmd == "/history":

        return history_command()

    if cmd == "/history-clear":

        return history_clear_command()

    if cmd == "/models":
        return models_command()

    if cmd == "/version":
        return version_command()

    if cmd == "/reload-all":
        return reload_all_command()

    if cmd == "/backup-config":
        return backup_config_command()

    if cmd == "/model":
        return model_command()

    if cmd == "/sysinfo":
        return sysinfo_command()

    if cmd == "/ai-status":
        return ai_status_command()

    if cmd == "/config":
        return config_command()

    if cmd == "/help":
        return help_command()

    matches = difflib.get_close_matches(
        cmd,
        COMMANDS,
        n=3,
        cutoff=0.5
    )

    print(
        "\nUnknown command."
    )

    if matches:

        print(
            "\nDid you mean?\n"
        )
    
        for match in matches:

            print(match)

    return True