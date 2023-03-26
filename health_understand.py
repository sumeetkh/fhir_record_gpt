import os
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

from fhirclient import client
import json

# Create an instance of the FHIR client using the server URL
settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://my.fhir.server.com/baseDstu3'
}

smart = client.FHIRClient(settings=settings)


os.environ["OPENAI_API_KEY"] = "<Key>"

template_text = """
You are an intelligent tool capable of deeply understanding FHIR records. You can
navigate over multiple resources and provide information that enables understanding
and efficient decision making.

When given an objective, Based on your given objective, you should plan the right sequence. You have the following commands
that you can sequence

SEMANTIC_SEARCH  ResourceType



These Commands have the following schema, and each command will update the observation.

The following are the only valid SEQUENCES

SEMANTIC_SEARCH  ResourceType


=============================
SEMANTIC_SEARCH ResourceType 

ResourceType : Type of Resouce to Query : such as Procedure, Observation, Condition, Encounter, Medication or Claim


==============================

Examples

Question: List all the procedures performed on the patient?
Command: SEMANTIC_SEARCH PROCEDURE

Question: List all the Conditions for the patient?
Command: SEMANTIC_SEARCH CONDITIONS

Question: List all the procedures carried out for the patient in 2018?
Command: SEMANTINC_SEARCH PROCEDURE

Question: What was the outcome of the procedure Number 123?
Commmand: SEMANTIC_SEARCH PROCEDURE; 

Question: Describe the most recent care plan?
Command: SEMANTIC_SEARCH CAREPLAN



==================================
Question: {question}
Command: 
"""

llm = OpenAI(temperature=0, model_name="gpt-4")
new_prompt = PromptTemplate(
    input_variables=["question"], 
    template=template_text
)

new_promp_chain = LLMChain(llm=llm, prompt=new_prompt)


query_template = """
{query}

{resource}
"""

query_prompt = PromptTemplate(
    input_variables=["query", "resource"], 
    template=query_template
)
query_chain = LLMChain(llm=llm, prompt=query_prompt)


find_resource_query_template = """
Out of the following resources, find the resource json that effectively answers the following 
query. Output only the relevant json and nothing else. It is OK if the JSON enables a partial
answer to the question

Query: {query}
Resources:

{resources}

Output: 
"""
find_resource_prompt = PromptTemplate(
    input_variables=["query", "resources"], 
    template=find_resource_query_template
)
find_resource_chain = LLMChain(llm=llm, prompt=find_resource_prompt)


find_dependencies_query_template = """
Find the uuids of dependend of the following resource. 

A dependency is one of the FHIR keys that 
"""

#summary_chain = LLMChain(llm=llm, prompt=summary_input_prompt)

'''
multiple_input_prompt = PromptTemplate(
    input_variables=["query", "observation"], 
    template=template_text
)


summary_text_template = """
Summarize the {resource_type} for the patient

{resource}
"""

summary_input_prompt = PromptTemplate(
    input_variables=["resource_type", "resource"], 
    template=summary_text_template
)


chain = LLMChain(llm=llm, prompt=multiple_input_prompt)

summary_chain = LLMChain(llm=llm, prompt=summary_input_prompt)
'''
#output = chain.run(customer_message="hello", order_id="test")



def get_entries(filename):
    with open(filename, 'r') as f:
        bundle_json = json.load(f)

    # Parse the Bundle using the FHIR client
    entries = bundle_json['entry']
    return entries


def lookup_all(entries, command):
    resource_type = command.removeprefix("SEMANTIC_SEARCH").strip()

    print(f"getting all resources of type {resource_type}")
    ret = []
    for entry in entries:
        resource = entry.get("resource", None)
        resource_str = resource.get("resourceType", None)
        if resource_str is not None and resource_str.lower() == resource_type.lower():
            ret.append(entry)

    return ret


def execute_query(query, results):
    return query_chain.run(query=query, resource=json.dumps(results))


def find_closest_resource(query, results):
    return find_resource_chain.run(query=query, resources=json.dumps(results))


def fetch_observations(entries):
    recent_observations = []
    for entry in entries:
        resource = entry.get("resource", None)
        resource_str = resource.get("resourceType", None)
        if resource_str == "Observation":
            recent_observations.append(entry)
    return recent_observations[-15:]


def fetch_commands(filename, question):
    entries = get_entries(filename)

    
    # Observations has to be extracted separately because of the large number of observations
    # this will be addressed if 32k size GPT-4 backend is used, my current key is restricted to 8k 
    # tokens
    if "observation" in question or "Observation" in question:
        recent_observations = fetch_observations(entries)
        print(recent_observations)
        query_response = execute_query(question, recent_observations)
        return query_response

    output = new_promp_chain.run(question=question)
    commands = output.split(";")
    print(commands)
    query_response = ""
    if len(commands) == 1:
        first_command = commands[0]
        print(f"Executing {first_command}")
        if first_command.startswith("SEMANTIC_SEARCH"):
            results = lookup_all(entries, first_command)
            print(results)
            query_response = execute_query(question, results)
    elif len(commands) == 3:
        first_command = commands[0]
        if first_command.startswith("SEMANTIC_SEARCH"):
            results = lookup_all(entries, first_command)
            closest_resource = find_closest_resource(question, results)
            print(closest_resource)
    return query_response

'''
if __name__ == "__main__":
    final_output = process_record()
    print(final_output)
'''

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

#cors = CORS(app, resources={r"/*": {"origins": ["https://localhost:5001"]}})

@app.route('/api', methods=['POST'])
def wrap_function1():
    data = request.get_json()
    file_name = data.get('file_name')
    question = data.get('question')
    command_outputs = fetch_commands(file_name, question)
    print(command_outputs)
    return jsonify({"answer": command_outputs})
    

if __name__ == '__main__':
    app.run(debug=True)

