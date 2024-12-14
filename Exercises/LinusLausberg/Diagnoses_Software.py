import pandas as pd
# nltk = Natural Language Toolkit
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import kagglehub

# Download dataset using KaggleHub
path = kagglehub.dataset_download("anshulgupta1502/diseases-symptoms")
df = pd.read_csv(f"{path}/Diseases_Symptoms.csv")

# Initialize stopword list
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load data
x = df.iloc[:, [2, 3]]  # Symptoms and Treatment column
y = df[['Name']]

def update_stopwords(new_stopwords):
    """Update the stopword list with new non-symptom words."""
    stop_words.update(new_stopwords)

def preprocess_text(user_input):
    """Tokenize and clean user input by removing stopwords."""
    word_tokens = word_tokenize(user_input.lower())
    return [w for w in word_tokens if w not in stop_words]

def extract_symptoms(processed_tokens, known_symptoms):
    """Extract symptoms from processed tokens by matching with known symptoms."""
    return [word for word in processed_tokens if word in known_symptoms]

# Function to search possible diseases
def searching_possibels_diseases(x, y, extracted_symptoms):
    """Match user symptoms with diseases in the dataset."""
    possible_results = {}
    for counter in range(len(x)):
        symptoms_list = x.loc[counter, 'Symptoms'].lower().split(', ')
        for symptom in extracted_symptoms:
            if symptom in symptoms_list:
                disease = y.loc[counter, 'Name']
                if disease not in possible_results:
                    possible_results[disease] = 1
                elif disease in possible_results:
                    possible_results[disease] += 1
    return possible_results

def input_to_diseases(user_symptoms, known_symptoms):
    """Process user symptoms, match diseases, and return sorted results."""
    processed_tokens = preprocess_text(user_symptoms)
    extracted_symptoms = extract_symptoms(processed_tokens, known_symptoms)

    if not extracted_symptoms:
        print("No recognizable symptoms found.")
        return {}
    
    possible_results = searching_possibels_diseases(x, y, extracted_symptoms)
    sorted_results = dict(sorted(possible_results.items(), key=lambda item: item[1], reverse=True))
    keys = list(sorted_results.keys())
    max_count =  sorted_results[keys[0]]
    for key in keys:
        if sorted_results[key] <=  max_count/3:
            sorted_results.pop(key)
    data = []
    count = 0
    for disease, probability in sorted_results.items():
        data.append([disease,probability])
        count += 1
    final_df = pd.DataFrame(data, columns=['Disease', 'Probability'])
    print(final_df)
    return sorted_results

# Known symptoms from dataset
known_symptoms = set(', '.join(df['Symptoms']).split(', '))

# Example input
# user_symptoms = input('What are your sympytoms?')
# Fracture
# user_symptoms = 'After the accident, the patient experienced swelling and bruising around the injured area. There was a noticeable deformity, and the patient reported difficulty moving the limb due to severe pain. Additionally, they experienced blurred vision and saw halos around lights, indicating a possible concussion and loss of function in the affected area.'
# Pulmonary Eosinophilia
# user_symptoms = 'So listen, in the last few days i have experienced some bloatin and vomiting as well as Nausea and abdominal pain. and another Problem is constipation. please, no doctor could tell me whats wrong with me.'
# Volvulus
user_symptoms = 'On Monday i had to Cough a lot an after traning I had chest pain, fever, night sweats, Fatigue. Also I had a shortness of Breath for an exdente period of time.'


# Process input and match diseases
sorted_results = input_to_diseases(user_symptoms, known_symptoms)

# Update stopwords if sowhat went completely wrong
additional_stopwords = ['accident', 'injured', 'area', 'noticed', 'patient', 'report', 'function']
update_stopwords(additional_stopwords)
