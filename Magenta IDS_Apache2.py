#!/usr/bin/env python3

ip_dict = {}
counter = 0
target_num = 3
message = "BLOCKED!"

# open the apache logfile and parse it for key fields
with open('apache.log') as f:
    lines = f.readlines()

    for line in lines:
        line = line.strip()
        split_line = line.split()

        if '401 HTTP' in line:
            srcIP = split_line[0]

            if srcIP in ip_dict:
                ip_dict[srcIP] += 1
            else:
                ip_dict[srcIP] = 1

    sorted_ips = sorted(ip_dict.items(), key=lambda x: x[1])

    for each_pair in sorted_ips:
        ip = each_pair[0]
        count = each_pair[1]

        # Trigger alert if 3 or more failed logins from same IP
        if count >= 3:

            import requests
            import json

            # Set the webhook URL and the message to send (EDIT THIS)
            webhook_url = "Slack-webhook.here"
            message = {"text": "ALERT: MULTIPLE UNSUCCESSFUL SSH LOGIN ATTEMPTS!"}

            # Send the HTTP POST request to the Slack webhook URL
            response = requests.post(webhook_url, data=json.dumps(message),
                                     headers={"Content-Type": "application/json"})

            # Check the response status code and print the response text
            if response.status_code == 200:
                print("Slack Alert Sent - Apache2")
            else:
                print("Error sending message:", response.text)

            import smtplib

            try:
                # create an SMTP session
                smtp = smtplib.SMTP('smtp.gmail.com', 587)

                # use TLS for added security
                smtp.starttls()

                # user auth (EDIT THIS)
                smtp.login("----@gmail.com", "password")

                # define the alert message
                message = "MULTIPLE FAILED SSH LOGIN ATTEMPTS"

                # sending the email (EDIT THIS)
                smtp.sendmail("----@gmail.com", "----@gmail.com", message)

                # Terminating the session
                smtp.quit()
                print("Email Alert Sent - Apache2")

            except Exception as ex:
                print("Error: ", ex)

    print("Recommend updating UFW rules with: ufw deny from " + srcIP)