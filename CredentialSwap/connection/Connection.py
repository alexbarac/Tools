import paramiko


class Connection:
    """Client to interact with a remote host via SSH & SCP."""
    host_name = "bd23w-ssdd.com"
    port = '22'
    username = "test"

    def __init__(self, values):
        self.branch = values[0]
        self.env = values[1]
        self.type = values[2]

    def _connect(self):
        self.commands = []
        self.key = paramiko.RSAKey.from_private_key_file("connection/key.pem")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()

        print("connecting")
        self.client.connect(hostname=self.host_name, port=self.port, username=self.username, pkey=self.key)
        print("connected")

        ftp = self.client.open_sftp()

        if self.type == 'v2':
            file = ftp.file("/var/www/vhosts/" + self.branch + "/core/credentials.php", "w")
            file.write("<?php $credentials = new " + self.env + "Credentials();")
            file.close()
        else:
            if "Beta" in self.env:
                self.env = "live"
            else:
                self.env = "livetest"
            file = ftp.file("/var/www/vhosts/" + self.branch + "/credentials.php", "w")
            file.write('<?php include("' + self.env + '.credentials.inc.php");')
            file.close()
        file.flush()
        ftp.close()
        self.client.close()

##branch cloud2-1875  cloud-4394
