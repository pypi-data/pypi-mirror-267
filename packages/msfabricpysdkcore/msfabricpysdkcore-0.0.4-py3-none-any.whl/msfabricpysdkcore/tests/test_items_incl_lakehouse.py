import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()
        self.workspace_id = "c3352d34-0b54-40f0-b204-cc964b1beb8d"

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.item_name = "testitem" + datetime_str
        self.item_type = "Notebook"
    
    def test_item_end_to_end(self):

        item = self.fc.create_item(display_name=self.item_name, type=self.item_type, workspace_id=self.workspace_id) 
        self.assertEqual(item.display_name, self.item_name)
        self.assertEqual(item.type, self.item_type)
        self.assertEqual(item.workspace_id, self.workspace_id)
        self.assertEqual(item.description, "")

        item = self.fc.get_item(workspace_id=self.workspace_id, item_id=item.id)
        item_ = self.fc.get_item(workspace_id=self.workspace_id,
                                  item_name=self.item_name, item_type=self.item_type)
        self.assertEqual(item.id, item_.id)
        self.assertEqual(item.display_name, self.item_name)
        self.assertEqual(item.type, self.item_type)
        self.assertEqual(item.workspace_id, self.workspace_id)
        self.assertEqual(item.description, "")

        item_list = self.fc.list_items(workspace_id=self.workspace_id)
        self.assertTrue(len(item_list) > 0)

        item_ids = [item_.id for item_ in item_list]
        self.assertIn(item.id, item_ids)

        self.fc.update_item(workspace_id=self.workspace_id, item_id=item.id, display_name=f"u{self.item_name}")
        item = self.fc.get_item(workspace_id=self.workspace_id, item_id=item.id)
        self.assertEqual(item.display_name, f"u{self.item_name}")

        status_code = self.fc.delete_item(workspace_id=self.workspace_id, item_id=item.id)

        self.assertAlmostEqual(status_code, 200)

    def test_lakehouse(self):

        lakehouse = self.fc.get_item(workspace_id=self.workspace_id, item_name="lakehouse1", item_type="Lakehouse")
        item_id = lakehouse.id
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        table_name = f"table{date_str}"


        status_code = self.fc.load_table(workspace_id=self.workspace_id, item_id=item_id, table_name=table_name, 
                                         path_type="File", relative_path="Files/folder1/titanic.csv")

        self.assertEqual(status_code, 202)

        table_list = self.fc.list_tables(workspace_id=self.workspace_id, item_id=item_id)
        table_names = [table["name"] for table in table_list]

        self.assertIn(table_name, table_names)

if __name__ == "__main__":
    unittest.main()