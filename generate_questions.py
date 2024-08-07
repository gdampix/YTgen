import pandas as pd

class GenerateQuestions:

    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path

    # Function to process the CSV file
    def get_n_questions(self, n_questions):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.csv_path)

        if n_questions:
            df = df.sample(n_questions,replace=True)
        
        # List to hold the dictionaries
        questions_data = []
        
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            # Create the dictionary for the current row
            question_data = {
                "id_question": row['question'],
                "id_option_1": row['option_1'],
                "id_option_2": row['option_2'],
                "id_option_3": row['option_3'],
                "id_option_4": row['option_4'],
            }
            
            # Store the correct option
            correct_option_id = "id_"+row['correct_option']
            
            # Append the dictionary and correct option to the list
            questions_data.append({
                'question_data': question_data,
                'correct_option': correct_option_id
            })
        
        return questions_data


if __name__=="__main__":
    # Specify the path to your CSV file
    csv_file_path = 'data/csv/qbank.csv'
    n_questions = 2

    # Process the CSV file
    gq = GenerateQuestions(csv_file_path)
    questions = gq.get_n_questions(n_questions)

    # Print the processed data
    for item in questions:
        print(f"Question Data: {item['question_data']}")
        print(f"Correct Option: {item['correct_option']}")
        print('---')