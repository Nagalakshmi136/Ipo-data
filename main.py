from ipopy.ipo_data_handler import IPODataSender


def main():
    send_method = input("Enter the method of sending data (whatsapp/email): ").lower()
    ipo_data_sender = IPODataSender()
    if send_method == "whatsapp":
        contact_name = input("Enter the contact name: ")
        ipo_data_sender.send_via_whatsapp(contact_name)
    elif send_method == "email":
        from_email_address = input("Enter your email address: ").encode('ascii', 'ignore').decode('ascii')
        app_password = input(
            f"Enter your 16 character app password created for the {from_email_address}: "
        ).encode('ascii', 'ignore').decode('ascii')

        print(app_password)
        to_email_address = input("Enter the recipient's email address: ")
        ipo_data_sender.send_via_email(
            from_email_address, app_password, to_email_address
        )
    else:
        print("Invalid method entered. Please enter either 'whatsapp' or 'email'.")


if __name__ == "__main__":
    main()
