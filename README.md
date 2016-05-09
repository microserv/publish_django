# Publish module for CMS microservice.
# Django version.



## Publishing microservise API documentation.

The fields: article, title, tags, and description are all text fields.
Their content does not matter to, and is not checked by, the publishing microservise.

The id field is a 24 character long lowercase hex string.
It is stored as a text field.


### save article

request:
A POST request to /save_article

input:
The request body should contain a JSON object with the data from the editor.
It should atleast contain the fields: article, title, tags, description.

Effect:
The supplied article should be inserted into the article database.
It should attempt to update the indexer.

Success condition:
If the article was inserted into the database.

return:
If the request was successful:
An Http response with status code 204.

If the request was unsuccessful:
An Http response with status code 500.


### list

request:
A GET request to /list

Effect:
None.

Success condition:
If a list of the articles in the database was generated and returned. 

return:
If the request was successful:
A JSON object containing a field "list" that is a list with JSON objects,
each should have the fields: title, description, id.

If the request was unsuccessful:
An Http response with status code 500.


### article

request:
A GET request to /article/<id>

input:
None.

Effect:
None.

Success condition:
If the article was found, turn into a valid html file, and returned.

return:
If the request was successful:
An html page with the article.

If the request was unsuccessful:
An Http response with status code 500.


### article json

request:
A GET request to /article_json/<id>

input:
None.

Effect:
None.

Success condition:
If the article JSON object was found and returned.

return:
If the request was successful:
A JSON object with the fields: title, description, article, tags.

If the request was unsuccessful:
An Http response with status code 500.


### delete article

request:
A DELETE request to /article_json/<id>

input:
None.

Effect:
The requested article should be deleted from the article database.
It should attempt to update the indexer.

Success condition:
If the article was deleted from the database.

return:
If the request was successful:
An Http response with status code 204.

If the request was unsuccessful:
An Http response with status code 500.