# First Step
- Invoke Boto3 api as follows:
<pre>  
    client = aws_utils.get_boto3_client(cis_dict["awsaccesskeyid"], cis_dict["awssecretaccesskey"], 'comprehendmedical')
    response = client.detect_entities_v2(
        Text= 'Fever, cold, paracetamol, aspirin, headache, shortness of breath, blurry vision, mango, lemonade, mahesh'
    )
   
    Input from alexa --> Fever, cold, paracetamol, aspirin, headache, shortness of breath, blurry vision, mango, lemonade, mahesh
    Response:
    # Note we have filtered out the response to keep only the Medical Condition
    | Fever |MEDICAL_CONDITION |
    | cold |MEDICAL_CONDITION |
    | headache |MEDICAL_CONDITION |
    | shortness of breath |MEDICAL_CONDITION |
    | blurry vision |MEDICAL_CONDITION |
</pre>

# Step 2
- Invoke http://clickifsickservice.azurewebsites.net/DetailsCollections.svc/GetAllSymptomKeywords/sanalkumar/sanal_123/
<pre>
This returns all the Symptoms and the corresponding Id's. 
In this step we will get all the ID's for all the medical conditions returned in step 1 above. For example
 'Fever' in step 1 matches ID 17 below. So we make a comma separated list of all the 
 Symptom id's
  17,18,20,31 and we pass this list to next step.
Partial response Snippet
[
{
"ID": 2,
"ParentID": 0,
"SymptomKeyWord": "",
"SymptomName": "Low iron"
},
{
"ID": 3,
"ParentID": 0,
"SymptomKeyWord": "Normal platelets",
"SymptomName": "Schistocytes with normal platelets"
},
{
"ID": 5,
"ParentID": 0,
"SymptomKeyWord": "subkey1,subkey2",
"SymptomName": "Surgical scar"
},
{
"ID": 6,
"ParentID": 0,
"SymptomKeyWord": "",
"SymptomName": "Hypotension"
},
{
"ID": 7,
"ParentID": 0,
"SymptomKeyWord": "appendicitis, pain",
"SymptomName": "Positive grey turner or Cullen sign"
},
{
"ID": 17,
"ParentID": 0,
"SymptomKeyWord": "",
"SymptomName": "Fever"
}
]
</pre>

# Step 3
 To this url: http://ciswebapi.azurewebsites.net/api/DiagnosisResults/
<pre>
    Post the following payload
        LoginId = "25a5e4b7-20f6-4529-afb0-08995e5ef15b",
        MajorComplaintIds = null,
        PageOriginFlag = 1,
        UserName = "sanalkumar",
        Password = "sanal_123",
        SymptomIds = symptomIds (comma separated), 17,18,20,31
        SymptomsDoctorsNote = null
</pre>
