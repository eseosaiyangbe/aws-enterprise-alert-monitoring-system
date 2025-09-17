# Workflow

1. **Unauthorized API Call**  
   - An unauthorized IAM user (e.g., `test-user`) tries to run a restricted command such as:  
     ```bash
     aws ec2 terminate-instances --instance-ids i-1234567890abcdef
     ```

2. **CloudTrail Logging**  
   - AWS CloudTrail records the API activity (who, when, where, and what).  
   - Logs are stored in an encrypted S3 bucket with KMS for secure retention.  

3. **CloudWatch Monitoring**  
   - CloudTrail delivers logs to CloudWatch Logs.  
   - Metric filters and alarms detect unusual activities (e.g., failed authentication, root account usage).  

4. **EventBridge Routing**  
   - When CloudWatch detects a violation, an event is forwarded to Amazon EventBridge.  
   - EventBridge routes the event to one or more targets for processing.  

5. **Lambda Remediation**  
   - The Lambda function parses the log entry, identifies it as suspicious, and publishes a message to SNS.  

6. **SNS Notifications**  
   - Amazon SNS broadcasts notifications (email, SMS, or webhook) to the security team and/or external systems.  

7. **Security Team Response**  
   - Administrators receive the alert in real-time and investigate.  
   - Automated Lambda actions provide first-line defense to reduce risks immediately.  

---

# Security & Compliance Features in This Project

- **KMS Encryption:** All CloudTrail logs are encrypted using AWS KMS before being stored.  
- **Least Privilege Roles:** IAM roles restrict access to only what each service needs.  
- **Real-Time Alerting:** EventBridge + SNS provide near-instant detection and notifications.  
- **Automated Remediation:** Lambda can execute predefined security responses without human delay.  

---

# Use Cases

- Detecting unauthorized API calls.  
- Meeting compliance requirements for audit logging.  
- Automating incident response to reduce Mean Time To Respond (MTTR).  
- Securing sensitive workloads against misuse or insider threats.  
- Monitor actions that could lead to unexpected billing issues.

---

# AWS Services Used

- **AWS CloudTrail** – Audit API calls.  
- **Amazon CloudWatch** – Monitor logs & metrics.  
- **Amazon EventBridge** – Event routing.  
- **AWS Lambda** – Automated remediation.  
- **Amazon SNS** – Notifications.  
- **Amazon S3 + KMS** – Secure log storage.  
- **IAM Roles** – Access control.  

---

# Notification Flow

- Admins can get alerts via SNS (Email/SMS/Webhooks).  
- Security systems can integrate with ticketing tools (e.g., Jira, ServiceNow) or SIEMs for deeper analysis.