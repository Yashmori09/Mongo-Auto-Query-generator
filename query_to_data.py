from base import MongoDB
from model import OpenAi
import re


class retrieve(OpenAi,MongoDB):
    def __init__(self) -> None:
        super().__init__()
        
    
    def query_data(self,query):
        match = re.search(r'```([^`]*)```', query, re.DOTALL)
        modified_query_string = re.sub(r'([$a-zA-Z_][\w$]*)(?=:)', r"'\1'",match.group(1))
     
        result =re.sub(r"(?s).*?\b(db.*)", r"\1", modified_query_string)

        
        final_query='self.'+ result
        # print(final_query)
        despace=final_query.replace(" ","")
        # print(despace)
        data=list(eval(despace))
        return data

# if __name__=='__main__':
#     obj=retrieve()
#     obj.query_data()