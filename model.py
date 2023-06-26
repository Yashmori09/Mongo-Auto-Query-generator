from schema_gen import SchemaGen
import os
import openai
from dotenv import load_dotenv, find_dotenv


class OpenAi(SchemaGen):
    def __init__(self) -> None:
        super().__init__()
        _ = load_dotenv(find_dotenv('openai.env')) # read local .env file
        openai.api_key  = os.environ['OPENAI_API_KEY']

    def get_completion(self,messages, model="gpt-3.5-turbo"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.5, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    

    def question_gen(self):
        schema=self.schema()
        bson=["Double","String","Object","Array","Binary data","ObjectId","Boolean","Date",'Null','Regular Expression','JavaScript','32-bit integer','Timestamp','64-bit integer','Decimal128','Min key','Maxkey']
        system=f"""
        You are a mongodb expert. you need to give the answer of the given question in mongodb query and also validate that answer generated by you in such a way that the answer should be logically and syntactically correct.
        """
        information=f"""
        The given {schema} represents a MongoDB schema, where 'title' refers to the name of the collection. The 'required' field specifies the necessary columns for the collection, and the 'properties' field defines the names of the columns along with their corresponding BSON types, represented as {bson}.
        If the BSON type is 'array', the 'arraytype' field indicates the type of elements present within the array. If the BSON type is 'dict', there are additional fields. The 'dicttype' field specifies the type of values contained within the dictionary, while the 'dictdetails' field provides internal details about the dictionary. These details include the 'dictrequired' field, which lists the required fields within the dictionary, and the 'dictproperties' field, which outlines the types of the fields.
        This dictionary structure within the schema acts as a nested schema. The more layers of nested dictionaries there are, the more information it conveys about the data entry.
        """
        user=f"""
        
        You need to create 20 complex questions which can be answered by mongodb query.
        You will be provided by a schema of database and along with some terminology of schema{information}.you have to use all the mongodb functions to generate the complex questions and answer.
        the syntax and the logic of the answer to solve the generated  question should be very much perfect. no error should be found in the answer
        provide the answer in following format:
        Q1:
        A1:
        where Q1 is the question generated and 
        A1 should be the mongodb compass query with proper syntax and logic

        """
        messages = [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user}
        ]

        response = self.get_completion(messages)
        return response
    
    def user_answer_gen(self,question_set,question):
        
        schema=self.schema()
        system=f"""
        You are a mongodb expert. you need to give the answer of the given question in mongodb query and also validate that answer generated by you in such a way that the answer should be logically and syntactically correct.
        """
        info = f"""
        You are provided with the the question and answer set of the the complex questions and their answers as mongodb query.
        {question_set} and also schema of collection{schema} 
        """
        user = f""" 
        {info}
        Learn the relations between the collections and also the details from the given set of questions and answer the given question below in the mongodb query.

        Question:{question}

        your answer should be only mongodb compass query \n
        every words inside the list and dict after 'aggregate' should be in inverted commas(' '))\n
        no extra explanation is needed.\n
        Also dont use triple quotes(''' ''') in answer\n

        """
        messages2 = [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user}
        ]

        response2 = self.get_completion(messages2)
        return response2

# if __name__ == '__main__':
#     obj = OpenAi()
#     question_set=obj.question_gen()
#     print(question_set)
#     question='Find the customer with the lowest number of transactions.'
#     obj.user_answer_gen(question_set,question)