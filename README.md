## Disclaimer

This work is not meant to be used in it's current form - it's a demo app. Medical
records, histories and recommendations should be used carefully. While AI systems will
provide a lot of utility and value generation in these areas - there are a lot of potential harms 
and possibilities of misuse. This work requires more iterations before it can be used.


## fhir_record_gpt

- Use requirements.py to build a local environment
- Run the Flask server
- Fun index.html, input a FHIR filename as the File Name param and ask questions.


## Try some questions

- Could you summarize the active conditions for the patient?
- Tell me more details about Anemia condition for the patient?
- Which of the most recent observations are outside the normal range?
- What are some recommendations you'd make based on the observations?



## Right now the following form of questions are supported

- Summarizing the entire history, e.g. summarizing history of procedures or conditions.
- Query specific questions about a procedure, summary, claim, medication etc.
- Ask for diet/exercise plan recommendations based on conditions or recent observations.


## Synthetic Data

- fhir folder contains synthetic data that can be used in the question. 
- The data is limited in information about claims and CarePlans, but the code will work if those resources are included
and queried
