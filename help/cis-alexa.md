# Alexa cookbook
- https://github.com/alexa/alexa-cookbook
- https://github.com/alexa-samples?q=&type=&language=python&sort=  
- https://github.com/alexa-samples/skill-sample-python-colorpicker

# serverless.com, see this if you are new to serverless
https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb

# https://rupakganguly.com/posts/how-to-build-a-serverless-alexa-skill/
# https://www.serverless.com/blog/serverless-python-packaging
# create project
sls create -t aws-python --name sls-py-alexa-color-picker -p sls-py-alexa-color-picker
cd sls-py-alexa-color-picker
sls plugin install -n serverless-alexa-skills
sls plugin install -n serverless-python-requirements
cd auth-yml
sls alexa auth
cd ..

- sls alexa create --name ColorPicker --locale en-US --type custom
- Serverless: [Skill ID] amzn1.ask.skill.e445454-3a30-er343-a694-erererererere

# create manifests and update with skill
- sls alexa manifests
# Add intents to the model. Update(save the model) and build the model
sls alexa update

#build model
sls alexa build

#see the model created
sls alexa models 

serverless deploy -v --stage dev
# removes the deployed lambda endpoint
# serverless remove -v --stage dev

npm install --save serverless-python-requirements


# CIs Diagnosis
- sls alexa create --name CISDiagnosis --locale en-US --type custom

Rest API Click if Sick
-------------------------
https://awscli.amazonaws.com/AWSCLIV2.pkg