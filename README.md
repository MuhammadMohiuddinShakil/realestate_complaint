# Installation Instructions for Odoo Module

## Steps:

1. **Download the Module:**
    - Clone or download the module's repository from its source on Git.

2. **Add Module to Odoo Directory:**
    - Extract the downloaded module if it's in a compressed format (e.g., zip).
    - Move the extracted module directory to the addons/custom addons directory of your Odoo instance.

3. **Access Odoo Instance:**
    - Log in to your Odoo instance using your credentials.

4. **Activate Developer Mode:**
    - Go to the settings menu by clicking on your username.
    - Enable 'Developer Mode' from the dropdown menu.

5. **Update Module List:**
    - Go to the Apps menu.
    - Click on the 'Update Apps List' button.

6. **Install Module:**
    - Now, go to the Apps menu again, then click on 'Apps'.
    - Search for the newly added module in the Apps list.
    - Click on the module to install it.

## Configure Outgoing Mail Servers:

- To ensure proper functionality of the module, it's essential to configure the outgoing mail server in Odoo and enable
  debug mode. Follow these steps:

7. **Access Odoo Settings:**
    - Log in to your Odoo instance using your administrator credentials.
    - Navigate to the Settings menu.

8. **Configure Outgoing Mail Server:**
    - In the Settings menu, locate and click on the "Technical" section.
    - Under the Technical settings, find and select "Outgoing Mail Servers."

9. **Add New Outgoing Mail Server:**
    - Click on the "Create" button to add a new outgoing mail server.
    - Fill in the required fields such as Server Name, SMTP Server, Port, and Email Address.
    - Ensure that the authentication details (if required) are correctly provided.

10. **Test Connection:**
    - Click on the "Test Connection" button or send a test email to verify the configuration.

11. **Save Configuration:**
    - Once the configuration is verified, click on the "Save" button to save the outgoing mail server settings.
