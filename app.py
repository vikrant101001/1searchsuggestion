import streamlit as st
import time

# Custom CSS to style the application
def apply_custom_css():
    st.markdown("""
        <style>
        /* Dark theme colors with gradient */
        .stApp {
            background: linear-gradient(135deg, #1E1E1E, #2C3E50);
            color: #FFFFFF;
        }
        
        /* Title styling */
        h1 {
            color: #00FF9F;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 700;
            margin-bottom: 2rem;
        }
        
        h3 {
            color: #00CED1;
            margin-bottom: 2rem;
        }
        
        /* Custom search container with glass effect */
        .search-container {
            background: rgba(45, 45, 45, 0.7);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Custom search input */
        .stTextInput input {
            background-color: rgba(61, 61, 61, 0.8) !important;
            color: white !important;
            border: 2px solid rgba(0, 255, 159, 0.3) !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            font-size: 18px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: #00FF9F !important;
            box-shadow: 0 0 15px rgba(0, 255, 159, 0.3) !important;
        }
        
        /* Suggestion style */
        .suggestion {
            background: linear-gradient(90deg, rgba(61, 61, 61, 0.8), rgba(45, 45, 45, 0.8));
            padding: 15px 25px;
            margin: 10px 0;
            border-radius: 12px;
            transition: all 0.3s ease;
            border-left: 4px solid #00FF9F;
            cursor: pointer;
        }
        
        .suggestion:hover {
            background: linear-gradient(90deg, rgba(71, 71, 71, 0.9), rgba(55, 55, 55, 0.9));
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(45, 45, 45, 0.7) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            color: #00CED1 !important;
        }
        
        .streamlit-expanderContent {
            background-color: rgba(45, 45, 45, 0.5) !important;
            border-radius: 0 0 12px 12px !important;
            padding: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Trie Node class implementation
class TrieNode:
    def __init__(self):
        # Initialize a dictionary to store children nodes (characters)
        self.children = {}
        # Flag to mark end of a word
        self.is_end_of_word = False
        # Store the complete word at leaf nodes
        self.word = None

# Trie class implementation
class Trie:
    def __init__(self):
        # Initialize root node
        self.root = TrieNode()
    
    def insert(self, word):
        # Start from root node
        node = self.root
        
        # Iterate through each character in the word
        for char in word.lower():
            # If character doesn't exist, create a new node
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move to the next node
            node = node.children[char]
        
        # Mark end of word and store the complete word
        node.is_end_of_word = True
        node.word = word
    
    def search_suggestions(self, prefix, max_suggestions=3):
        suggestions = []
        
        # Start from root and reach the node corresponding to prefix
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return suggestions
            node = node.children[char]
        
        # Perform DFS to find suggestions
        self._dfs_suggestions(node, suggestions, max_suggestions)
        return suggestions
    
    def _dfs_suggestions(self, node, suggestions, max_suggestions):
        # If max suggestions reached, stop
        if len(suggestions) >= max_suggestions:
            return
        
        # If current node is end of a word, add to suggestions
        if node.is_end_of_word:
            suggestions.append(node.word)
        
        # Recursively explore all children
        for char in sorted(node.children.keys()):
            self._dfs_suggestions(node.children[char], suggestions, max_suggestions)

def load_data():
    # Initialize Trie
    trie = Trie()
    
    # Read data from file and insert into trie
    with open('data.txt', 'r') as file:
        for line in file:
            word = line.strip()
            trie.insert(word)
    
    return trie

def main():
    # Set page config first
    st.set_page_config(
        page_title="Search Suggestions using Tries",
        page_icon="🔍",
        layout="centered"
    )
    
    # Then apply custom CSS
    apply_custom_css()
    
    # Load data into trie
    trie = load_data()
    
    # Title and description
    st.title("Real World Applications of DSA:")
    st.subheader("Part 1 - Search Suggestion using Tries (Prefix Trees)")
    
    # Create search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input(
        "Start typing to see suggestions...",
        key="search_input"
    )
    
    # Get and display suggestions
    if search_query:
        suggestions = trie.search_suggestions(search_query)
        
        # Display suggestions with animation
        for suggestion in suggestions:
            st.markdown(
                f'<div class="suggestion">{suggestion}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.1)  # Small delay for animation effect
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add information about Tries
    with st.expander("Learn about Tries (Prefix Trees)"):
        st.markdown("""
        A Trie (also called prefix tree) is an efficient tree-like data structure used for:
        - Fast string search
        - Autocomplete features
        - Spell checkers
        
        **Time Complexity:**
        - Search: O(m) where m is the length of the string
        - Space: O(ALPHABET_SIZE * m * n) where n is number of words
        """)

if __name__ == "__main__":
    main() 