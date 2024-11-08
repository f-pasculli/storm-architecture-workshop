### Instruction

Create CludFormation stack following the order given by YAMl tempalte files. 

After creating app code module using 04_app_code_module.yaml template, replace "API_GATEWAY_URL" in index.html file and then upload it on root folder of the S3 bucket created by the stack.
The correct API_GATEWAY_URL value can be found as output of 03_api_module stack.

Now you web-app is ready and you enjoy it by using URL given as output by app code module.

Please note:
- module stacks must be launched in right order
- before destroying app-code-module stack you must delete all the files inside S3 bucket, otherwise deletion will fail. 