import os, requests, json, pprint, yaml, urllib3, sqlvalidator, re
import openai

def load_creds(config_file_path=None):
    """
    This function returns the needed credentials to run the service.

    Param path: path to the file containing the credentials
    return: dict of configuration strings
    """
    
    try:
        if config_file_path is None:
            
            base_path = os.getcwd()
            operating_system = os.name

            print("######################################", operating_system)

            #try first for a windows os
            if operating_system == "nt": 
                config_file_path = base_path +"\\poc-cfg\\OpenAI.yml"

            #in case FileNotFoundError
            elif operating_system == "posix":
                config_file_path = base_path + "/poc-cfg/OpenAI.yml"

            with open(config_file_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            return data
                
    except:
        raise

def get_response(start_phrase: str, model: str, temperature: float, max_tokens: int, stop: list, n=1, best_of=1):

    creds = load_creds()

    # Pick deployment name from config file
    if model == 'GPT':
        deployment_name = creds['deployment_name_gpt']
    elif model == 'Codex':
        deployment_name = creds['deployment_name_codex']
    else:

        # Default to GPT
        deployment_name = creds['deployment_name_gpt']
    
    url = creds['base_url'] + "/openai/deployments/" + deployment_name + "/completions?api-version=2022-12-01"

    headers={
        "api-key": creds['api_key'],
        "Content-Type": "application/json"
    }

    payload = {        
        "prompt": start_phrase + " SELECT",
        "temperature": temperature,    #altering this or top_p but not both
        "max_tokens": max_tokens,      #The maximum number of tokens to generate in the completion.
        "top_p": 1,                    #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        "n": n,                        #How many completions to generate for each prompt
        "best_of":best_of,                   #Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed. When used with n, best_of controls the number of candidate completions and n specifies how many to return – best_of must be greater than n.  
        "frequency_penalty": 0.0,      #Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        "presence_penalty": 0.0,       #Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
        "stream": False,               #
        "logprobs": 5,                 # 
        "stop": stop                   #
        
    }

    
    # Call API
    payload_str = json.dumps(payload)
    h = urllib3.PoolManager()
    call = h.request(
        'POST',
        url,
        headers = headers,
        body=payload_str
    )

    response = json.loads(str(call.data.decode('utf-8')))

    """
    model: we use "davinci" for GPT-3 and CODEX.
    max_tokens: set it to a sufficient number to allow the model to provide a complete answer.
    temperature: set it to a value between 0 and 1 to control the diversity and creativity of the generated text.
    top_p: set it to a value between 0 and 1 to control the probability of the model selecting the most likely tokens, the value is on 0.9
    n: set it to a value of 1 to get a single response from the model.  
    """
    print(response)
    # return the extract the text from the response

    return response['choices'][0]['text']



def query_validator(query):

    sql_query = sqlvalidator.parse(query)

    if sql_query.is_valid():
        return { 'valid': True }
    else:
        print(sql_query.errors)
        return { 'valid': False, "errors": sql_query.errors }
    
def query_cleanup(query: str):
    # Simple cases
    output = query.replace("```sql","")
    output = output.replace("```","")
    output = output.replace("# ","")
    #output = output.replace("\n\n","")

    # More sophisticated cases with regex
    output = re.sub(r'^\n\n','', output) # Double line break at beginning of response
    output = re.sub(r'^\s*','', output) # Initial white spaces
    output = re.sub(r'^\?','', output) # Initial white spaces

    output = "SELECT "+ output
    return output


#EXAMPLE: 

#start_phrase1 = """### Postgres SQL tables, with their properties:
## Employee(id, name, department_id)
# Department(id, name, address)
# Salary_Payments(id, employee_id, amount, date)
#### A query to list the names of the departments which employed more than 10 employees in the last 3 months"""




#start_phrase2 = """SQL tables, with their properties:
#['customers(customerNumber,customerName,contactLastName,contactFirstName,phone,addressLine1,addressLine2,city,state,postalCode,country,salesRepEmployeeNumber,creditLimit)', 'employees(employeeNumber,lastName,firstName,extension,email,officeCode,reportsTo,jobTitle)', 'offices(officeCode,city,phone,addressLine1,addressLine2,state,country,postalCode,territory)', 'orderdetails(orderNumber,productCode,quantityOrdered,priceEach,orderLineNumber)', 'orders(orderNumber,orderDate,requiredDate,shippedDate,status,comments,customerNumber)', 'payments(customerNumber,checkNumber,paymentDate,amount)', 'productlines(productLine,textDescription,htmlDescription,image)', 'products(productCode,productName,productLine,productScale,productVendor,productDescription,quantityInStock,buyPrice,MSRP)']

#write SQL query to get all the countries of the customers

#"""

#start_phrase3 = """### MySQL tables, with their properties:
##customers(customerNumber,customerName,contactLastName,contactFirstName,phone,addressLine1,addressLine2,city,state,postalCode,country,salesRepEmployeeNumber,creditLimit)
#employees(employeeNumber,lastName,firstName,extension,email,officeCode,reportsTo,jobTitle)
#offices(officeCode,city,phone,addressLine1,addressLine2,state,country,postalCode,territory)
#orderdetails(orderNumber,productCode,quantityOrdered,priceEach,orderLineNumber)
#orders(orderNumber,orderDate,requiredDate,shippedDate,status,comments,customerNumber)
#payments(customerNumber,checkNumber,paymentDate,amount)', 'productlines(productLine,textDescription,htmlDescription,image)
#products(productCode,productName,productLine,productScale,productVendor,productDescription,quantityInStock,buyPrice,MSRP)
####A query get all the cities of the employees, offices and customers, without duplicates.
#"""

#if __name__ == '__main__':
#    get_response(start_phrase2)