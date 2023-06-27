from base import MongoDB
from model import OpenAi
import re


class retrieve(OpenAi,MongoDB):
    def __init__(self) -> None:
        super().__init__()
        
    
    def query_data(self,query):
        modified_query=query.replace('```','')
        despaced_query=modified_query.replace(' ','')
        modified_query_string = re.sub(r'([$a-zA-Z_][\w$]*)(?=:)', r"'\1'", despaced_query)
        final_query='self.'+ modified_query_string
        data=list(eval(final_query))
        return data

# if __name__=='__main__':
#     obj=retrieve()
#     obj.query_data()