import webbrowser
from Automation.web_data import websites

def open_website(web_name, is_single_key=False):
    
    if is_single_key and web_name.lower() in websites:
        url = "https://" + websites[web_name.lower()]
        webbrowser.open(url)
        print(f"Opened website: {url}")
        return
    
    websites_name = web_name.lower().split()    
    counts = {}
    for name in websites_name:
        counts[name] = counts.get(name, 0) + 1
    
    url_open = []

    for name,count in counts.items():
        if name in websites:
            url = "https://" + websites[name]
            url_open.extend([url] * count)
        else:
            print(f"Website '{name}' not found in the list.")

    for url in url_open:
        webbrowser.open(url)
    
    if url_open:
        print("Opened websites:", ", ".join(url_open))
    else:
        print("No websites found.")


while True:
   web_input = input("Enter website names to open (or 'exit' to quit): ")
   if web_input.lower() == 'exit':
       break
   open_website(web_input)