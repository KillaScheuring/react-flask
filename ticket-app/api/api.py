from flask import Flask, request
from data_manipulation import update_ticket
from data_manipulation import delete_ticket
from data_manipulation import create_ticket
import json

app = Flask(__name__)


@app.route('/create', methods=['POST'])
def create_new_ticket():
    """
    This processes the user's request to create a ticket
    """
    # Retrieve data from the react page
    new_ticket = request.get_json()

    print("creating", new_ticket['ticket_id'], "...")

    # Create the ticket
    create_ticket(new_ticket['ticket_id'], new_ticket['ticket_type'],
                  new_ticket['ticket_description'], new_ticket['ticket_opened_by'],
                  new_ticket['ticket_due_date'])
    return 'Created'


@app.route('/remove', methods=['POST'])
def remove_ticket():
    """
    This processes the user's request to remove a ticket
    """
    # Retrieve ticket information
    ticket_delete_data = request.get_json()

    print("Deleting", ticket_delete_data["ticket_id"], "...")

    # Remove ticket
    delete_ticket(ticket_delete_data["ticket_id"])
    return 'Removed'


@app.route('/update', methods=['POST'])
def process_update_ticket():
    """
    This processes the user's request to update a ticket
    """
    # Retrieve ticket information and updated data
    ticket_update_data = request.get_json()

    print("Updating", ticket_update_data["ticket_id"], "...")

    update_ticket(ticket_update_data["ticket_id"],
                  {
                      ticket_update_data["attribute_label"]: ticket_update_data["attribute_value"]
                  })
    return 'Updated'


@app.route('/tickets')
def view_tickets():
    """
    This is where React gets the ticket data
    :return: tickets to the react page
    """

    # Retrieve the ticket, type, and user data from the JSONs
    with open('../json/tickets.json', 'r') as f:
        tickets_raw = json.load(f)
    with open('../json/ticket_types.json', 'r') as f:
        ticket_types_raw = json.load(f)
    with open('../json/users.json', 'r') as f:
        users_raw = json.load(f)

    return {"tickets": tickets_raw, "types": ticket_types_raw, "users": users_raw}


if __name__ == '__main__':
    app.run(host="localhost")
