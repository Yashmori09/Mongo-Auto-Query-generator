from h2o_wave import main, app, Q, ui
from model import OpenAi
from query_to_data import retrieve
import pandas as pd


obj=OpenAi()
questions=obj.question_gen()
datafrm=retrieve()

@app('/')
async def serve(q: Q):
    intitial_state(q,questions)
    await q.page.save()


def intitial_state(q,questions):
    q.page['meta'] = ui.meta_card(
        box='',
        layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header'),
                    ui.zone('search'),
                    ui.zone('query'),
                    ui.zone('table')

                ]

            )
        ]
    )
    q.page['header'] = ui.header_card(
        box='header',
        title='Mongo X',
        subtitle='MongoD Helper'
    )
    q.page['search'] = ui.form_card(
        box='search',
        items=[
            ui.textbox(name='SearchBox',
                       label='Search'),
            ui.button(name='search_button', label='Search')

        ]

    )
    if q.args.search_button:
        q.page['query'] = ui.form_card(
            box='query',
            items=[ui.text(q.args.SearchBox)]
            
        )
        query=obj.user_answer_gen(questions,q.args.SearchBox)
        df= dataframe(query)
        
        q.page['table_view']=ui.form_card(
            box='table',
            items=[
                ui.text_xl("Table View"),
                ui.table(
                    name='data_table',
                    columns=[ui.table_column(name=col,label=col)for col in df.columns.values],
                    rows=[
                        ui.table_row(
                            name=str(i),
                            cells=[str(df[col].values[i])for col in df.columns.values]
                        ) for i in range(len(df))
                    ]
                )
            ]
        )
        

def dataframe(query):
    answer=datafrm.query_data(query)
    df=pd.DataFrame(answer)

    return df






