
import time
import json
from pprint import pprint as pp

# placed into variables for easy use
tickets_file_location = '../json/tickets.json'
ticket_types_file_location = '../json/ticket_types.json'
users_file_location = '../json/users.json'


def create_ticket(ticket_id, ticket_type_id, ticket_description, ticket_opened_by_id, ticket_due_date):
    """
    Function to create a ticket and add to persistent json file
    :param ticket_id: str
    :param ticket_type_id: int
    :param ticket_description: text
    :param ticket_opened_by_id: int
    :param ticket_due_date: time
    """

    # Get current data to update it
    with open(tickets_file_location, 'r') as f:
        tickets = json.load(f)

    # Place all information for new ticket into a dictionary to easily add it to the ticket dictionary
    new_ticket = {
        "type": int(ticket_type_id),
        "description": ticket_description,
        "opened_by": int(ticket_opened_by_id),
        "opened_at": time.time(),
        "updated_at": time.time(),
        "due_date": ticket_due_date,
        "updated_by": int(ticket_opened_by_id)
    }

    # Add the new ticket using it's ID as the key
    tickets.setdefault(ticket_id, new_ticket)

    # Rewrite the persistent JSON file
    with open(tickets_file_location, 'w') as f:
        f.write(json.dumps(tickets))

    return 0


def update_ticket(ticket_id, new_data):
    """
    Requires the ticket_id will update given attribute(s) of the ticket
    :param ticket_id: str
    :param new_data: various possible attributes
    """

    print("updating", ticket_id, "...")

    # Check to see which attribute is being updated
    ticket_type_id = new_data.get('ticket_type', None)
    ticket_description = new_data.get('ticket_description', None)
    ticket_updated_by_id = new_data.get('ticket_updated_by', None)
    ticket_due_date = new_data.get('ticket_due_date', None)

    # Retrieve the ticket data from JSON
    with open(tickets_file_location, 'r') as f:
        tickets = json.load(f)

    # If so, update the data
    if ticket_type_id:
        tickets[ticket_id]["type"] = int(ticket_type_id)
    if ticket_updated_by_id:
        tickets[ticket_id]["updated_by"] = int(ticket_updated_by_id)
    if ticket_description:
        tickets[ticket_id]["description"] = ticket_description
    if ticket_due_date:
        tickets[ticket_id]["due_date"] = ticket_due_date

    # Set updated_at to current time
    tickets[ticket_id]["updated_at"] = time.time()

    # Rewrite the JSON
    with open(tickets_file_location, 'w') as f:
        f.write(json.dumps(tickets))


def delete_ticket(ticket_id):
    """
    Deletes ticket with given id
    :param ticket_id: str
    """
    # Get ticket information from JSON
    with open(tickets_file_location, 'r') as f:
        tickets = json.load(f)

    # Remove the ticket with the matching id
    del tickets[ticket_id]

    # Rewrite JSON
    with open(tickets_file_location, 'w') as f:
        f.write(json.dumps(tickets))
