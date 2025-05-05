import time
import hashlib
import json
import streamlit as st

# Blockchain list
blockchain = []

# Function to calculate SHA-256 hash of a block (excluding the hash field itself)
def calculate_hash(block):
    block_copy = block.copy()
    block_copy.pop("hash", None)  # Remove the 'hash' field to avoid circular reference
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Function to create a new block
def create_block(index, ticket_data, previous_hash):
    block = {
        "index": index,
        "timestamp": time.time(),
        "ticket_data": ticket_data,  # Contains event details, buyer, and seat
        "previous_hash": previous_hash,  # Hash of the previous block
        "hash": ""  # Placeholder; to be populated after calculating the hash
    }
    block["hash"] = calculate_hash(block)  # Calculate and add the hash for the block
    return block

# Create Genesis Block (first block in the blockchain)
def create_genesis_block():
    genesis_ticket_data = {
        "event": "Genesis Concert",
        "buyer": "System",
        "seat": "N/A"
    }
    genesis_block = create_block(1, genesis_ticket_data, "0")  # No previous block, so hash is "0"
    return genesis_block

# Function to add a new ticket sale (block)
def add_ticket_sale(event, buyer, seat):
    previous_block = blockchain[-1]  # Get the last block in the blockchain
    new_index = previous_block["index"] + 1  # Increment the index for the new block
    new_ticket_data = {
        "event": event,
        "buyer": buyer,
        "seat": seat
    }
    new_block = create_block(new_index, new_ticket_data, previous_block["hash"])  # Link to previous block's hash
    blockchain.append(new_block)
    return new_block

# Initialize the blockchain with the Genesis Block
if len(blockchain) == 0:
    blockchain.append(create_genesis_block())

# Streamlit UI setup
st.title("Event Ticket Sales Blockchain")
st.write("This is a simple blockchain implementation for managing event ticket sales.")

# Form to input ticket sale details
with st.form("ticket_form", clear_on_submit=True):
    event_name = st.text_input("Event Name", "Rock Festival 2025")
    buyer_name = st.text_input("Buyer Name")
    seat_number = st.text_input("Seat Number")
    submit_button = st.form_submit_button("Add Ticket Sale")

    if submit_button and buyer_name and seat_number:
        new_block = add_ticket_sale(event_name, buyer_name, seat_number)
        st.success(f"Ticket Sale Added! Block #{new_block['index']} created.")
        st.write("Updated Blockchain:")
        st.json(new_block)  # Show the newly added block

# Display the full blockchain
st.subheader("Complete Blockchain")
for block in blockchain:
    st.json(block)
