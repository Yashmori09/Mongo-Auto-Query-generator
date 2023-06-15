from base import MongoDB


class SchemaGen(MongoDB):

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        count = self.db['listingsAndReviews'].count_documents({})
        print(count)

    def fieldname(self, field):
        keys = []
        for doc in field.keys():
            keys.append(doc)

        return keys

    def bson(self, first_item):
        prop = {}
        for i in first_item:
            field_type = type(first_item[i]).__name__
            prop[i] = {"bsonType": field_type}

            if field_type == 'list':
                list_item = first_item[i][0]
                array_type = type(list_item).__name__
                prop[i] = {"bson": field_type,
                           "arrayType": array_type}

                if array_type == 'dict':
                    dict_type = self.nested_schema(first_item[i][0])
                    prop[i] = {"bson": field_type,
                               "arrayType": array_type,
                               "dict_details": dict_type}

            if field_type == 'dict':

                dict_item_type = type(list(first_item[i].values())[0]).__name__

                if dict_item_type == 'dict':
                    nested_schema = self.nested_schema(
                        list(first_item[i].values())[0])
                    prop[i] = {"bson": field_type,
                               "dict_type": dict_item_type,
                               "dict_details": nested_schema}

                else:
                    prop[i] = {"bson": field_type,
                               "dict_type": dict_item_type
                               }

        return prop

    def nested_schema(self, nested_item):
        nested_schema = {}
        nested_schema['dict_required'] = self.fieldname(nested_item)
        nested_schema['dict_properties'] = self.bson(nested_item)
        return nested_schema

    def schema(self):
        final_schema = []
        collection_name = self.db.list_collection_names()
        # i = collection_name[1]
        for i in collection_name:
            schema = {}
            schema['title'] = i
            first_item = self.db[i].find_one()
            field_names = self.fieldname(first_item)
            schema['required'] = field_names
            prop = self.bson(first_item)
            schema['properties'] = prop
            final_schema.append(schema)

        # print(final_schema)
        return final_schema


# if __name__ == '__main__':
#     obj = SchemaGen()
#     resopnse=obj.schema()
#     print(resopnse)
