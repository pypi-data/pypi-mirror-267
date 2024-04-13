import json
import pathlib
import re
import sys

import edwh
import invoke
import yaml
from invoke import task


@task(name="install", pre=[edwh.tasks.require_sudo])
def install_multipass(c):
    if not c.run("multipass --version", warn=True, hide=True).ok:
        print(" [ ] Multipass not found. installing...")
        c.sudo("snap install multipass")
        print(" [x] Multipass installed")
    else:
        print(" [x] Multipass already installed")


def generate_key(c, comment: str, filename: str):
    c.run(f'ssh-keygen -t ed25519 -C "{comment}" -f {filename} -N ""')


@task(name="fix-host", aliases=["fix-dns"], iterable=["hostname"], pre=[edwh.tasks.require_sudo])
def fix_hosts_for_multipass_machine(c, machine_name, hostname=()):
    if not machine_name:
        print("Machine name required. Use -m or --machine-name", file=sys.stderr)
    output = c.run("multipass list --format yaml", hide=True).stdout.strip()
    machines = yaml.load(output, yaml.SafeLoader)
    if machine_name not in machines:
        print(
            f"'{machine_name}' not found. Choose one of: {', '.join(machines.keys())}",
            file=sys.stderr,
        )
        exit(1)
    machine = machines[machine_name][0]
    if machine["state"] != "Running":
        print(
            f"'{machine_name}' is not running.",
            file=sys.stderr,
        )
        if input("Should i start the machine for you? [Yn]") in ("y", "Y", ""):
            c.run(f"multipass start {machine_name}")
        return fix_hosts_for_multipass_machine(c, machine_name)
    first_address = machine["ipv4"][0]
    # start with the given hostnames (it's iterable, so should be a list style or default empty tuple)
    hostnames = list(hostname)
    # register the hostname
    hostnames.append(machine_name)
    # only unique values
    hostnames = list(set(hostnames))
    with open("/etc/hosts", "r") as hosts_handle:
        host_lines = hosts_handle.read().split("\n")
        found = any(name for name in hostnames if name in " ".join([line.split("#")[0] for line in host_lines]))
        if found:
            print("Updating hosts file")
            if len(hostname) > 1:
                print("You have entered hostnames, that argument is incompatible with the upgrade. ")
                print("Edit /etc/hosts manually to register aliases manually")
            new_hosts = []
            for line in host_lines:
                if any(True for name in hostnames if name in line):
                    # line found, replace ip adress: convert tabs to spaces
                    line = line.replace("\t", "    ")
                    # create a new line with the ipv, whitespace, and the remainder of the original
                    # line (everything after the first space), replacing multiple spaces with one.
                    new_hosts.append(re.sub(r"  +", " ", f'{first_address}      {line.split(" ", 1)[1]}'))
                    print(new_hosts[-1])
                else:
                    new_hosts.append(line)
            c: invoke.Context
            overwrite_hosts_command = (
                """python3 -c "import sys \nwith open('/etc/hosts','w') as h: h.write(sys.stdin.read().strip())" <<EOFEOFEOF\n"""
                + "\n".join(new_hosts)
            )
            overwrite_hosts_command += "\nEOFEOFEOF"
            c.sudo("ls >> /dev/null")  # force a sudo to ask for password
            c.sudo(overwrite_hosts_command)
        else:
            print("Appending to hosts file")
            c.sudo("ls >> /dev/null")  # force a sudo to ask for password
            line_to_append = re.sub(r"  +", " ", f"{first_address}  {' '.join(hostnames)}")
            print(line_to_append)
            # simpelweg overschrijven via een echo of cat >> /etc/hosts mag niet. dus dan maar via een python script.
            c.sudo(f'''python3 -c "with open('/etc/hosts','a') as h: h.write('{line_to_append}')"''')


@task(name="list")
def list_machines(c, quiet=False):
    output = c.run("multipass list --format json", hide=True).stdout
    if quiet:
        return json.loads(output)["list"]
    else:
        print(output)


@task(pre=[install_multipass], name="prepare")
def prepare_multipass(c, machine_name):
    print(" ... Searching for vms")
    machines = list_machines(c, quiet=True)
    # convert to lookup by name
    machines = {m["name"]: m for m in machines}
    if machine_name not in machines:
        raise KeyError(
            f'Machine name "{machine_name}" not found in multipass. Available names: {", ".join(list(machines.keys()))}'
        )
    machine = machines[machine_name]
    ip = machine["ipv4"][0]
    print(f" [x] {machine_name} found @ {ip} ")
    multipass_keyfile = pathlib.Path("~/.ssh/multipass.key").expanduser()
    if not multipass_keyfile.exists():
        # create keyfile
        generate_key(c, "pyinvoke access to multipass machines", str(multipass_keyfile))
        print(" [x] created missing key file")
    else:
        print(" [x] key file exists")
    pub_file = pathlib.Path(f"{str(multipass_keyfile)}.pub")
    pub_key = pub_file.read_text().strip()
    if (
        pub_key
        in c.run(
            f'echo "cat .ssh/authorized_keys ; exit " | multipass shell {machine_name}',
            warn=False,
            hide=True,
        ).stdout
    ):
        print(" [x] public key is installed to connect")
    else:
        print(" [ ] installing public key to access machine")
        c.run(
            f'echo "echo {pub_key} >> .ssh/authorized_keys; exit" | multipass shell {machine_name}',
            hide=True,
        )
        print(f" [x] installed multipass keyfile on {machine_name}")
    edwh_cmd = pathlib.Path(sys.argv[0]).name
    print(f"Execute {edwh_cmd} with:")
    fab_commands = "|".join(c.run(f"{edwh_cmd} --complete", hide=True).stdout.strip().split("\n"))
    print(f"  {edwh_cmd} -eH ubuntu@{ip} [{fab_commands}]")
    print(f'  {edwh_cmd} -eH ubuntu@{ip} -- echo "or some other arbitrary bash command"')
