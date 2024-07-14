import os
import json
import pytz
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.exceptions import FacebookRequestError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration
with open('config.json', 'r') as config_file:
    BUDGET_CONFIG = json.load(config_file)

# Facebook API Credentials
FB_APP_ID = os.environ.get('FB_APP_ID')
FB_APP_SECRET = os.environ.get('FB_APP_SECRET')
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')

# Initialize the Facebook Ads API
FacebookAdsApi.init(FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN)

AD_ACCOUNT_ID = os.environ.get('AD_ACCOUNT_ID')
if not AD_ACCOUNT_ID:
    raise ValueError("AD_ACCOUNT_ID environment variable is not set")

def adjust_budget(item_id, is_campaign, new_budget):
    try:
        if is_campaign:
            item = Campaign(item_id)
            item_type = 'Campaign'
        else:
            item = AdSet(item_id)
            item_type = 'Ad Set'
        
        item.api_get(fields=['name', 'daily_budget', 'lifetime_budget'])
        name = item['name']
        daily_budget = float(item.get('daily_budget', 0))
        lifetime_budget = float(item.get('lifetime_budget', 0))
        
        if daily_budget > 0:
            budget_field = 'daily_budget'
            old_budget = daily_budget
        elif lifetime_budget > 0:
            budget_field = 'lifetime_budget'
            old_budget = lifetime_budget
        else:
            return f"{item_type} {item_id} ({name}): No budget found to update."
        
        # Update the budget
        params = {
            budget_field: int(new_budget)
        }
        item.api_update(params=params)
        
        # Verify the update
        item.api_get(fields=[budget_field])
        updated_budget = float(item[budget_field])
        
        return f"{item_type} {item_id} ({name}):\nBudget adjusted from {old_budget/100:.2f} AUD to {updated_budget/100:.2f} AUD"
    except FacebookRequestError as e:
        return f"Error updating {item_type.lower()} {item_id}: Facebook API error - {e.api_error_message()}"
    except Exception as e:
        return f"Error updating {item_type.lower()} {item_id}: {type(e).__name__} - {str(e)}"

def check_and_adjust_budgets():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    if now.weekday() == 4 and now.hour == 19:  # Friday 7 PM
        print("It's Friday evening. Reducing budgets...")
        results = adjust_budgets('reduced')
        send_email("Facebook Ad Budgets Reduced", "\n".join(results))
    elif now.weekday() == 6 and now.hour == 9:  # Sunday 9 AM
        print("It's Sunday morning. Restoring normal budgets...")
        results = adjust_budgets('normal')
        send_email("Facebook Ad Budgets Restored", "\n".join(results))
    else:
        print("It's not time to adjust budgets.")

def adjust_budgets(budget_type):
    results = []
    for item_type in ['campaigns', 'ad_sets']:
        for item_id, budgets in BUDGET_CONFIG[item_type].items():
            result = adjust_budget(item_id, item_type == 'campaigns', budgets[budget_type])
            results.append(result)
            print(result)
    return results
        
def send_email(subject, body):
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    from_email = os.environ.get('FROM_EMAIL')
    to_email = os.environ.get('TO_EMAIL')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    check_and_adjust_budgets()