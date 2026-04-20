# LabUptimeDashboard
A better way to view devices and labs on our lab network than a whiteboard, using homepage and gatus  
# Components
**Homepage:** easy-to-customize dashboard framework. Read the docs at https://gethomepage.dev/  
**Gatus:** the backend that runs service uptime checks displayed by Gatus. Read the docs at https://gatus.io/  
**py-proxy:** python middleware used by the other 2 docker containers. Translates data exposed by Gatus API to the format Homepage expects it in.  

# Initial Setup
Create a `.env` file in the project root that `docker-compose.yml` will read from. Set the following 2 variables:  
``` sh
# this is the URL of Gatus backend. Ensure the py-proxy container can access this URL.  
GATUS_URL=http://x.x.x.x:3002/api/v1/endpoints/statuses
# this is the IP address of the Homepage frontend that the end user is allowed to reach the frontend.  
HOMEPAGE_ALLOWED_HOSTS=x.x.x.x:3000
```
From the project root, start the containers with: `docker compose up -d`  
Go to the URL that you specified as `HOMEPAGE_ALLOWED_HOST` in your browser to ensure this is working. The next section walks you through adding services and customize the dashboard.  
# Modifying dashboard
### Configure Uptime Checkers with Gatus
First, create a new uptime check using gatus. Browse to `gatus/config.yaml`. For each service, add an entry using the below templates. In many cases, you want to perform multiple checks on the same endpoint. You should specify a separate entry for each check
``` yml
  - name: template HTTP website     # name the check
    group: example                  # logical group to add the check to
    url: "http://x.x.x.x:xxxx"      # endpoint that Gatus will contact
    interval: xxs                   # frequency of check in seconds, ex 60s
    conditions:
      - "[STATUS] == 200"           # the condition for success, in this case, site returns 200

  - name: template open TCP port
    group: example                  # this check will be in the same group (example) as "template HTTP website"
    url: "tcp://x.x.x.x:22"         # you can use raw TCP/UDP sockets for checks
    interval: xxs
    conditions:
      - "[CONNECTED] == true"       # the condition for success, in this case, connection is accepted/port is open

```
Browse to the gatus frontend on port 3002 in your browser. Use the `GATUS_URL` variable specified earlier. You should see the groups you specified displayed as dropdown menus. In each group, there should be a tile for each of the services above.  

### Verify the Middleware
Next, the data will be ingested from gatus into the python middleware. **No configuration is needed here.** The proxy is only exposed to localhost on the machine you are running from. To display the output for verfication and troubleshooting, you can `curl http://127.0.0.1:5000/status`. You should see the hosts in Gatus displayed in JSON format.  

### Populate the Dashboard with Hosts and Checkers
Finally, you need to link the homepage frontend to the backend. This is done by modifying `homepage/config.yaml`. The simplest thing you can do is a tile with a note, which will usually be a host with its IP address. You can use the template below for:  
``` yml
- group 1:
  - simple-host:
      # use a filename found in https://github.com/homarr-labs/dashboard-icons/tree/main
      # or use a custom icon by placing it in the public/icons directory and referencing it with /icons/filename.ext
      icon: 1337x
      # put the IP here or any other description you'd like to show on the card
      description: "x.x.x.x"
```

For most hosts, you will want to link one or more uptime checks from Gatus. Use the template below to get started:  
1. Create the groups that machines will be nested under in the top level of the yml.  
2. Create the host 1 indent in. Each of these is represented as a tile on homepage.   
3. In the "widgets" attribute of each host, create a separate "mapping" entry for each check you added in gatus for that host. Each of these is displayed as a box within the tile from step 2. This is usually used to check for multiple open ports on the same device.  
``` yml
- group 1:
  - full-host:
      # use a filename found in https://github.com/homarr-labs/dashboard-icons/tree/main
      # or use a custom icon by placing it in the public/icons directory and referencing it with /icons/filename.ext
      icon: 1337x
      # put the IP here or any other description you'd like to show on the card
      description: "x.x.x.x"
      # this entry turns the tile into a clickable link to the specified URL
      href: http://x.x.x.x
      # this entry enables ping monitoring for the specified IP address, shown as a red/green in the top left corner
      ping: x.x.x.x
      # this entry adds your service checks by pointing to py-proxy. Don't change anything between here and mappings
      widgets:
          - type: customapi
            url: http://172.18.0.1:5000/status
            refreshInterval: 10000
            mappings:
              # this section maps the entry to the gatus field. Specify it as group_checkname.online
              # replace any spaces in the gatus name with hyphens. All lowercase.
              - field: "group_gatusname.online"
              # this is what you want displayed on the dashboard for this check.
              # I usually specify service name (:port)
                label: "check name (:1337)"
              # leave format as text for a simple online/offline status.
                format: text
              - field: "group_name-with-spaces.online"
                label: "check name with spaces (:1234)"
                format: text
```

# Miscellaneous Configuration
The header is specified in `homepage/widgets.yaml`  
``` yml
- greeting:
    text_size: xl
    text: "text to display at the top of the dashboard"
```

The columns are specified in `homepage/settings.yaml` under `layout`:  
``` yml
layout:
  column 1 name displayed in homepage:
    style: column
    columns: 1  # display as 1 column (no internal splitting)
    col: 1      # column number from left to right
  column 2 name displayed in homepage:
    style: column
    columns: 1
    col: 2
```

CSS Injection can be used for customization via `homepage/custom.css`
