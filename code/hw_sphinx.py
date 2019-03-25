import paramiko
from os.path import expanduser


def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    """Connect SSH to an EC2 instance and return SSH"""
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    """ Create/update the environment"""
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create\
         -f ~/msds603_instructor/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update\
             -f ~/msds603_instructor/environment.yml")
        print(stdout.read())


def main():
    """Implement functions using the provided user credentials"""
    ec2_address = "ec2-12-123-123-123.us-west-2.compute.amazonaws.com"
    user = "ec2-user"
    key_file = "/.ssh/msan603.pem"

    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    create_or_update_environment(ssh)


if __name__ == '__main__':
    main()
