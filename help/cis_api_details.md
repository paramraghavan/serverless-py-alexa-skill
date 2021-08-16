For every alexa request we make the following 3 calls to CIS in sequence and get the answer back.

Sequence Diagram
------------------
![image](https://user-images.githubusercontent.com/52529498/129519688-5e11bc0b-76cc-4e57-a404-b814e2a3fe88.png)


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
    Request:
    Post the following payload to the above url
        LoginId = "25a5e4b7-20f6-4529-afb0-08995e5ef15b",
        MajorComplaintIds = null,
        PageOriginFlag = 1,
        UserName = "sanalkumar",
        Password = "sanal_123",
        SymptomIds = symptomIds (comma separated), 17,18,20,31
        SymptomsDoctorsNote = null
</pre>

<pre>
    Response snippet:
    [
     {
        "DiagnosisID":112,
        "DiagnosisName":"Acute Meningitis",
        "TotalWeightage":70,
        "Description":"",
        "Link":"",
        "NextAction":"• CT brain No Contrast<br><br>• Do Lumbar Pressure for CSF analysis, after making sure there is no evidence of ICT",
        "LabTest":"CT brain No Contrast",
        "Importants":false,
        "LabTestIds":"93",
        "ImportanceIds":null,
        "DiagnosisIdCollection":null,
        "DiseaseId":0,
        "DiseaseName":null,
        "DiagnosisPriority":101
     },
     {
        "DiagnosisID":173,
        "DiagnosisName":"Sepsis",
        "TotalWeightage":60,
        "Description":"",
        "Link":"",
        "NextAction":"• Start early Broad spectrum antibiotics",
        "LabTest":" ",
        "Importants":false,
        "LabTestIds":null,
        "ImportanceIds":null,
        "DiagnosisIdCollection":null,
        "DiseaseId":0,
        "DiseaseName":null,
        "DiagnosisPriority":101
     },
     {
        "DiagnosisID":174,
        "DiagnosisName":"Severe Sepsis",
        "TotalWeightage":50,
        "Description":"",
        "Link":"",
        "NextAction":"• Look for sepsis induced organ dysfunction and elevated Lactic acid levels",
        "LabTest":" ",
        "Importants":false,
        "LabTestIds":null,
        "ImportanceIds":null,
        "DiagnosisIdCollection":null,
        "DiseaseId":0,
        "DiseaseName":null,
        "DiagnosisPriority":7
     },
     {
        "DiagnosisID":430,
        "DiagnosisName":"Acute Pyelonephritis",
        "TotalWeightage":40,
        "Description":"",
        "Link":"",
        "NextAction":"• Do US kidney in complicated Acute Pyelonephritis<div>Recommended one dose ceftriaxone or one dose Aminoglycoside prior to oral treatment with antibiotics</div>",
        "LabTest":" ",
        "Importants":false,
        "LabTestIds":null,
        "ImportanceIds":null,
        "DiagnosisIdCollection":null,
        "DiseaseId":0,
        "DiseaseName":null,
        "DiagnosisPriority":10
     },
     .
     .
  ]
</pre>
