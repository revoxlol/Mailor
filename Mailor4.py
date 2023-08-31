import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
import time
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

class EmailAutomationApp(tk.Tk):
    
    
    def __init__(self):
        super().__init__()
        self.title("Mailor")
        self.geometry("350x375")
        
        # Create labels and entry fields for email details
        tk.Label(self, text="SendGrid API Key:").pack()
        self.api_key_entry = tk.Entry(self, show='*', width=55)
        self.api_key_entry.pack()
        
         # Create a toggle button to show/hide API Key
        self.toggle_api_key_button = tk.Button(self, text="Show Key", command=self.toggle_api_key)
        self.toggle_api_key_button.pack()
        self.api_key_visible = False  # Flag to track visibility
        
        tk.Label(self, text="Sender's Email:").pack()
        self.sender_email_entry = tk.Entry(self,width=40)
        self.sender_email_entry.pack()
        
         # Create a button to select the recipient CSV file
        tk.Button(self, text="Select Recipients CSV", command=self.select_recipient_csv, bg="light blue", fg="black").pack(anchor="nw",padx=10, pady=(10, 2))
        
        tk.Button(self, text="Attach Resume", command=self.attach_file, bg="light blue", fg="black").pack(anchor="nw",padx=10)
        # Initialize attachment file path
        self.attachment_path = ""
        
       
        
        tk.Label(self, text="Subject:").pack()
        self.subject_entry = tk.Entry(self, width=40)
        self.subject_entry.pack()
        
        tk.Label(self, text="Email Body:").pack()
        self.body_text = tk.Text(self, height=6)
        self.body_text.pack()
        

        # Create a button to start sending emails
        tk.Button(self, text="Start Sending", command=self.send_emails, bg="light blue", fg="black").pack(pady="5")
        

        # Initialize recipient CSV file path
        self.recipient_csv = ""
        
    def toggle_api_key(self):
        if self.api_key_visible:
            self.api_key_entry.config(show='*')
            self.toggle_api_key_button.config(text="Show Key")
        else:
            self.api_key_entry.config(show='')
            self.toggle_api_key_button.config(text="Hide Key")
        
        self.api_key_visible = not self.api_key_visible    
    def attach_file(self):
        # Open a file dialog to select a file to attach
        self.attachment_path = filedialog.askopenfilename()    
    
    def select_recipient_csv(self):
        # Open a file dialog to select the recipient CSV file
        self.recipient_csv = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),))
    attachment_path = "C:/Users/Revox/Resume.pdf"
    def send_email(self, api_key, sender_email, recipient_email, recipient_name, subject, body, attachment_path):
        # Create a personalized email message
        personalized_subject = subject.replace("[Name]", recipient_name)
        personalized_body = body.replace("[Name]", recipient_name)
        
        message = Mail(
            from_email=sender_email,
            to_emails=recipient_email,
            subject=personalized_subject,
            plain_text_content=personalized_body
        )
        if attachment_path:
         with open(attachment_path, "rb") as attachment_file:
            attachment_data = attachment_file.read()
            attachment = Attachment()
            attachment.file_content = base64.b64encode(attachment_data).decode()
            attachment.file_type = "application/pdf"  # Adjust the file type accordingly
            attachment.file_name = os.path.basename(attachment_path)
            attachment.disposition = "attachment"
            message.attachment = attachment
        
        message.attachment = attachment
        

        try:
            # Send the email using the SendGrid API client
            sg = SendGridAPIClient(api_key=api_key)
            response = sg.send(message)
            return response.status_code
        except Exception as e:
            return str(e)
    
    def send_emails(self):
      
        # Get email details from the GUI
        api_key = self.api_key_entry.get()
        sender_email = self.sender_email_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END)
        
    
        api_key
        if not api_key or not sender_email or not subject or not body or not self.recipient_csv:
            messagebox.showerror("Error", "Please provide all the required details!")
            return
        
        # Read recipient details from the CSV file
        recipients = []
        
       
        with open(self.recipient_csv, "r") as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
             if len(row) >= 2:
                recipient_email = row[0]
                recipient_name = row[1]    
                recipients.append({"email": recipient_email, "name": recipient_name})
                
        
        # Send personalized emails to recipients
            for recipient in recipients:
                recipient_email = recipient["email"]
                recipient_name = recipient["name"]
            
                status_code = self.send_email(api_key, sender_email, recipient_email, recipient_name, subject, body, self.attachment_path)
                #Checking for errors in the terminal
                print(f"Email sent to {recipient_email} with response code: {status_code}")
                time.sleep(15)  # Delay for 15 seconds between each email
            
            
        messagebox.showinfo("Success", "Emails sent successfully!")
        
        #calling the reseting def
        
        self.reset_fields()
    
    #Reseting each parameters except the one you comment
    
    def reset_fields(self):
        #self.api_key_entry.delete(0, tk.END)
        # self.sender_email_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        #self.body_text.delete("1.0", tk.END)
        #self.recipient_csv = ""

if __name__ == "__main__":
    app = EmailAutomationApp()
    app.mainloop()
