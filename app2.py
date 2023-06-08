import json
import random
import streamlit as st

# Load flashcards from JSON file
def load_flashcards(file_path):
    try:
        with open(file_path, "r") as file:
            flashcards = json.load(file)
        return flashcards["flashcards"]
    except (IOError, ValueError, KeyError) as e:
        st.error(f"Failed to load flashcards from {file_path}: {str(e)}")
        return []

# Shuffle the answers (correct and incorrect)
def shuffle_answers(answers):
    random.shuffle(answers)
    return answers

# Display flashcard
def display_flashcard(flashcard):
    def submitted():
        st.session_state.submitted = True

    answers = [flashcard["correct answer"]] + flashcard["incorrect answers"]
    shuffled_answers = shuffle_answers(answers)

    with st.form(
        flashcard["question"] + "_" + flashcard["correct answer"],
    ):
        # Display answer choices as a single block using st.radio
        selected_answer = st.radio(
            flashcard["question"],
            shuffled_answers,
            key=flashcard["question"] + "_radio",
        )

        st.form_submit_button("Submit", on_click=submitted)
    
    return flashcard

# Main function
def main():
    # Configure Streamlit page settings
    st.set_page_config(page_title="Numbering Systems", page_icon="images/TSK Logo Circle_Green.psd", menu_items={
        'Get Help': 'https://www.techsmart.codes/contact/',
        'Report a bug': "https://www.techsmart.codes/contact/",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

    # Path to the flashcard JSON file
    flashcard_file = "utils/numbering_systems.json"

    # Load flashcards from the file
    flashcard_deck = load_flashcards(flashcard_file)

    # Initialize session state variables if not already present
    if "flashcard_deck" not in st.session_state:
        st.session_state['flashcard_deck'] = flashcard_deck
    
    if "submitted" not in st.session_state:
        st.session_state['submitted'] = False

    if "random_flashcard" not in st.session_state:
        st.session_state['random_flashcard'] = {}

    # Display the title of the flashcard application
    st.title("Numbering Systems")

    # Display the number of flashcards remaining in the deck
    st.write("There are", len(st.session_state['flashcard_deck']), "more cards in this deck!")

    # if len(st.session_state['flashcard_deck']) == 0:
    #     # Display a warning message if there are no flashcards
    #     st.warning("No flashcards found. Please check the flashcard file.")
    #     return

    if not st.session_state['submitted']:
        # Randomly select and display a flashcard initially
        random_flashcard = random.choice(st.session_state['flashcard_deck'])
        display_flashcard(random_flashcard)

        # Store the randomly selected flashcard in session state
        st.session_state["random_flashcard"] = random_flashcard

        # Store the correct answer separately for checking later
        st.session_state["correct answer"] = random_flashcard["correct answer"]
    
    else:
        # Get the question from the randomly selected flashcard
        question = st.session_state['random_flashcard']['question']

        # Reset the submitted state for the next flashcard
        st.session_state["submitted"] = False

        # Remove the current flashcard from the deck
        index = st.session_state['flashcard_deck'].index(st.session_state['random_flashcard'])
        st.session_state['flashcard_deck'].pop(index)

        # Clear the randomly selected flashcard from session state
        st.session_state["random_flashcard"] = {}

        selected_answer = None

        # Iterate over the session state items and find the selected answer
        for key, value in st.session_state.items():
            if key.endswith("_radio") and value:
                selected_answer = value
                break    

        # Check the answer and display feedback
        if selected_answer == st.session_state["correct answer"]:
            st.markdown(f"_{question}_")
            st.markdown(f"Congratulations! You have chosen the correct answer: **{st.session_state['correct answer']}**")
        else:
            st.markdown(f"_{question}_")
            st.markdown("Oops! You have chosen the incorrect answer.")
            st.markdown(f"The correct answer is: **{st.session_state['correct answer']}**")

        # Display a button for the next flashcard
        st.button("Next")

# Entry point of the script
if __name__ == "__main__":
    main()
