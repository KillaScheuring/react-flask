import unittest
import time
from . import data_manipulation as dm
import random
import json


class MyTestCase(unittest.TestCase):
    # Please note that these tests do not currently pass.
    # For api.py to use the functions in data_manipulation.py,
    # the path to the json files needs to be '../json' rather than '.json/'
    # Tests work when the path is '.json/'
    def test_create_ticket_simple(self):
        """
        Test if the new ticket is entered into the JSON correctly
        """
        # Test Data
        ticket_id = "0"
        ticket_type_id = 0
        ticket_description = "New ticket test"
        ticket_opened_by_id = 11111
        ticket_due_date = time.time() + 60 * 60 * 24 * 60

        #  Get current number of tickets to compare later
        with open(dm.tickets_file_location) as file:
            number_of_tickets = len(json.load(file).keys())

        # Create a ticket with set data
        dm.create_ticket(ticket_id, ticket_type_id,
                         ticket_description, ticket_opened_by_id,
                         ticket_due_date)

        # Get updated data
        with open(dm.tickets_file_location) as file:
            tickets = json.load(file)

            # number of tickets
            self.assertEqual(len(tickets.keys()), number_of_tickets + 1, "Number of tickets should increase by 1")

            # type
            self.assertEqual(tickets[ticket_id]["type"], ticket_type_id, "The types should be the one entered")
            # description
            self.assertEqual(tickets[ticket_id]["description"], ticket_description,
                             "The descriptions should be the one entered")
            # opened_by
            self.assertEqual(tickets[ticket_id]["opened_by"], ticket_opened_by_id,
                             "The opened_by user id should be the one given")
            # due_date
            self.assertEqual(tickets[ticket_id]["due_date"], ticket_due_date, "The due_date should be the one given")

            # updated_by
            self.assertEqual(tickets[ticket_id]["updated_by"], tickets[ticket_id]["opened_by"],
                             "The updated_by id should be the same as the opener")

            # updated_at and opened_at
            self.assertEqual(tickets[ticket_id]["opened_at"], tickets[ticket_id]["updated_at"],
                             "The opened_at and updated_at should be the same")

    def test_update_ticket_simple(self):
        """
        Test if the ticket is updated correctly
        """
        # set consistent id to set and look up changes
        ticket_id = "5"

        # Test data to change ticket
        ticket_type_id = 2
        ticket_updated_by_id = 22222
        ticket_description = "Update ticket test"
        ticket_due_date = time.time() + 60 * 60 * 24 * 90

        # Create ticket to update
        dm.create_ticket(ticket_id, "1", "New ticket for updating", 11111, time.time() + 60 * 60 * 24 * 10)

        # Get original data to compare later
        with open(dm.tickets_file_location) as file:
            tickets = json.load(file)
            number_of_tickets = len(tickets.keys())
            old_version = tickets[ticket_id]

        # Update ticket
        dm.update_ticket(ticket_id,
                         {
                             "ticket_updated_by_id": ticket_updated_by_id,
                             "ticket_description": ticket_description,
                             "ticket_due_date": ticket_due_date,
                             "ticket_type": ticket_type_id
                         })

        # Get new data and test it
        with open(dm.tickets_file_location, 'r') as file:
            tickets = json.load(file)
            updated_version = tickets[ticket_id]

            # Not Modified in update
            # number of tickets
            self.assertEqual(len(tickets.keys()), number_of_tickets, "Number of tickets should not have changed")
            # opened_by
            self.assertEqual(updated_version["opened_by"], old_version["opened_by"],
                             "The opened_by id should not have changed")
            # opened_at
            self.assertEqual(updated_version["opened_at"], old_version["opened_at"],
                             "The opened_at time should not have changed")

            # Modified with update function parameters
            # type
            self.assertEqual(updated_version["type"], ticket_type_id, "The type should have updated to what was given")
            # description
            self.assertEqual(updated_version["description"], ticket_description,
                             "The description should have been updated to what was given")
            # due_date
            self.assertEqual(updated_version["due_date"], ticket_due_date,
                             "The due_date should have been updated to what was given")
            # updated_by
            self.assertEqual(updated_version["updated_by"], ticket_updated_by_id,
                             "The updated_by should have been updated to what was given")

            # Modified by function automatically
            # updated_at
            self.assertNotEqual(updated_version["updated_at"], old_version["updated_at"],
                                "The updated_at should have been updated")

    def test_delete_ticket_simple(self):
        """
        test if the ticket is removed correctly
        """

        ticket_id = "0"

        with open(dm.tickets_file_location) as file:
            ticket_before_removal = json.load(file).get(ticket_id, None)

        dm.delete_ticket(ticket_id)

        with open(dm.tickets_file_location) as file:
            ticket_after_removal = json.load(file).get(ticket_id, None)

        self.assert_(ticket_before_removal and not ticket_after_removal,
                     "The ticket was in the tickets and it was removed")


if __name__ == '__main__':
    unittest.main()
