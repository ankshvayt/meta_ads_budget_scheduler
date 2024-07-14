# Facebook Ad Budget Adjuster

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Schedule Configuration](#schedule-configuration)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Facebook Ad Budget Adjuster is an automated tool that adjusts Facebook ad budgets at specified times. It's designed to help marketers efficiently manage their ad spend by automatically reducing budgets on Friday evenings and restoring them on Sunday mornings.

## Features
- Automated budget adjustments for Facebook ad campaigns and ad sets
- Scheduled execution via GitHub Actions
- Email notifications for budget changes
- Flexible configuration through environment variables

## Installation
To use this package in your project:
```bash
pip install git+https://github.com/ankshvayt/meta_ads_budget_scheduler.git
```

## Configuration

### Environment Variables
Set the following environment variables in your GitHub repository secrets:

#### Facebook API Credentials
- `FB_APP_ID`: Your Facebook App ID
- `FB_APP_SECRET`: Your Facebook App Secret
- `FB_ACCESS_TOKEN`: Your Facebook Access Token
- `AD_ACCOUNT_ID`: Your Facebook Ad Account ID

#### Email Configuration
- `SMTP_SERVER`: SMTP server for sending emails
- `SMTP_PORT`: SMTP port
- `SMTP_USERNAME`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `FROM_EMAIL`: Email address to send notifications from
- `TO_EMAIL`: Email address to send notifications to

### Schedule Configuration
The schedule is configured using cron syntax in GitHub Actions:

1. Go to your GitHub repository settings.
2. Navigate to "Secrets and variables" > "Actions".
3. Add two new repository secrets:
   - `MORNING_SCHEDULE`: Cron expression for morning run
   - `EVENING_SCHEDULE`: Cron expression for evening run

Example cron expressions:
- `30 3 * * *`: Runs at 3:30 AM UTC daily
- `30 13 * * *`: Runs at 1:30 PM UTC daily

Note: GitHub Actions uses UTC time. Adjust your cron expressions accordingly.

## Usage
Once configured, the script will run automatically according to the schedule you've set. You can also manually trigger the workflow from the "Actions" tab in your GitHub repository.

To use the package in your own Python scripts:
```python
from fb_ad_budget_adjuster import check_and_adjust_budgets

check_and_adjust_budgets()
```
Ensure all necessary environment variables are set before running.

## Development
To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/ankshvayt/meta_ads_budget_scheduler.git
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with the necessary environment variables for local testing.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.