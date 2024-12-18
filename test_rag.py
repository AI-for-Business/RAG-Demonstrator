from query_data import query_rag
from langchain_community.llms.ollama import Ollama

# Define a template for evaluating whether the actual response matches the expected response
EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

# Monopoly Test Cases
def test_monopoly_money_on_go():
    assert query_and_validate(
        question="How much money does a player collect when passing 'Go' in Monopoly? (Answer with the number only)",
        expected_response="$200",
    )

def test_monopoly_houses_before_hotel():
    assert query_and_validate(
        question="How many houses must a player have on a property before building a hotel in Monopoly? (Answer with the number only)",
        expected_response="4",
    )

def test_monopoly_wrong_houses_before_hotel():
    # Negative Test: Verify that incorrect expectations are handled
    assert not query_and_validate(
        question="How many houses can a player build on a single property before building a hotel in Monopoly? (Answer with the number only)",
        expected_response="3",  # Incorrect answer expected
    )

def test_monopoly_free_parking():
    assert not query_and_validate(
        question="How much money does a player receive when landing on 'Free Parking' in Monopoly? (Answer with the number only)",
        expected_response="200",  # Incorrect answer expected
    )

# Ticket to Ride Test Cases
def test_ticket_to_ride_train_cars():
    assert query_and_validate(
        question="How many train cars does each player start with in Ticket to Ride? (Answer with the number only)",
        expected_response="45",
    )

def test_ticket_to_ride_destination_cards():
    assert query_and_validate(
        question="How many destination cards does a player draw when they choose to draw new ones in Ticket to Ride? (Answer with the number only)",
        expected_response="3",
    )

def test_ticket_to_ride_longest_path_bonus():
    assert not query_and_validate(
        question="How many points does a player receive for having the longest continuous path in Ticket to Ride? (Answer with the number only)",
        expected_response="15",  # Incorrect answer expected
    )

def test_ticket_to_ride_route_penalty():
    assert not query_and_validate(
        question="How many points is a player penalized if they cannot complete a route in Ticket to Ride? (Answer with the number only)",
        expected_response="50",  # Incorrect answer expected
    )

def query_and_validate(question: str, expected_response: str):
    # Query the RAG system with the given question
    response_text = query_rag(question)

    # Create the evaluation prompt with expected and actual responses
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    # Initialize the Ollama language model with the specified model version
    model = Ollama(model="llama3.2")
    # Invoke the model with the evaluation prompt to get a 'true' or 'false' answer
    evaluation_results_str = model.invoke(prompt)
    # Clean up the evaluation result string by stripping whitespace and converting to lowercase
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    # Print the evaluation prompt for debugging purposes
    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # If the response matches the expected answer, print in green color
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # If the response does not match, print in red color
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        # If the evaluation result is neither 'true' nor 'false', raise an error
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

