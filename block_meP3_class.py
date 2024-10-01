#!/usr/bin/python3

import subprocess
import datetime
import smtplib

class IPBlocker:
    def __init__(self):
        self.whitelist = [
            '156.119.190.184', '156.119.195.42', '10.162.61.79', '127.0.0.1',
            '149.101.1.118',  # DOJ added 8/15/2017
            '66.104.15.23'    # BNC added 8/25/2017
        ]
        self.generic_suffix = "something.xxx.example"
        self.admin_email = f"somone@{self.generic_suffix}"
        self.my_host = f"ecf.{self.generic_suffix}"
        self.smtp_host = "smtp.someplace.xxx.example"
        self.carbon_copy_email = [
            f"myemail@{self.generic_suffix}",
            f"myemail2@{self.generic_suffix}"
        ]
        self.block_value = 200
        self.alert_value = 5
        self.log_file = '/var/tmp/logfile_block_me.txt'

    def get_active_connections(self):
        cmd = "ss -ntu | awk '{print $5}' | cut -d: -f1 | grep -v '[ervers|ddress]' | sort | uniq -c | sort -n"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)
        return proc.stdout.read().split('\n')

    def block_ip(self, ip):
        oct1, oct2, oct3, oct4 = ip.split(".")
        if int(oct1) > 0 and len(ip) > 8:
            print(f"Running firewall block rule for {ip}...")
            cmd = f"/sbin/iptables -I INPUT 1 -s {ip} -j DROP"
            print(cmd)
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    def write_message_to_log(self, first_part, second_part):
        d = self.get_date("2")
        with open(self.log_file, 'a') as f:
            if first_part:
                line_string = f"{d}:{first_part} {second_part}\n"
            else:
                line_string = f"{d},{second_part}\n"
            f.write(line_string)
        print("Message written to log.")

    def get_date(self, format_type):
        now = datetime.datetime.now()
        if format_type == "1":
            return now.strftime("%Y-%m-%d_%H:%M:%S ")
        elif format_type == "2":
            return now.strftime("%Y-%m-%d,%H:%M:%S")
        else:
            return str(datetime.date.today())

    def send_email(self, count, ip):
        fromaddr = f"From: {self.my_host} <{self.admin_email}>"
        toaddr = f"To: <{self.admin_email}>"
        subject = f"Subject: blocking ip {ip}"
        
        header = f"{fromaddr}\r\n{toaddr}\r\n"
        for cc_email in self.carbon_copy_email:
            header += f"cc: <{cc_email}>\r\n"
        header += f"{subject}\r\n"

        body = (f"{header}Hello,\r\nWe detected a LARGE AMOUNT of tcp connections to {self.my_host}. "
                f"There are {count} connections from {ip} so we blocked them.\r\n\r\n"
                "************************\r\n"
                "##########\r\nUSBC\r\nSystems\r\nTel: 410-962-XXXX\r\n###########")

        server = smtplib.SMTP(self.smtp_host)
        server.set_debuglevel(1)
        server.sendmail(self.admin_email, [self.admin_email] + self.carbon_copy_email, body)
        server.quit()

    def process_connections(self):
        for conn in self.get_active_connections():
            parts = conn.split()
            if len(parts) == 2:
                count, ip = parts
                if ip not in self.whitelist:
                    count = int(count)
                    if count > self.block_value:
                        self.write_message_to_log("BLOCKED", f"{ip},{count}")
                        self.send_email(count, ip)
                        print(f"BLOCKING {ip} - {count}")
                        self.block_ip(ip)
                    elif count > self.alert_value:
                        print(f"ALERT {ip} - {count}")
                        self.write_message_to_log("", f"ALERT,{ip},{count}")
                    else:
                        date = self.get_date("2")
                        print(f"{date},{count},connections from,{ip}")

if __name__ == "__main__":
    blocker = IPBlocker()
    blocker.process_connections()
