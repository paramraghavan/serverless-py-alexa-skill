For every alexa request we make the following 3 calls to CIS in sequence and get the answer back.

# Step 1
- Invoke Boto3 api as follows:
<pre>  
    client = aws_utils.get_boto3_client(cis_dict["awsaccesskeyid"], cis_dict["awssecretaccesskey"], 'comprehendmedical')
    response = client.detect_entities_v2(
        Text= 'Fever, cold, paracetamol, aspirin, headache, shortness of breath, blurry vision, mango, lemonade, mahesh'
    )
   
    Input text sent to alexa by caller 
        --> Fever, cold, paracetamol, aspirin, headache, shortness of breath, blurry vision, mango, lemonade, mahesh
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
    This call returns all the Symptoms and the corresponding Id's configured in the CIS system.
    For example:
     'Fever' in step 1 matches ID 17 below. We make a comma separated list of relevant symptom id's 
      and pass this list to next step.
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
  Following url  returns the response which is sent back as alexa response:
  http://ciswebapi.azurewebsites.net/api/DiagnosisResults/
  Input to above url is the list of SyptomId's based on step 2 - 17,18,20,31
<pre>
    Post the following payload to the above url
        LoginId = "25a5e4b7-20f6-4529-afb0-08995e5ef15b",
        MajorComplaintIds = null,
        PageOriginFlag = 1,
        UserName = "sanalkumar",
        Password = "sanal_123",
        SymptomIds = symptomIds (comma separated), 17,18,20,31
        SymptomsDoctorsNote = null
</pre>
