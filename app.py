import json
import random
import streamlit as st

from time import sleep


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


# Generate a unique key based on the question and answer
def generate_key(question, answer):
    return f"{question}_{answer}"


# Display flashcard
def display_flashcard(flashcard):
    def submitted():
        st.session_state.submitted = True

    answers = [flashcard["correct answer"]] + flashcard["incorrect answers"]
    shuffled_answers = shuffle_answers(answers)

    with st.form(
        generate_key(flashcard["question"], flashcard["correct answer"]),
        clear_on_submit=False,
    ):
        # Display answer choices as a single block using st.radio
        selected_answer = st.radio(
            flashcard["question"],
            shuffled_answers,
            key=generate_key(flashcard["question"], "radio"),
        )

        st.form_submit_button("Submit", on_click=submitted)

    return flashcard


# Main function
def main():
    flashcard_file = "static/numbering_systems.json"
    flashcards = load_flashcards(flashcard_file)

    st.title("Study App")
    

    if len(flashcards) == 0:
        st.warning("No flashcards found. Please check the flashcard file.")
        return

    if "submitted" in st.session_state:
        if st.session_state.submitted:
            selected_answer = None

            # Iterate over the dictionary items and find the selected answer
            for key, value in st.session_state.items():
                if key.endswith("_radio") and value:
                    selected_answer = value
                    break

            # Check the answer and display feedback
            if selected_answer == st.session_state["correct answer"]:
                st.markdown("Congratulations! You have chosen the correct answer.")
            else:
                st.markdown("Oops! You have chosen the incorrect answer.")
                st.markdown(
                    f"The correct answer is {st.session_state['correct answer']}."
                )

            st.button("next")

            st.session_state["submitted"] = False

        else:
            random_flashcard = random.choice(flashcards)

            flashcard = display_flashcard(random_flashcard)
            st.session_state["correct answer"] = random_flashcard["correct answer"]

    else:
        # Randomly select and display a flashcard initially
        random_flashcard = random.choice(flashcards)

        flashcard = display_flashcard(random_flashcard)
        st.session_state["correct answer"] = random_flashcard["correct answer"]

        if random_flashcard in flashcards:
            print('yes')


if __name__ == "__main__":
    main()
