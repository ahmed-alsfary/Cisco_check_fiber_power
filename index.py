import paramiko
import re
import requests

# List of devices information
devices = [
    {
        'host': '192.168.255.40',
        'username': 'username',
        'password': 'password',
        'name': 'binook'
    },
    {
        'host': '192.168.255.17',
        'username': 'username',
        'password': 'password',
        'name': 'Obaidy'
    },
    {
        'host': '192.168.255.102',
        'username': 'username',
        'password': 'password',
        'name': 'Shaab'
    },
    {
        'host': '192.168.255.174',
        'username': 'username',
        'password': 'password',
        'name': 'Taji'
    },
    {
        'host': '192.168.255.205',
        'username': 'username',
        'password': 'password',
        'name': '7 Qsoor'
    },
    {
        'host': '192.168.255.249',
        'username': 'username',
        'password': 'password',
        'name': 'Baladiat Old'
    },
    {
        'host': '192.168.255.241',
        'username': 'username',
        'password': 'password',
        'name': 'Baladiat New'
    },
    {
        'host': '192.168.255.43',
        'username': 'username',
        'password': 'password',
        'name': 'Ameen'
    },
    {
        'host': '192.168.255.7',
        'username': 'username',
        'password': 'password',
        'name': 'Dora'
    },
    {
        'host': '192.168.255.8',
        'username': 'username',
        'password': 'password',
        'name': 'Siha'
    },
    {
        'host': '192.168.255.35',
        'username': 'username',
        'password': 'password',
        'name': 'Ghazalia'
    },
    {
        'host': '192.168.255.33',
        'username': 'username',
        'password': 'password',
        'name': 'Hussainia New'
    },
    {
        'host': '192.168.255.170',
        'username': 'username',
        'password': 'password',
        'name': 'Hussainia Old'
    },
    {
        'host': '192.168.255.32',
        'username': 'username',
        'password': 'password',
        'name': 'Madina'
    },
    {
        'host': '192.168.255.36',
        'username': 'username',
        'password': 'password',
        'name': 'Watheq'
    },
    {
        'host': '192.168.255.137',
        'username': 'username',
        'password': 'password',
        'name': 'Mahmoodia New'
    },
    {
        'host': '192.168.255.29',
        'username': 'username',
        'password': 'password',
        'name': 'Zaafarania'
    },
    {
        'host': '192.168.255.146',
        'username': 'username',
        'password': 'password',
        'name': 'Jihad'
    },
    {
        'host': '192.168.255.57',
        'username': 'username',
        'password': 'password',
        'name': 'Jamiaa'
    },
    {
        'host': '10.40.40.4',
        'username': 'username',
        'password': 'password',
        'name': 'Baoia'
    },
    {
        'host': '192.168.255.24',
        'username': 'username',
        'password': 'password',
        'name': 'Bob Al-Sham'
    },
    # Add more devices here
]

# Iterate over devices and perform the check
for device in devices:
    host = device['host']
    username = device['username']
    password = device['password']

    try:
        # Create SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        # Check ports from 1/2 to 1/50 on the current device
        for port_number in range(2, 51):
            port_name = f"1/{port_number}"

            # Execute commands to check the interfaces and transceiver details
            command = f'show interface eth {port_name} transceiver details'
            stdin, stdout, stderr = ssh.exec_command(command)

            # Read the command output
            output = stdout.read().decode('utf-8')

            # Extract the required information using regex
            matches = re.findall(r"Ethernet(\d+/\d+)\n\s+transceiver is (present|not present)\n\s+type is (\w+)(?:[\s\S]*?Rx Power\s+(\S+)\s+\S+\s+\S+\s+\S+\s+(\S+))?", output)

            # Process and print the extracted information
            for match in matches:
                port = match[0]
                fiber_port = match[2]
                port_status = match[1]
                rx_power_str = match[3]  # Rx Power as string

                # Check if Rx Power is greater than 10 dBm
                if rx_power_str and rx_power_str != 'N/A':
                    rx_power = float(rx_power_str)
                    if rx_power < -17:
                        print("Device:", device['name'])
                        print("Port:", port)
                        print("Fiber Port:", fiber_port)
                        print("Port Status:", port_status)
                        print("Rx Power:", rx_power_str, "dBm")
                        print("--------")

                        # Send message with port result
                        message = f"Port {port} on device {device['name']} has Rx Power of {rx_power_str} dBm"
                        message_url = f"http://192.168.224.177:8040/api/sendWhatsApp?to=120363046451528270@g.us&message={message}"
                        response = requests.get(message_url)
                        if response.status_code == 200:
                            print("Message sent successfully!")
                        else:
                            print("Failed to send message.")

        # Close the SSH connection
        ssh.close()

    except paramiko.AuthenticationException:
        print(f"Authentication failed for device: {host}")
    except paramiko.SSHException as ssh_ex:
        print(f"SSH error occurred for device: {host} - {str(ssh_ex)}")
    except Exception as ex:
        print(f"An error occurred for device: {host} - {str(ex)}")

    # Continue with the next device
    continue
