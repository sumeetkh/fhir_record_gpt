
'''
import json
import fhirclient.models.patient as p
with open('fhir/Zackary401_Littel644_b3e09e1a-6149-4b8f-a045-29f135ad8884.json', 'r') as h:
    pjs = json.load(h)
patient = p.Patient(pjs)
patient.name[0].given
'''

from fhirclient import client
import json
#from fhirclient.models.fhirabstractbase import FHIRAbstractBase


# Create an instance of the FHIR client using the server URL
settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://my.fhir.server.com/baseDstu3'
}
smart = client.FHIRClient(settings=settings)

# Read #the contents of the file containing the Bundle

with open('fhir/Alejandra902_Villa94_63056f6b-4cb3-4f9b-9a62-c3817991e6a1.json', 'r') as f:
    bundle_json = json.load(f)

# Parse the Bundle using the FHIR client
entries = bundle_json['entry']

print("Parsed entires")

# Parse the Bundle using the FHIR client
# bundle = smart.parse_resources('Bundle', bundle_json)

# Iterate through the resources in the Bundle and handle each one appropriately
condition_arr = []
for entry in entries:
    resource = entry.get("resource", None)
    #print(resource)
    resource_type = resource.get("resourceType", None)
    
    print(resource_type)

    if resource_type == 'Procedure':
        print(resource)

        condition_arr.append(resource)
   
    '''
    if resource_type == 'Patient':
        # Handle Patient resource
        print('Handling Patient resource')
    elif resource_type == 'Observation':
        # Handle Observation resource
        print('Handling Observation resource')
    elif resource_type == 'MedicationRequest':
        # Handle MedicationRequest resource
        print('Handling MedicationRequest resource')
    else:
        # Handle other resource types as needed
        print('Handling resource of type {}'.format(resource_type))
    '''


#print(condition_arr)
with open('tmp/procedure.json', 'w') as out:
    out.write(json.dumps(condition_arr[0]))





