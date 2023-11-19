import streamlit as st

# Function to read and format the story
def display_story(story_path):
    with open(story_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('Title:'):
            st.header(line.strip())  # Display the title as a header
        elif line.startswith('Chapter'):
            st.subheader(line.strip())  # Display chapter titles as subheaders
        else:
            st.write(line)  # Display the story content

# Setting the title of the Streamlit app
st.title("AI Novel Generator")

# Getting user inputs for country and genre
country = st.text_input("Enter the country where the novel is set:", "Korea")
genre = st.text_input("Enter the genre of the novel:", "Fantasy")

# Dynamic character inputs
st.subheader("Character Information")
# Use a session state to keep track of the number of characters
if 'num_characters' not in st.session_state:
    st.session_state.num_characters = 1

# Function to add a new character input
def add_character():
    st.session_state.num_characters += 1

# Button to add new character
st.button("Add Character", on_click=add_character)

# Create inputs for each character
characters = []
for i in range(st.session_state.num_characters):
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Name of character {i+1}", key=f"name_{i}")
        with col2:
            description = st.text_input(f"Description of character {i+1}", key=f"description_{i}")
        characters.append((name, description))

# Button to generate the novel
if st.button("Generate Novel"):
    display_story('/root/kinam/Children-Book-Dataset/story.txt')

# Command to run the Streamlit app (needed when executing the file)
# if __name__ == "__main__":
#     st.run()
