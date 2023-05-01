import ovh

# Create an OVH client 
# recommended permisions [GET /vps*, GET /order*, POST /order*]
client = ovh.Client(
    endpoint='ovh-eu',                                     # Endpoint of API OVH Europe
    application_key='xxx',                    # Application Key
    application_secret='xxx', # Application Secret
    consumer_key='xxx',       # Consumer Key
)

#get list of all server names
servers = client.get('/vps')
print('Here is the list of all active servers and possible upgrade models: ')
print('For example: vps-starter-1-2-20 (model Starter - 1 vCore - 2GB RAM - 20GB SSD disk)')
# List all servers plans and available upgrades
server_upgrades_dict = {}

for server in servers:
    legit_plan_code = []
    #get get server's current plan code
    server_detail = client.get('/vps/%s' % server)
    current_plan_code = server_detail['model']['name']

    upgrade_details = client.get('/order/upgrade/vps/%s' % server)
    
    for detail in upgrade_details:
        unchecked_plan_code = detail['planCode']

        #get disk sizes from plan codes
        current_disk_size = current_plan_code[current_plan_code.rindex("-")+1:]
        unchecked_disk_size = unchecked_plan_code[unchecked_plan_code.rindex("-")+1:]

        #verify if plan code is available for upgrade 
        if int(unchecked_disk_size) >= int(current_disk_size):
            legit_plan_code.append(unchecked_plan_code)
    
    #store server as key and proper plan codes, current plan code as values
    server_upgrades_dict[server] = [legit_plan_code, current_plan_code]

#print all possibilities for an upgrade
for key, value in server_upgrades_dict.items():
    print("\n%s - %s can be upgraded to one of:\n%s" % (key, value[1], value[0]))

put_parameters = {}
server_to_upgrade = input("Provide a server name to upgrade: ")
while server_to_upgrade not in servers:
    print("You do not own %s" % server_to_upgrade)
    server_to_upgrade = input("Provide a proper server name to upgrade: ")     
put_parameters['serviceName'] = server_to_upgrade


plan_code_to_apply = input("Provide a plan code to upgrade: ")
while plan_code_to_apply not in server_upgrades_dict[server_to_upgrade][0]:
    print("Such upgrade is not possible ")
    plan_code_to_apply = input("Provide a proper plan code to upgrade: ")
put_parameters['planCode'] = plan_code_to_apply

auto_pay = input("Do you want to automatically pay with preffered payment method? [y/n]: ")
#convert to lowercase for case-insensitivity
auto_pay = auto_pay.lower()
while auto_pay not in ['y', 'n']:
    auto_pay = input("Do you want to automatically pay with preffered payment method? [y/n]: ")
    auto_pay = auto_pay.lower()
#convert input to boolean
auto_pay_boolean = True if auto_pay == 'y' else False
put_parameters['autoPayWithPreferredPaymentMethod'] = auto_pay_boolean

print('\nSummary:\nYou are upgrading %s from %s to %s\nAutomaticallypay with preffered payment method: %s' % (server_to_upgrade, server_upgrades_dict[server_to_upgrade][1], plan_code_to_apply, auto_pay_boolean))

confirmation = input("\nWrite CONFIRM to generate invoice: ")
while confirmation != 'CONFIRM':
    confirmation = input("\nWrite CONFIRM to generate invoice: ")

#upgrade the server - POST /order
client.post('/order/upgrade/vps/%s/%s' % (server_to_upgrade, plan_code_to_apply), autoPayWithPreferredPaymentMethod=auto_pay_boolean, quantity=1)
print('Generated upgrade invoice for: %s' % server_to_upgrade)







