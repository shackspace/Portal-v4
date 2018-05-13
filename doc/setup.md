# Portal v4 Setup

## Installing portal v4

The script portal/bootstrap.sh should install all necessary packages on a raspbian. Users, groups and scripts are also deployed.


## Process: Opening and Closing

After connecting to the wireless of the portal a registered user can open by opening a ssh connect to the portal (ip 172.16.0.1). The usage of the user open opens the portal, the user close closes the portal.

## Process: Managing keys

Keys are managed by shackspaces internal management software (at the moment byro [https://github.com/byro/byro]). Opening and closing of the portal is done through different system users (open and close) and for each of the users a special authorized_keys file is generated.

Format for user open is:

command="/opt/Portal/portal/portal.py -a open -s $shack_id -n \"$real_name\" --nick \"$nick_name\"",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-rsa $ssh_pubkey

For user close it is:

command="/opt/Portal/portal/portal.py -a close -s $shack_id -n \"$real_name\" --nick \"$nick_name\"",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-rsa $ssh_pubkey
