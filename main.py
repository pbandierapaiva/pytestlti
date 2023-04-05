from lti import ToolConfig

from typing import Union

from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile

import uuid
import subprocess


app = FastAPI()


@app.get("/lti")
def read_root():
    return HTMLResponse("<h2>Teste</h2>")
    #return Response(content=data, media_type="application/xml")

@app.post("/")
#def read_root():
async def lti_launch(request: Request, 
                     lis_person_contact_email_primary: str = Form(...),
                     resource_link_id: str = Form(...),
                     lis_result_sourcedid: str = Form(...),
                     context_id: str = Form(...),
                     context_title: str = Form(...),
                     lis_outcome_service_url: str = Form(...),
                     lis_person_name_full: str = Form(...)):
    atividadearq = f"atividades/{context_id}.texto"
    enun = open(atividadearq)
    htmlout = enun.read()
    htmlout += f"""{lis_result_sourcedid}<br>
      <h3>Envie o arquivo a ser avaliado</h3>
      <form action="/uploadfile/" method="post" enctype="multipart/form-data">
      <input type="hidden" name="outcome" value={lis_outcome_service_url}>
      <input type="file" name="file">
        <button type="submit">Upload</button>
        </form>"""
    return HTMLResponse(htmlout)
#                    "<h3>Você: " + lis_person_name_full+"</h3>"
#                     +"<h3>e-mail: " + lis_person_contact_email_primary+"</h3>"
#                     +"<h3>context_id: " + context_id+"</h3>")

@app.post("/uploadfile/")
async def create_upload_file(lis_outcome_service_url: str = Form(...),
    file: UploadFile = File(...)):
        contents = await file.read()
        nome = "uploaded_files/" + str(uuid.uuid4())
        with open(nome, "wb") as f:
            f.write(contents)
        f.close()
    
        proc = subprocess.Popen(["python", nome], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output_str, _ = proc.communicate(input="")

        return {"filename": output_str, "lis_outcome_service_url":lis_outcome_service_url }


@app.post("/xx")
#def read_root():
async def lti_launch(request: Request,
                                          oauth_consumer_key: str = Form(...),
                                          oauth_signature_method: str = Form(...),
                                          oauth_signature: str = Form(...),
                                          oauth_timestamp: str = Form(...),
                                          oauth_nonce: str = Form(...),
                                          oauth_version: str = Form(...),
                                          lis_person_name_full: str = Form(...),
                                          lis_person_contact_email_primary: str = Form(...),
                                          lis_outcome_service_url: str = Form(...),
                                          lis_result_sourcedid: str = Form(...),
                                          resource_link_id: str = Form(...),
                                          context_id: str = Form(...),
                                          context_title: str = Form(...),
                                          **kwargs):
    # basic stuff
    app_title = 'My App'
    app_description = 'An example LTI App'
    launch_view_name = 'lti_launch'
    launch_url = "request.build_absolute_uri(reverse('lti_launch'))"

    lti_tool_config = ToolConfig(
        title=app_title,
        launch_url=launch_url,
        secure_launch_url=launch_url,
        #extensions=extensions,
        description = app_description
    )
   # return Response( content= lti_tool_config.to_xml(),media_type="application/xml")
    #return {"Hello": "World"}
    return HTMLResponse(f"""
                                <html>
                                    <head>
                                        <title>LTI Launch</title>
                                    </head>
                                    <body>
                                        <h1>Hello {lis_person_name_full}!</h1>
                                        <p>Your email is {lis_person_contact_email_primary}</p>
                                        <p>Your outcome service URL is {lis_outcome_service_url}</p>
                                        <p>Your result sourced ID is {lis_result_sourcedid}</p>
                                        <p>Your resource link ID is {resource_link_id}</p>
                                        <p>Your context ID is {context_id}</p>
                                        <p>Your context title is {context_title}</p>
                                    </body>
                                </html>
                            """)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}
