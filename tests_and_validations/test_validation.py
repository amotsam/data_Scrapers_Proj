import unittest
import pandas as pd
from unittest.mock import patch
from src.main import validate_data

class TestValidation(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_validate_data_success(self, mock_read_csv):
        # Mock data for testing
        mock_data = pd.DataFrame({
            "column1": [1, 2, 3],
            "column2": ["a", "b", "c"]
        })
        mock_read_csv.return_value = mock_data

        validation_rules = {
            "required_columns": ["column1", "column2"],
            "non_empty_columns": ["column1"]
        }

        result = validate_data("fake_file_path.csv", validation_rules)
        self.assertTrue(result)

    @patch("pandas.read_csv")
    def test_validate_data_missing_column(self, mock_read_csv):
        # Mock data missing a required column
        mock_data = pd.DataFrame({
            "column1": [1, 2, 3]
        })
        mock_read_csv.return_value = mock_data

        validation_rules = {
            "required_columns": ["column1", "column2"],
            "non_empty_columns": ["column1"]
        }

        result = validate_data("fake_file_path.csv", validation_rules)
        self.assertFalse(result)

    @patch("pandas.read_csv")
    def test_validate_data_empty_values(self, mock_read_csv):
        # Mock data with empty values
        mock_data = pd.DataFrame({
            "column1": [1, 2, None],
            "column2": ["a", "b", "c"]
        })
        mock_read_csv.return_value = mock_data

        validation_rules = {
            "required_columns": ["column1", "column2"],
            "non_empty_columns": ["column1"]
        }

        result = validate_data("fake_file_path.csv", validation_rules)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
