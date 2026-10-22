## AWS Real-Time Monitoring & Alerting System
This project demonstrates how to build a real-time monitoring, alerting, and automated response system in AWS. The architecture leverages CloudTrail, CloudWatch, EventBridge, Lambda, SNS, S3, and KMS to detect unauthorized API calls and take immediate action.


## Architecture Overview
![](/aws-enterprise-alert-monitoring-system/images/architecture.gif)

The above solution is designed to:
- Capture all API activity in the AWS environment.
- Detect unauthorized or suspicious API calls.
- Trigger real-time alerts to administrators and security teams.
- Automate incident response actions with Lambda.
- Store audit logs securely in encrypted S3.

## **Use Case Scenarios of This Project for Organizations**
1. **Security Monitoring**
Organizations can monitor unauthorized API calls (e.g., UnauthorizedOperation) in real-time and take immediate action.
Example: If an unauthorized user tries to describe or modify EC2 instances, an alert is sent to the security team.

2. **Compliance and Audit Readiness**
Logs stored in an encrypted S3 bucket help meet compliance standards like SOC 2, HIPAA, or GDPR.
Example: Auditors request logs for API activity over the last 6 months. With this setup, these logs are securely available.

3. **Incident Response**
Automatically alert security teams about suspicious activity to reduce response time.
Example: If root account credentials are used unexpectedly, an immediate notification can help mitigate potential risks.

4. **Cost Optimization**
Monitor actions that could lead to unexpected billing issues.
Example: Detect if an unauthorized user attempts to create costly resources (e.g., high-end EC2 instances).



## **Setup Instructions**

### **1. Prerequisites**
- AWS account.
- IAM user/role with permissions to manage CloudTrail, SNS, Lambda, and S3.

---

### **2. Steps to Set Up**

1. **Create an S3 Bucket**
   - Enable versioning and default encryption (KMS).
   - Use this bucket for storing CloudTrail logs.

2. **Set Up IAM Role**
   - Creat an IAM Role that Cloudtrail needs to act on the cloudwatch log group:
     - For this demo we will use AWS managed policies:
     - AmazonS3FullAccess, AWS CloudTrail_FullAccess, AWSKeyManagementServicePowerUser, CloudWatchFullAccess.
     - A custom managed policy for cloudtrail PutLogEven and CreateLogStream

3. **Set Up CloudTrail**
   - Enable CloudTrail and configure:
     - S3 bucket for log storage.
     - SNS topic for event notifications.

4. **Create an SNS Topic**
   - Name: `cloudtrail-alerts-demo`.
   - Add an email or phone number as a subscriber.

5. **Deploy the Lambda Function**
   - Add the code in `lambda/lambda_handler.py`.
   - Set environment variables:
     - `SNS_TOPIC_ARN`: ARN of the SNS topic.
   - Attach the necessary IAM role.

6. **Test the Setup**
   - Use the test event in `scripts/test-events.json`.
   - Simulate an unauthorized action:
     ```bash
     aws ec2 describe-instances --profile unauthorized-user
     ```

---
# Deploy Using the AWS CloudFormation Template (Optional)

This guide provides step-by-step instructions for deploying the CloudFormation Template (CFT) to set up resources for the AWS CloudTrail Real-Time Monitoring and Alerting Demo.

## Prerequisites

Before deploying the CFT, ensure you have the following:
- **AWS Account**: Access to a valid AWS account.
- **IAM Permissions**: Ensure you have permissions to create:
  - S3 buckets and policies
  - CloudTrail trails
  - IAM roles and policies
  - Lambda functions
  - CloudWatch log groups
  - SNS topics and subscriptions
  - KMS keys
- **AWS CLI/Console**: Use either the AWS Management Console or the AWS CLI to deploy the stack.
- **Template File**: The CloudFormation template file (`cloudtrail-demo.yml`).
- **Parameters**:
  - **AccountId**: Your AWS account ID.
  - **Region**: Your preferred AWS region (e.g., `us-east-1`).
  - **EmailSubscription**: An email address to receive SNS notifications.

---

## Deployment Steps

### 1. Save the CloudFormation Template
Save the provided YAML file as `cloudtrail-demo.yml`.

---

### 2. Deploy the Template Using the AWS Console

1. **Navigate to the AWS CloudFormation Console**:
   - [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/)

2. **Create a New Stack**:
   - Choose **Stacks** > **Create Stack** > **With new resources (standard)**.

3. **Upload the Template File**:
   - Select **Upload a template file**.
   - Choose the `cloudtrail-demo.yml` file from your system.

4. **Specify Stack Parameters**:
   - **AccountId**: Enter your AWS Account ID.
   - **Region**: Specify your desired AWS Region.
   - **EmailSubscription**: Enter your email address to receive SNS alerts.

5. **Proceed with the Configuration**:
   - Click **Next**, optionally configure stack options, and proceed to the next step.

6. **Review and Create the Stack**:
   - Review the stack settings and click **Create Stack** to begin the deployment.

---

### 3. Confirm the SNS Subscription
Once the stack is deployed:
- Check your email inbox for a subscription confirmation email from AWS SNS.
- Click the **Confirm subscription** link to enable notifications.

---

### 4. Verify Deployment

After deploying the stack, validate that resources are created and functioning as expected:
1. **CloudTrail Logs**:
   - Verify that the S3 bucket contains CloudTrail logs.
   - Check the CloudWatch log group (`aws-cloudtrail-logs-<AccountId>-demo`) for events.
2. **SNS Notifications**:
   - Confirm that you receive email alerts for unauthorized actions.


3. **Lambda Function**:
   - Check the AWS Lambda console to confirm the function `process-cloudtrail-logs` was deployed successfully.

---

## 
Cleanup

To avoid incurring charges, delete the stack after completing your work:
1. Navigate to the **CloudFormation Console**.
2. Select the deployed stack and click **Delete**.
3. Confirm the deletion.

---

## Troubleshooting

1. **Email Not Received**:
   - Check your spam/junk folder.
   - Verify the email address you provided in the `EmailSubscription` parameter.

2. **Stack Deployment Errors**:
   - Ensure you have the necessary IAM permissions to create all required resources.
   - Review the **Events** tab in the CloudFormation Console for error messages.

3. **SNS Notifications Not Triggered**:
   - Confirm CloudTrail's integration with CloudWatch and SNS.
   - Check the CloudWatch log group for Lambda function execution errors.

---

## Resources

- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

---

## **Files in the Directory**

- **lambda/lambda_handler.py**: Lambda function code for processing CloudTrail events.
- **scripts/test-events.json**: Test payload for simulating an SNS event.
- **README.md**: Documentation for the demo setup.
- **templates/cloudtrail-enhanced-demo.yaml** (Optional): CloudFormation template for automating setup.

