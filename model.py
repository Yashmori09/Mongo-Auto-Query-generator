from schema_gen import SchemaGen
import os
import openai
from dotenv import load_dotenv, find_dotenv
from constant import *

class OpenAi(SchemaGen):
    def __init__(self) -> None:
        super().__init__()
        _ = load_dotenv(find_dotenv(OPENAI_ENV)) # read local .env file
        openai.api_key  = os.environ['OPENAI_API_KEY']

    def get_completion(self,messages, model=MODEL):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.5, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    

    # def question_gen(self):
    #     schema=self.schema()
    #     bson=["Double","String","Object","Array","Binary data","ObjectId","Boolean","Date",'Null','Regular Expression','JavaScript','32-bit integer','Timestamp','64-bit integer','Decimal128','Min key','Maxkey']
    #     system=f"""
    #     You are a mongodb expert who gives logically and syntatically correct mongodb query.  
    #     """
    #     information=f"""
    #     The given {schema} represents a MongoDB schema, where 'title' refers to the name of the collection. The 'required' field specifies the necessary columns for the collection, and the 'properties' field defines the names of the columns along with their corresponding BSON types, represented as {bson}.
    #     If the BSON type is 'array', the 'arraytype' field indicates the type of elements present within the array. If the BSON type is 'dict', there are additional fields. These details include the 'dictrequired' field, which lists the required fields within the dictionary, and the 'dictproperties' field, which outlines the types of the fields.
    #     This dictionary structure within the schema acts as a nested schema. The more layers of nested dictionaries there are, the more information it conveys about the data entry.
    #     """
    #     user=f"""
        
    #     You need to create 20 different complex questions which can be answered by mongodb query.
    #     You will be provided by a schema of database and along with some terminology of schema{information}.you have to use all the mongodb functions to generate the complex questions and answer.
    #     the syntax and the logic of the answer to solve the generated  question should be very much perfect. Use all the collections given in schema to generate the questions. 
    #     provide the answer in following format:
    #     Q1:
    #     A1:
    #     where Q1 is the question generated and 
    #     A1 should be the mongodb compass query with proper syntax and logic

    #     """
    #     messages = [
    #         {'role': 'system', 'content': system},
    #         {'role': 'user', 'content': user}
    #     ]

    #     response = self.get_completion(messages)
    #     return response
    
    def user_answer_gen(self,question):
        aggregation_functions = [
    "$addFields",
    "$expr",
    "$add",
    "$and",
    "$arrayElemAt",
    "$arrayToObject",
    "$avg",
    "$bucket",
    "$bucketAuto",
    "$ceil",
    "$cmp",
    "$concat",
    "$cond",
    "$dateFromString",
    "$dateToString",
    "$dayOfMonth",
    "$divide",
    "$eq",
    "$exp",
    "$filter",
    "$first",
    "$floor",
    "$gt",
    "$gte",
    "$ifNull",
    "$in",
    "$indexOfArray",
    "$isArray",
    "$isoWeek",
    "$jsonSchema",
    "$last",
    "$let",
    "$literal",
    "$log",
    "$log10",
    "$lt",
    "$lte",
    "$map",
    "$max",
    "$mergeObjects",
    "$meta",
    "$min",
    "$mod",
    "$month",
    "$multiply",
    "$ne",
    "$not",
    "$or",
    "$pow",
    "$push",
    "$range",
    "$reduce",
    "$replace",
    "$reverseArray",
    "$round",
    "$size",
    "$slice",
    "$sqrt",
    "$stdDevPop",
    "$stdDevSamp",
    "$strcasecmp",
    "$substr",
    "$subtract",
    "$sum",
    "$switch",
    "$toDate",
    "$toLower",
    "$toString",
    "$toUpper",
    "$trunc",
    "$type",
    "$unset",
    "$week",
    "$year",
    "$zip"
]

        schema=self.schema()
        system=f"""
         You are a mongodb expert who gives logically and syntatically correct mongodb query.  
        """
        # info = f"""
        # You are provided with the the question and answer set of the the complex questions and their answers as mongodb query.
        #  and also schema of collection.
        # """
        # user = f""" 
        # {info}
        # Learn the relations between the collections{schema} and the depthness of schema and also the details from the given set of questions{question_set} and answer the given question below in the mongodb query.
        # specially take care of nested schemas and give the detailed query according to schema.
        # your answer should be only mongodb compass query and no extra explanation is needed.Use the given schema keys to generate the query  \n
        # Use Aggregate function.\n
        # Also query should be in triple delimiter(``` ```) \n
        # Question:{question}
        # """
        user = f""" 
        Learn the relations between the collections{schema} and the depthness of schema. Answer the given question below in the mongodb query.
        You can use any of the aggregate function{aggregation_functions} to generate query.Dont use short query and instead use detailed query.Use uppercase 'True' and 'False'.
        your answer should be only mongodb compass query and no extra explanation is needed.Use the given schema keys to generate the query  \n
        Use Aggregate function.\n
        
        Also query should be in triple delimiter(``` ```) \n
        Question:{question}
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