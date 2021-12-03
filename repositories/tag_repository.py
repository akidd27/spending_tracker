from db.run_sql import run_sql
from models.tag import Tag

#similar to merchant repository

#create
def save(tag):
    #sql query and values
    sql = "INSERT INTO tags (name, active) VALUES (%s, %s) RETURNING id"
    values = [tag.name, tag.active]

    #save tag to db, get id and save it to Tag object
    results = run_sql(sql, values)
    tag.id = results[0]['id']
    return tag

#read all
def select_all():
    #create empty tags list
    tags = []

    #sql query
    sql = "SELECT * FROM tags"
    results = run_sql(sql)

    #create tag object for each row in results and append to list
    for row in results:
        tag = Tag(row['name'], row['active'], row['id'])
        tags.append(tag)
    return tags

#read by id
def select(id):
    tag = None

    #sql query and id value
    sql = "SELECT * FROM tags WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    #if exists, return tag object from query result
    if result is not None:
        tag = Tag(result['name'], result['active'], result['id'])
    return tag

#update tag
def update(tag):
    #sql query and values
    sql = "UPDATE tags SET (name, active) = (%s, %s) WHERE id = %s"
    values = [tag.name, tag.active, tag.id]
    run_sql(sql, values)

#delete all
def delete_all():
    sql = "DELETE  FROM tags"
    run_sql(sql)

#delete by id
def delete(id):
    sql = "DELETE FROM tags WHERE id = %s"
    values = [id]
    run_sql(sql, values)