from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.tag import Tag
import repositories.tag_repository as tag_repository

tags_blueprint = Blueprint("tags", __name__)

#show all active tags
@tags_blueprint.route("/tags")
def tags():
    active_tags = tag_repository.select_active()
    return render_template("tags/index.html", title='My Tags', active_tags=active_tags)

#form to create new tag
@tags_blueprint.route("/tags/new")
def new_tag():
    return render_template("/tags/new.html", title="New Tag")

#add new tag and return to /tags
@tags_blueprint.route("/tags", methods=['POST'])
def add_tag():
    name = request.form['name']
    if not tag_repository.check_by_name(name):
        tag = Tag(name)
        tag_repository.save(tag)
        return redirect('/tags')
    else:
        return render_template('/tags/already_exists.html', title="Error", name=name)

#form to edit/delete/deactivate tag
@tags_blueprint.route("/tags/<id>")
def edit_tag(id):
    tag = tag_repository.select(id)
    return render_template('/tags/edit.html', title=tag.name, tag=tag)

#update tag from form data
@tags_blueprint.route("/tags/<id>", methods=['POST'])
def update_tag(id):
    name = request.form['name']
    tag = Tag(name, True, id)
    tag_repository.update(tag)
    return redirect('/tags')

#delete tag
@tags_blueprint.route('/tags/<id>/delete', methods=['POST'])
def delete_tag(id):
    tag_repository.delete(id)
    return redirect('/tags')

#deactivate tag
@tags_blueprint.route('/tags/<id>/deactivate', methods=['POST'])
def deactivate_tag(id):
    tag = tag_repository.select(id)
    tag.active = False
    tag_repository.update(tag)
    return redirect('/tags')

#show deactivated tags
@tags_blueprint.route('/tags/inactive')
def inactive_tags():
    inactive_tags = tag_repository.select_active(False)
    return render_template('/tags/inactive.html', title='Inactive Tags', inactive_tags=inactive_tags)

#activate tag
@tags_blueprint.route('/tags/<id>/activate', methods=['POST'])
def activate_tag(id):
    tag = tag_repository.select(id)
    tag.active = True
    tag_repository.update(tag)
    return redirect('/tags/inactive')
