import pandas
import json
import math
import os
from jinja2 import Template
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 2000)
pandas.set_option('display.max_colwidth', 100)
pandas.set_option('display.colheader_justify', 'center')
pandas.set_option('display.precision', 3)
class schema_converter:
    def __init__(self,file_location):
        try:
            self.data_frame=pandas.read_csv(file_location)
        except:
            try:
                self.data_frame=pandas.read_excel(file_location)
            except:
                raise ("File is not in CSV or Excel Readable format")
    def json_ld(self):
        json_data_frame=self.data_frame[1:]
        column_name=self.data_frame.iloc[0].tolist()
        json_data_frame.columns=column_name
        type=json_data_frame['Type'].tolist()
        uri=json_data_frame['URI'].tolist()
        full_uri=json_data_frame['Full URI'].tolist()
        label=[str(i).replace("\"","").replace("\'","") for i in json_data_frame['Label'].tolist()]
        definition=[str(i).replace("\"","").replace("\'","") for i in json_data_frame['Definition'].tolist()]
        comment=[str(i).replace("\"","").replace("\'","") for i in  json_data_frame['Comment'].tolist()]
        usage_note=json_data_frame['Usage Note'].tolist()
        term_status=json_data_frame['Term Status'].tolist()
        # equivalent_term=[str(i).replace("nan","") for i in json_data_frame['Equivalent Term'].tolist()]
        equivalent_term=json_data_frame['Equivalent Term'].tolist()
        sub_term=json_data_frame['SubTerm Of'].tolist()
        domain_schema=json_data_frame["Domain / Scheme"].tolist()
        range=json_data_frame["Range"].tolist()
        target_concept_scheme=json_data_frame["Target Concept Scheme"].tolist()
        top_concept_of=json_data_frame["Top Concept Of"].tolist()
        properties=json_data_frame["Has Properties"].tolist()
        properties=[str(i).split("\n") for i in properties]
        has_top_concept=json_data_frame["Has Top Concept"].tolist()
        has_concept=json_data_frame["Has Concept"].tolist()
        length=len(type)
        t=Template(

            "{\"@context\":\"http://credreg.net/ctdl/schema/context/json\", \"@graph\":[{% for i in range(length) %}{\"@type\":\"{{type[i]}}\",\"@id\":\"{{uri[i]}}\", \"rdfs:label\":{\"en-US\":\"{{label[i]}}\"}, \"rdfs:comment\":{\"en-US\":\"{{definition[i]}}\"},\"dct:description\":{\"en-US\":\"{{comment[i]}}\"},\"vs:term_status\":\"{{term_status[i]}}\",\"meta:changeHistory\":\"fill in later\",\"owl:equivalentClass\":[\"{{equivalent_term[i]}}\"],\"meta:domainfor\":{{properties[i]}}} {% if not loop.last %}, {% endif %} {% endfor %}]}")

        a=t.render(type=type,uri=uri,label=label,comment=comment,definition=definition,term_status=term_status,equivalent_term=equivalent_term,length=length,properties=properties)
        a=a.replace("\'","\"")
        print(a)
        a=json.loads(a,strict=False)
        a=json.dumps(a,indent=4)

        f=open("test.json","w")
        f.write(a)
        f.close()
