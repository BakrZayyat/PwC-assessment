import streamlit as st
import openai
openai.api_key = "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"

def generate_quiz(topic, num_questions):
    questions_and_options = []

    for _ in range(num_questions):
        prompt = f"Generate a multiple-choice quiz on {topic}:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extracting question, options, and correct answer from the response
        question_option_set = response.choices[0].text.strip().split("\n\n")
        question = question_option_set[0].strip()
        option_Set = question_option_set[1].strip().split("\n")
        options = [opt.strip() for opt in option_Set[0:]]
        correct_answer = [opt[1:].strip() for opt in options if opt.startswith("*")]

        # Check if the question has at least 4 options
        if len(options) >= 4:
            questions_and_options.append({"question": question, "options": options, "correct_answer": correct_answer[0] if correct_answer else options[0]})

    return questions_and_options

# Streamlit app
def main():
    st.title("MCQ Quiz Application")

    # User input for quiz topic and number of questions
    topic = st.text_input("Enter your preferred quiz topic:")
    num_questions = st.number_input("Enter the number of questions:", min_value=1, value=5)

    # Generate quiz questions and options using OpenAI
    questions_and_options = generate_quiz(topic, num_questions)

    # Display the quiz questions and options in separate pages
    with st.form("quiz_form"):
        for i, qa_pair in enumerate(questions_and_options):
            question = qa_pair["question"]
            options = qa_pair["options"]
            # Display question and options
            st.write(f"*Q{i + 1}:* {question}")
            selected_option = st.radio(f"Select the correct answer for Q{i + 1}", options)

            # Save user's selected option
            st.session_state[f"user_answer_{i+1}"] = selected_option

        # Check if it's the last question to show "Submit Quiz" button
        if st.form_submit_button(label='Submit Quiz'):
            # After submitting, show correct answers in a new page
            st.markdown("## Correct Answers")
            for i, qa_pair in enumerate(questions_and_options):
                correct_answer = qa_pair["correct_answer"]
                st.write(f"Q{i + 1}: {correct_answer}")

# Streamlit app
if __name__ == "__main__":
    main()