import React, {useState, useEffect} from 'react';
import EditableLabel from 'react-inline-editing';
import './App.css';

class TicketTextCell extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hover: false
        };

        this.handleMouseIn = this.handleMouseIn.bind(this);
        this.handleMouseOut = this.handleMouseOut.bind(this);

        this.trueValueStyle = {
            display: this.state.hover ? 'block' : 'none'
        };

        this.valueStyle = {
            display: this.state.hover ? 'none' : 'block'
        };
    }

    handleMouseIn() {
        this.setState({hover: true});
    }

    handleMouseOut() {
        this.setState({hover: false});
    }

    render() {
        // True value should only be visible when the mouse hovers over the cell
        this.trueValueStyle = {
            display: this.state.hover ? 'block' : 'none'
        };

        this.valueStyle = {
            display: this.state.hover ? 'none' : 'block'
        };
        return (
            <td className={this.props.className} onMouseEnter={this.handleMouseIn} onMouseLeave={this.handleMouseOut}>
                <div style={this.trueValueStyle}>{this.props.trueValue}</div>
                <div style={this.valueStyle}>{this.props.value}</div>
            </td>
        );
    }
}

class TicketTextEditableCell extends TicketTextCell {
    constructor(props) {
        super(props);
        /*
        Given time constraints I opted to make all the fields that could be edited only text box edits.
        Otherwise I would have used dropdown menus for the user_id fields and the type field and allow the user to
        select valid entries for those fields.
         */
        this._handleFocusOut = this._handleFocusOut.bind(this);
        this.trueValueStyle = {
            display: this.state.hover ? 'block' : 'none'
        };

        this.valueStyle = {
            display: this.state.hover ? 'none' : 'block'
        };
        this.state.mounted = false;
    }

    componentDidMount() {
        this.setState({mounted: true});
    }

    _handleFocusOut(text) {
        // Check if the component is mounted before processing fetch.
        if (this.state.mounted) {
            const requestOptions = {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    "ticket_id": this.props.ticket_id,
                    "attribute_label": `ticket_${this.props.attributeLabel}`,
                    "attribute_value": text
                })
            };
            fetch('/update', requestOptions)
                .then(response => response.json())
                .then(data => this.setState({postId: data.id}));
            window.location.reload(false);
        }
    }

    render() {
        // True value should only be visible when the mouse hovers over the cell
        this.trueValueStyle = {
            display: this.state.hover ? 'block' : 'none'
        };

        this.valueStyle = {
            display: this.state.hover ? 'none' : 'block'
        };

        return (
            <td className={this.props.className} onMouseEnter={this.handleMouseIn} onMouseLeave={this.handleMouseOut}>
                <div style={this.trueValueStyle}>
                    <EditableLabel
                        text={String(this.props.trueValue)}
                        onFocusOut={this._handleFocusOut}
                    />
                </div>
                <div style={this.valueStyle}>{this.props.value}</div>
            </td>
        );
    }


}

class TicketRow extends React.Component {
    constructor(props) {
        super(props);
        this.deleteTicket = this.deleteTicket.bind(this);

        // Keeps the cells in order
        let attributeNames = ["type", "description", "opened_by", "opened_at", "updated_at", "due_date", "updated_by"];

        // Filter for inline editablility
        let editable = ["type", "description", "due_date", "updated_by"];
        // Filters for formatting value
        let users_id = ["opened_by", "updated_by"];
        let dates = ["opened_at", "updated_at", "due_date"];

        let row = [];
        for (let attribute of attributeNames) {
            // Set default value for displayed value
            let value = 0;
            // Set default className (Only different when attribute is a datetime
            let className = "";
            // Check if there is a value for this attribute
            if (this.props.attributes[attribute]) {
                // Check if the attribute is a user_id and if it is in the users dictionary
                if (users_id.includes(attribute)) {
                    value = this.props.usernames[this.props.attributes[attribute]] ?
                        this.props.usernames[this.props.attributes[attribute]]["name"] :
                        "Unknown";
                } else if (dates.includes(attribute)) {
                    // Check if attribute is a datetime and set class name appropriately
                    value = String(new Date(this.props.attributes[attribute] * 1000));
                    className = "date";
                } else if (attribute === "type") {
                    // Check if the attribute is type and if it is in the type dictionary
                    value = this.props.types[this.props.attributes[attribute]] ?
                        this.props.types[this.props.attributes[attribute]]["description"] :
                        "Unknown";
                } else {
                    //Otherwise the value doesn't need to be formatted
                    value = this.props.attributes[attribute];
                }
            } else {
                // if the value is null replace with N/A
                value = "N/A";
            }
            if (editable.includes(attribute)) {
                row.push(<TicketTextEditableCell
                    className={className}
                    ticket_id={this.props.id}
                    trueValue={this.props.attributes[attribute] ? this.props.attributes[attribute] : value}
                    value={value}
                    attributeLabel={attribute}
                />);
            } else {
                row.push(<TicketTextCell
                    className={className}
                    trueValue={this.props.attributes[attribute]}
                    value={value}
                />);
            }
        }
        row.push(<td>
            <button onClick={this.deleteTicket}>Remove</button>
        </td>);
        this.content = <tr>
            {row}
        </tr>
    }

    deleteTicket() {
        // Check with the user to see if they are sure they want to delete this ticket
        if (window.confirm("Delete?")) {
            // send information to flask to delete ticket
            const requestOptions = {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    "ticket_id": this.props.id
                })
            };
            fetch('/remove', requestOptions)
                .then(response => response.json())
                .then(data => this.setState({postId: data.id}));
            // Reload page to show updated table
            window.location.reload(false);
        }
    }

    render() {
        // Render content
        return this.content
    }
}

class CreateTicket extends React.Component {
    constructor(props) {
        super(props);

        this.showForm = this.showForm.bind(this);
        this.creatNewTicket = this.creatNewTicket.bind(this);

        this.state = {
            form: false
        };

        // The form should be visible when the create button is clicked
        this.formStyle = {
            display: this.state.form ? 'block' : 'none'
        };

        // The create button should be visible when the form is hidden
        this.formOpenStyle = {
            display: this.state.form ? 'none' : 'block'
        };
    }

    showForm() {
        this.setState({form: true});
    }

    creatNewTicket() {
        // Place form data into an object to make it easier to sent to flask
        let formData = {
            ticket_id: document.getElementById("ticket_id").value,
            ticket_type: document.getElementById("ticket_type").value,
            ticket_description: document.getElementById("ticket_description").value,
            ticket_opened_by: document.getElementById("ticket_opened_by").value,
            ticket_due_date: document.getElementById("ticket_due_date").value
        }

        // Send request to flask with new ticket data
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        };
        fetch('/create', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({postId: data.id}));
        // Reload page to show updated table
        window.location.reload(false);
    }

    render() {
        this.formStyle = {
            display: this.state.form ? 'block' : 'none'
        };

        this.formOpenStyle = {
            display: this.state.form ? 'none' : 'block'
        };

        return (<div>
                <button style={this.formOpenStyle} onClick={this.showForm}>Create New Ticket</button>
                <form style={this.formStyle} onSubmit={this.creatNewTicket}>
                    <table>
                        <thead>
                        <th>ID (Unique)</th>
                        <th>Type (ID)</th>
                        <th>Description (String)</th>
                        <th>Opened By (ID)</th>
                        <th>Due Date (Unix Timestamp)</th>
                        </thead>
                        <tbody>
                        <td>
                            <input name='ticket_id' id='ticket_id' defaultValue={Math.floor(Math.random()*10000)}/>
                        </td>
                        <td>
                            <input name='ticket_type' id='ticket_type' defaultValue={2}/>
                        </td>
                        <td>
                            <input name='ticket_description' id='ticket_description' defaultValue='New ticket'/>
                        </td>
                        <td>
                            <input name='ticket_opened_by' id='ticket_opened_by' defaultValue={111111}/>
                        </td>
                        <td>
                            <input name='ticket_due_date' id='ticket_due_date' defaultValue={0}/>
                        </td>
                        </tbody>
                    </table>
                    <button type='submit'>Add</button>
                </form>
            </div>
        );
    }
}

function App() {

    const [currentTickets, setCurrentTickets] = useState([]);
    useEffect(() => {
        fetch('/tickets').then(res => res.json()).then(data => {
            let ticketRows = [];
            for (let ticketID of Object.keys(data["tickets"])) {
                ticketRows.push(<TicketRow
                    id={ticketID}
                    attributes={data["tickets"][ticketID]}
                    usernames={data["users"]}
                    types={data["types"]}
                />)
            }
            let ticketTable = <table id='all-tickets'>
                <thead>
                <tr>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Opened By</th>
                    <th>Opened At</th>
                    <th>Updated At</th>
                    <th>Due Date</th>
                    <th>Updated By</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {ticketRows}
                </tbody>
            </table>

            setCurrentTickets(ticketTable);
        });
    }, []);

    return (
        <div className="App">
            {currentTickets}
            <CreateTicket/>
        </div>
    );
}

export default App;
