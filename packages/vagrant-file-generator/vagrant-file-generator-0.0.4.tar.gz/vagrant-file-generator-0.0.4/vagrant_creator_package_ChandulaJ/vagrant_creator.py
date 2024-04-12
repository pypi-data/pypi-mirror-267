import os

def generate_forwarded_ports():
    forwarded_ports = []

    while True:
        add_port = input("Do you want to add a forwarded port? [y (Yes) /n (No)]: ").lower()

        if add_port != 'y':
            break

        default_guest_port = 8080;
        default_host_port = 8080;
        guest_port = input(f"Enter the guest port number (default: {default_guest_port}): ") or default_guest_port
        host_port = input(f"Enter the host port number (default: {default_host_port}): ") or default_host_port
        auto_correct = input("Enable auto correct? (default: true) [t (True) /f (False)]: ").lower()

        forwarded_ports.append({
            'guest': guest_port,
            'host': host_port,
            'auto_correct': auto_correct
        })

    return forwarded_ports


def generate_provision_commands():
    provision_commands = []

    while True:
        add_command = input("Do you want to add a provisioning command? [y (Yes) /n (No)]: ").lower()

        if add_command != 'y':
            break

        command = input("Enter the provisioning command (e.g., 'sudo yum install ansible -y'): ")

        provision_commands.append(command)

    return provision_commands


def generate_vagrantfile():
    # Default values
    print("===================================== Vagrant file generator =====================================")
    default_vm_box = "centos/7"
    default_cpu = "1"
    default_ram = "1024"
    default_machine_name = "default-machine"
    default_host_name = "localhost"
    default_ip = "192.168.33.10"

    # Ask user for input
    vm_box = input(f"Enter vm box name (default: {default_vm_box}): ") or default_vm_box
    cpu = input(f"Enter CPU (default: {default_cpu}): ") or default_cpu
    ram = input(f"Enter RAM in MB (default: {default_ram}): ") or default_ram
    machine_name = input(f"Enter Machine Name (default: {default_machine_name}): ") or default_machine_name
    host_name = input(f"Enter Host Name (default: {default_host_name}): ") or default_host_name
    ip = input(f"Enter IP Address (default: {default_ip}): ") or default_ip


    forwarded_ports = generate_forwarded_ports()
    provision_commands = generate_provision_commands()

    # Generate Vagrantfile
    with open("Vagrantfile", "w") as f:
        f.write(f'''\
Vagrant.configure("2") do |config|

config.vm.define "{machine_name}" do |machine|
	machine.vm.network "private_network", ip: "{ip}"
	machine.vm.hostname = "{host_name}"
	
 # Forwarded ports
''')

        for port in forwarded_ports:
            auto_correct_value = "false" if port["auto_correct"] == "f" else "true"
            f.write(
                f'  machine.vm.network "forwarded_port", guest: {port["guest"]}, host: {port["host"]}, auto_correct: {auto_correct_value}\n'
            )

        f.write(f'''\

 end
  config.vm.box = "{vm_box}"
 
  # Provisioning
  config.vm.provision "shell", inline: <<-SHELL
''')

        for command in provision_commands:
            f.write(f'    {command}\n')

        f.write(f'''\
  SHELL

  config.vm.provider "virtualbox" do |vb|
    vb.memory = {ram}
    vb.cpus = {cpu}
  end
end
''')

    print("Vagrantfile generated successfully!")


