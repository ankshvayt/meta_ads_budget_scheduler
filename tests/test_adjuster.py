import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pytz
from fb_ad_budget_adjuster.adjuster import check_and_adjust_budgets, adjust_budget

class TestFBAdBudgetAdjuster(unittest.TestCase):

    @patch('fb_ad_budget_adjuster.adjuster.datetime')
    @patch('fb_ad_budget_adjuster.adjuster.adjust_budgets')
    def test_check_and_adjust_budgets_friday(self, mock_adjust_budgets, mock_datetime):
        # Set up mock datetime to return Friday 7 PM
        mock_now = datetime(2023, 1, 6, 19, 0, tzinfo=pytz.timezone('Asia/Kolkata'))  # Friday 7 PM
        mock_datetime.now.return_value = mock_now

        check_and_adjust_budgets()
        mock_adjust_budgets.assert_called_once_with('reduced')

    @patch('fb_ad_budget_adjuster.adjuster.datetime')
    @patch('fb_ad_budget_adjuster.adjuster.adjust_budgets')
    def test_check_and_adjust_budgets_sunday(self, mock_adjust_budgets, mock_datetime):
        # Set up mock datetime to return Sunday 9 AM
        mock_now = datetime(2023, 1, 8, 9, 0, tzinfo=pytz.timezone('Asia/Kolkata'))  # Sunday 9 AM
        mock_datetime.now.return_value = mock_now

        check_and_adjust_budgets()
        mock_adjust_budgets.assert_called_once_with('normal')

    @patch('fb_ad_budget_adjuster.adjuster.datetime')
    @patch('fb_ad_budget_adjuster.adjuster.adjust_budgets')
    def test_check_and_adjust_budgets_other_time(self, mock_adjust_budgets, mock_datetime):
        # Set up mock datetime to return a time other than Friday 7 PM or Sunday 9 AM
        mock_now = datetime(2023, 1, 7, 12, 0, tzinfo=pytz.timezone('Asia/Kolkata'))  # Saturday 12 PM
        mock_datetime.now.return_value = mock_now

        check_and_adjust_budgets()
        mock_adjust_budgets.assert_not_called()

    @patch('fb_ad_budget_adjuster.adjuster.Campaign')
    def test_adjust_budget_campaign(self, mock_campaign):
        mock_campaign_instance = MagicMock()
        mock_campaign_instance.api_get.return_value = None
        mock_campaign_instance.__getitem__.return_value = 1000  # current budget
        mock_campaign.return_value = mock_campaign_instance

        result = adjust_budget('123', True, 2000)
        self.assertIn("Budget adjusted from 10.00 AUD to 20.00 AUD", result)

    @patch('fb_ad_budget_adjuster.adjuster.AdSet')
    def test_adjust_budget_adset(self, mock_adset):
        mock_adset_instance = MagicMock()
        mock_adset_instance.api_get.return_value = None
        mock_adset_instance.__getitem__.return_value = 1000  # current budget
        mock_adset.return_value = mock_adset_instance

        result = adjust_budget('456', False, 500)
        self.assertIn("Budget adjusted from 10.00 AUD to 5.00 AUD", result)

if __name__ == '__main__':
    unittest.main()