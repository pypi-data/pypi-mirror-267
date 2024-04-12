import time
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console
from art import *
import json

def askQuestion():
    data = {}
    console = Console()

    tprint("BadB", font="swampland")
    console.print("")
    console.print("[bold blue]Welcome to the BADB[/bold blue]")
    console.print("[bold blue]Create your Backend/API seamlessly[/bold blue]")
    console.print("")
    file_name = prompt("[green]Name your app [/green]", validator =lambda name: len(name) > 0)
    console.print("[green]Initializing "+file_name+".json file...[/green]")
    data['name'] = file_name
    data['secret'] = "my_secret"
    console.print("")
    prefix = None
    if(confirm("[green]Any prefix for api-endpoints ?[/green]")):
        prefix = prompt("[green]Enter prefix for api-endpoints ?[/green]", validator = lambda pr: len(pr) > 0)
        console.print("Adding prefix /"+prefix+" to api-endpoints...")

    data['prefix'] = prefix

    if(confirm("🥱 [green]Want to add schema info ?[/green]")):
        data['schema'] = {}
        add_more_table = False
        while(True):
            s_name = prompt("[green]Enter table name ?[/green]", validator = lambda pr: len(pr) > 0)
            data['schema'][s_name] = {}
            console.print("Added table "+s_name)
            add_more_var = False
            while(True):
                s_var = prompt("Add variable name (Enter) and select datatype")
                data['schema'][s_name][s_var] = "NULL"
                # console.print("Select datatype for variable")
                dataTypes = ["INT", "TEXT", "BOOLEAN", "BLOB"]
                s_var_type = select(options=dataTypes, cursor="👉")
                data['schema'][s_name][s_var] = s_var_type
                console.print(s_var+": "+s_var_type)
                add_more_var = confirm("Add another variable to schema "+s_name+" ?")
                if add_more_var:
                    continue
                else:
                    console.print("Adding variables to schema "+s_name+" ...")
                    break
            add_more_table = confirm("Want to add more tables to project ?")
            if add_more_table:
                continue
            else:
                break

        if(confirm("[green]Want to add authentication functionality to the api ?[/green]")):
            data['auth_config'] = {}
            data["auth_config"]["auth"] = True
            console.print("Adding auth functionality ...")
            tables = list(data['schema'].keys())
            console.print("[green]Select table of which variables will be used to verify credentials")
            auth_table = select(options=tables, cursor="👉")
            data["auth_config"]["table"] = auth_table
            console.print(auth_table+" table selected...")
            table_vars = list(data['schema'][auth_table].keys())
            console.print("[green]Select variable to be used for verifying email/username")
            auth_email = select(options=table_vars, cursor="👉")
            data['auth_config']["email_field"] = auth_email
            console.print(auth_email+" selected...")
            console.print("[green]Select variable to be used for verifying password")
            auth_pass = select(options=table_vars, cursor="👉")
            data["auth_config"]['pass_field'] = auth_pass
            console.print(auth_pass+" selected...")
            all_routes = ["GET", "POST", "PUT", "DELETE"]
            data["auth_config"]['auth_routes'] = {}
            for i in tables:
                data["auth_config"]['auth_routes'][i] = None
                console.print("[green]Select all ROUTES to secure for "+i+" table[/green]")
                selected_routes = select_multiple(options=all_routes, tick_character="✅")
                str_selected_routes = ""
                for val in selected_routes: str_selected_routes += val+", "
                str_selected_routes = str_selected_routes[: len(str_selected_routes)-2]
                data["auth_config"]['auth_routes'][i] = str_selected_routes
                console.print(str(selected_routes)+" selected...")
            secret = prompt("Enter the secret key for hashing passwords", validator= lambda pr: len(pr) > 0)
            data['secret'] = secret

    # if(confirm("[green]Want to add any custom routes ?[/green]")):
    #     console.print("Adding custom routes functionality ...")
    #     route_name = prompt("Enter custom route name:", validator= lambda name: len(name) > 0)
    #     console.print("Enter custom route name: [bold]"+route_name+"[/bold]")
    #     console.print("Choose route method:")
    #     route_method = select(options=all_routes, cursor="👉")
    #     console.print(route_method+" selected...")
    #     require_auth = confirm("[green]Do require authentication for this route ?")
    #     if require_auth: console.print("Adding authentication...")
    #     console.print("Select table required by the route")
    #     route_table = select(options=tables, cursor="👉")
    #     console.print(route_table+" selected...")


    with open(data['name']+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    console.print("[green bold]Run following command to create api-endpoints :[/green bold] python -m badb [cyan bold]"+file_name+".json[/cyan bold]")
    # console.print("\t[bold] badb "+file_name+".json [/bold]")


