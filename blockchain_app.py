import streamlit as st
from blockchain_core import Blockchain
import json

# -----------------------------------------------------------------------------------
# Initialize the blockchain in the Streamlit session state.
# This ensures that the blockchain persists across user interactions.
# -----------------------------------------------------------------------------------
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain(difficulty=3)

blockchain = st.session_state.blockchain

# -----------------------------------------------------------------------------------
# Configure the Streamlit web app layout and styling
# -----------------------------------------------------------------------------------
st.set_page_config(page_title="Toy Blockchain", layout="centered")

# Apply custom CSS for a clean white background and a dark blue title
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    .main-title {
        color: #003366;
        font-size: 2.5rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------------
# Display Title and Author Information
# -----------------------------------------------------------------------------------
st.markdown('<div class="main-title">Toy Blockchain System</div>', unsafe_allow_html=True)
st.write("Author: **Briand Lancelot Rubin**")
st.markdown("This web interface demonstrates a simplified blockchain prototype with proof-of-work mining implemented in Python.")

# -----------------------------------------------------------------------------------
# Sidebar Menu: Choose an action to interact with the blockchain
# -----------------------------------------------------------------------------------
with st.sidebar:
    st.header("Actions")
    action = st.radio("Choose an action", [
        "Add Block",
        "View Blockchain",
        "Search Blockchain",
        "Check Chain Integrity",
        "Tamper with Block",
        "Save to File"
    ])

# -----------------------------------------------------------------------------------
# Action: Add and Mine a New Block
# -----------------------------------------------------------------------------------
if action == "Add Block":
    st.subheader("Add and Mine a New Block")
    data = st.text_area("Enter data for the new block:")
    if st.button("Mine and Add"):
        if data.strip() == "":
            st.warning("Please enter data before mining.")
        else:
            blockchain.add_block(data)
            st.success("New block successfully mined and added.")

# -----------------------------------------------------------------------------------
# Action: View the Entire Blockchain
# -----------------------------------------------------------------------------------
elif action == "View Blockchain":
    st.subheader("View Blockchain")
    for block in blockchain.chain:
        with st.expander(f"Block {block.header.index}"):
            st.json({
                "Index": block.header.index,
                "Timestamp": block.header.timestamp,
                "Nonce": block.header.nonce,
                "Previous Hash": block.header.previous_hash,
                "Hash": block.header.hash,
                "Difficulty": block.header.difficulty,
                "Data": block.data,
                "Mining Time": f"{getattr(block, 'mining_time', 'N/A')} seconds"
            })

# -----------------------------------------------------------------------------------
# Action: Search the Blockchain for a Keyword
# -----------------------------------------------------------------------------------
elif action == "Search Blockchain":
    st.subheader("Search Blockchain")
    keyword = st.text_input("Enter keyword to search:")
    if st.button("Search"):
        found = False
        for block in blockchain.chain:
            if keyword.lower() in str(block.data).lower():
                st.success(f"Found in Block {block.header.index}: {block.data}")
                found = True
        if not found:
            st.error("Keyword not found in any block.")

# -----------------------------------------------------------------------------------
# Action: Validate the Blockchain's Integrity
# -----------------------------------------------------------------------------------
elif action == "Check Chain Integrity":
    st.subheader("Blockchain Integrity Check")
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        st.success("Blockchain is valid.")
    else:
        st.error("Blockchain integrity is broken.")

# -----------------------------------------------------------------------------------
# Action: Tamper with a Block (for demonstration purposes)
# -----------------------------------------------------------------------------------
elif action == "Tamper with Block":
    st.subheader("Tamper with a Block")
    indices = list(range(len(blockchain.chain)))
    tamper_index = st.selectbox("Select block index to tamper", indices)

    if tamper_index == 0:
        st.warning("Genesis block cannot be tampered.")
    elif st.button("Tamper"):
        blockchain.tamper_block(tamper_index)
        st.warning(f"Block {tamper_index} has been modified for testing purposes.")

# -----------------------------------------------------------------------------------
# Action: Save the Blockchain to a Local JSON File
# -----------------------------------------------------------------------------------
elif action == "Save to File":
    st.subheader("Save Blockchain")
    filename = st.text_input("Enter filename (default: blockchain.json)", value="blockchain.json")
    if st.button("Save"):
        blockchain.save_to_file(filename)
        st.success(f"Blockchain saved as '{filename}'.")

        # Optional: Provide a download button
        with open(filename, "r") as f:
            st.download_button("Download File", f.read(), file_name=filename)
