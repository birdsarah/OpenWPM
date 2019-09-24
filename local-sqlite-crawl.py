from automation import CommandSequence, TaskManager

import csv

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
with open('alexatop1k.csv', 'r') as f:
    reader = csv.reader(f)
    sites = [item for sublist in list(reader) for item in sublist]

sites = sites[0:200]

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Enable flash for all three browsers
    browser_params[i]['disable_flash'] = True
    # Run headless crawl
    browser_params[i]['headless'] = True
    browser_params[i]['extension_enabled'] = True
    browser_params[i]['save_content'] = False

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = 'crawls/crawl-data-6/'
manager_params['log_directory'] = 'crawls/crawl-data-6/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence('http://'+site, reset=True)

    # Start by visiting the page
    command_sequence.get(sleep=10, timeout=60)

    # index='**' synchronizes visits between the three browsers
    manager.execute_command_sequence(command_sequence, index='**')

# Shuts down the browsers and waits for the data to finish logging
manager.close()
