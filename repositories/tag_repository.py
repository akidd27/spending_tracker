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

#read active/inactive tags
def select_active(active=True):
    #create empty tags list
    active_tags = []

    #sql query and values
    sql = "SELECT * FROM tags WHERE active = %s"
    values = [active]
    results = run_sql(sql, values)

    #create Tag object for each result row and append to list
    for row in results:
        tag = Tag(row['name'], row['active'], row['id'])
        active_tags.append(tag)
    
    return active_tags

#check if tag already exists with given name
#returns True if already exists else False
def check_by_name(name):
    sql = "SELECT 1 FROM tags WHERE name = %s"
    values = [name]
    result = run_sql(sql, values)
    if result:
        return True
    else:
        return False

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