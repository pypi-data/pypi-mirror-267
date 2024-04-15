import typer
from typing_extensions import Annotated
import requests
import os
from enum import Enum


class TYPE(str, Enum):
    a = "A"
    cname = "CNAME"
    aaaa = "AAAA"
    txt = "TXT"
    mx = "MX"


app = typer.Typer()

@app.command()
def create_record(
        zone_id: Annotated[str, typer.Argument(help="your zone id")], 
        name: Annotated[str, typer.Argument(help="name of the Cloudflare record")], 
        content: Annotated[str, typer.Argument(help="value of the Cloudflare record (what the record will resolve to)")], 
        type: Annotated[TYPE, typer.Argument(case_sensitive=True, help="type of the Cloudflare record")],
        priority: Annotated[int, typer.Option(help="priority of the TXT record", min=0, max=65535)] = 0,
        json: Annotated[bool, typer.Option(help="will output valid JSON. It can we useful when using this command in your script. Vanity logging will be disabled")] = False
    ):  
    
    token = os.getenv('CF_TOKEN')
    if not token or token == "": raise Exception(f'CF_TOKEN env variable not found or not initialized, I got: {token}')
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    data = { 
        'name': name,
        'content': content,
        'type': type 
    }
    
    if type == TYPE.mx: data['priority'] = priority

    res = requests.post(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', 
        json=data, headers=headers
    )
    
    if res.status_code != 200:
        if json: print(res.text)
        else: print(f'Error while creating the record, {res.text}')
        raise typer.Exit(code=1)
    else:
        if json: print(res.text)
        else: print(f'Record creted succesfully, {res.text}')

@app.command()
def get_records(
        zone_id: Annotated[str, typer.Argument(help="your zone id")], 
        query: Annotated[str, typer.Option(help="Text to be contained in the record's name.")] = None, 
        json: Annotated[bool, typer.Option(help="will output valid JSON. It can we useful when using this command in your script. Vanity logging will be disabled")] = False
    ):    
    
    token = os.getenv('CF_TOKEN')
    if not token or token == "": raise Exception(f'CF_TOKEN env variable not found or not initialized, I got: {token}')
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    res = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers)
    
    if res.status_code != 200:
        raise Exception(f'Request failed {res.text}')
    
    if query == None: 
        if json: print(res.json()['result'])
        else:
            for r in res.json()['result']:
                print(f'> ({r['id']}) {r['name']}: {r['content']}')

        raise typer.Exit()
    
    matches = []
    for record in res.json()['result']:
        if query in record['name']: 
            matches.append(record)
    
    if json: print(matches)
    else:
        for r in matches:
            print(f'> ({r['id']}) {r['name']}: {r['content']}')


@app.command()
def delete_record(
        zone_id: Annotated[str, typer.Argument(help="your zone id")], 
        record_id: Annotated[str, typer.Argument(help="id of the record to delete")], 
        force: Annotated[bool, typer.Option('--force', help="Do not ask for confirmation when deleting.")] = False,
    ):
    
    token = os.getenv('CF_TOKEN')
    if not token or token == "": raise Exception(f'CF_TOKEN env variable not found or not initialized, I got: {token}')

    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    record_details = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}', headers=headers)
    
    if record_details.status_code == 404: raise Exception(f'A dns record with that id does not exists: {record_details.text}')
    elif record_details.status_code != 200:
        raise Exception(f'Request failed {record_details}')
    
    res = record_details.json()['result']
    print(f'About to delete: \nid:        {res['id']}\nzone_id:   {res['zone_id']}\nname:      {res['name']}\ntype:      {res['type']}\ncontent:   {res['content']}\nzone_name: {res['zone_name']}')
    
    if force == False:
        confirm = typer.confirm("Are you sure you wanna nuke this?")

        if not confirm:
            raise typer.Abort()
        
    del_res = requests.delete(url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}', headers=headers)

    if del_res.status_code != 200:
        print(f'Error while deleting the record {del_res.text}')
    else:
        print(f'Record {res['name']} deleted')


@app.command()
def delete_records(
        zone_id: Annotated[str, typer.Argument(help="your zone id")],
        query: Annotated[str, typer.Argument(help="Text to be contained in the record's name.")],
        force: Annotated[bool, typer.Option('--force', help="Do not ask for confirmation when deleting.")] = False,
    ):
    
    token = os.getenv('CF_TOKEN')
    if not token or token == "": raise Exception(f'CF_TOKEN env variable not found or not initialized, I got: {token}')
    
    headers = {
        'Authorization': f'Bearer {token}'
    }

    res = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/', headers=headers)
    
    if res.status_code != 200:
        raise Exception(f'Request failed {res}')
    
    matches = []
    for record in res.json()['result']:
        if query in record['name']: matches.append(record)
    
    print("Matched records:")
    for m in matches:
        print(f'> {m['name']}')
        
    print("\n")
    for match in matches:    
        print(f'About to delete: \nid:        {match['id']}\nzone_id:   {match['zone_id']}\nname:      {match['name']}\ntype:      {match['type']}\ncontent:   {match['content']}\nzone_name: {match['zone_name']}\n')
        
        if force == False:
            confirm = typer.confirm("Are you sure you wanna nuke this?")

            if not confirm:
                continue
                # raise typer.Abort()
            
        del_res = requests.delete(url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{match['id']}', headers=headers)

        if del_res.status_code != 200:
            print(f'Error while deleting the record {del_res.text}')
        else:
            print(f'Record {match['name']} deleted\n')
            

if __name__ == "__main__":
    app()