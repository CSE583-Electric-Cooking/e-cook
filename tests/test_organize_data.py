import unittest
import pandas as pd
import os
import io
from unittest import mock

class TestDeaggregate(unittest.TestCase):
    """
    Smoke tests for the Kosko functions.
    """
    def test_deaggregate_smoke(self):
        """
        Smoke test for the deaggregate function.
        Checks if the deaggregate function correctly processes actual CSV files and creates a dictionary.
        """
        # Assuming you have actual CSV files with content for testing
        test_csv_data = {
            "user_1_data.csv": "column1,column2\n1,2\n3,4",
            "user_2_data.csv": "column1,column2\n5,6\n7,8"
        }

        # Create temporary CSV files for testing
        for filename, content in test_csv_data.items():
            with open(filename, 'w') as file:
                file.write(content)

        try:
            # Run the deaggregate function on the test CSV files
            data_files = list(test_csv_data.keys())
            user_data = deaggregate(data_files)

            # Check if the resulting dictionary contains the expected data
            self.assertTrue("1" in user_data)
            self.assertTrue("2" in user_data)
            self.assertEqual(user_data["1"], pd.DataFrame({"column1": [1, 3], "column2": [2, 4]}))
            self.assertEqual(user_data["2"], pd.DataFrame({"column1": [5, 7], "column2": [6, 8]}))

        finally:
            # Clean up: Remove the temporary CSV files
            for filename in test_csv_data.keys():
                os.remove(filename)

    def test_deaggregate_one_shot(self):
        """
        One-shot test for the deaggregate function.
        Checks if the deaggregate function handles an empty list gracefully.
        """
        data_files = []
        user_data = deaggregate(data_files)
        self.assertEqual(user_data, {})

    def test_deaggregate_edge(self):
        """
        Edge test for the deaggregate function.
        Checks if the deaggregate function handles a large number of data files.
        """
        # Assuming you have actual CSV files with content for testing
        num_files = 1000
        test_csv_data = {f"user_{i}_data.csv": f"column1,column2\n{i},{i + 1}" for i in range(1, num_files + 1)}

        # Create temporary CSV files for testing
        for filename, content in test_csv_data.items():
            with open(filename, 'w') as file:
                file.write(content)

        try:
            # Run the deaggregate function on the large number of test CSV files
            data_files = list(test_csv_data.keys())
            user_data = deaggregate(data_files)

            # Check if the resulting dictionary contains the expected number of entries
            self.assertEqual(len(user_data), num_files)

        finally:
            # Clean up: Remove the temporary CSV files
            for filename in test_csv_data.keys():
                os.remove(filename)

class TestQuery(unittest.TestCase):
    """
    Unit tests for the query function.
    """
    def test_query_smoke(self):
        """
        Smoke test for the query function.

        Checks if the query function prints user IDs for a given dictionary.
        """
        test_dict = {"1": pd.DataFrame({"column1": [1, 2], "column2": [3, 4]}),
                     "2": pd.DataFrame({"column1": [5, 6], "column2": [7, 8]})}
        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            query(test_dict)
            output = mock_stdout.getvalue().strip()
            self.assertIn("USER ID: 1", output)  # Check if "USER ID: 1" is in the printed output
            self.assertIn("USER ID: 2", output)  # Check if "USER ID: 2" is in the printed output

    def test_query_one_shot(self):
        """
        One-shot test for the query function.

        Checks if the query function handles an empty dictionary gracefully.
        """
        test_dict = {}
        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            query(test_dict)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")  # Check if the output is empty

    def test_query_edge(self):
        """
        Edge test for the query function.

        Checks if the query function handles a dictionary with a large number of entries.
        """
        # Assuming you have a large dictionary with unique user IDs
        num_entries = 1000
        test_dict = {str(i): pd.DataFrame({"column1": [i], "column2": [i + 1]}) for i in range(1, num_entries + 1)}

        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            query(test_dict)
            output = mock_stdout.getvalue().strip()
            # Check if the output contains a specific user ID from the large dictionary
            self.assertGreaterEqual(output.count("USER ID:"), 1)

if __name__ == '__main__':
    unittest.main()
