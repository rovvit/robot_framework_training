*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}     http://localhost:8000

*** Test Cases ***
Get_items
    Create Session    my_session    ${base_url}
    ${response}=    GET On Session    my_session  /items

    #VALIDATIONS
    ${status_code}=    Set variable    ${response.status_code}
    Should be equal as integers    ${status_code}   200

    ${body}=    Set variable    ${response.content}
    Should contain    ${body}   count

    ${contentTypeValue}=    Get from dictionary    ${response.headers}     content-type
    Should be equal    ${contentTypeValue}      application/json