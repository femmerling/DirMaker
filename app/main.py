# do not change or move the following lines if you still want to use the box.py auto generator
from app import app, db
from models import Contacts, Contact_Details, Directory_Mappings, Directories

# you can freely change the lines below
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response
import logging
from helpers import generate_key
# define global variables here
import xlrd
from datetime import datetime


def read_rows(input_file):
	workbook = xlrd.open_workbook(file_contents=input_file.read())
	sheet = workbook.sheet_by_index(0)
	rows = [sheet.row_values(rownumber) for rownumber in range(sheet.nrows)]
	return rows

def check_float(inputval):
	try:
		float(inputval)
		return str(int(float(inputval)))
	except ValueError:
		return inputval

# home root controller
@app.route('/')
def index():
	# define your controller here
	directories = Directories.query.all()
	directories = [directory.dto() for directory in directories]
	return render_template('welcome.html',directories=directories)

@app.route('/selection', methods=["GET","POST"])
def selection_control():
	input_file = request.files["file"]
	directories = Directories.query.all()
	directories = [item.dto() for item in directories]
	rows = read_rows(input_file)
	return render_template("addresslate.html",rows = rows,directories=directories)


@app.route('/process',methods=['GET','POST'])
def process_names():
	json_payload = json.loads(request.data)
	define = json_payload["head"]
	rows = json_payload["rows"]
	root_id = int(json_payload["root_id"])
	first_name = None
	last_name = None
	middle_name = None
	heads = []
	keys_idx = len(rows[0])-1
	level1=[]
	level2=[]
	level3=[]
	i = 0
	while i <= keys_idx:
		heads.append(rows[0][str(i)])
		i+=1
	for item in rows[1:]:
		max_idx = len(item) - 1
		j = 0
		details = []
		levels = {}
		while j <= max_idx:

			if define[j] != "ignore":
				detail = {}
				if define[j] == "first_name":
					first_name = item[str(j)]
				elif define[j] == "last_name":
					last_name = item[str(j)]
				elif define[j] == "middle_name":
					middle_name = item[str(j)]
				elif define[j] == "level1":
					if item[str(j)] not in level1:
						level1.append(item[str(j)])
					levels["1"] = item[str(j)]
					if item[str(j)] != "":
						detail["key"] = heads[j]
						if heads[j] == "company":
							detail["content_type"] = "ORG"
						elif heads[j] == "title":
							detail["content_type"] = "TITLE"
						elif heads[j] == "phone":
							detail["content_type"] = "TEL"
						elif heads[j] == "mobile":
							detail["content_type"] = "TEL"
						elif heads[j] == "iphone":
							detail["content_type"] = "TEL"
						elif heads[j] == "fax":
							detail["content_type"] = "TEL"
						elif heads[j] == "email":
							detail["content_type"] = "EMAIL"
						else:
							detail["content_type"] = "text"

						detail["value"] = check_float(item[str(j)])

				elif define[j] == "level2":
					if item[str(j)] not in level2:
						level2.append(item[str(j)])
					levels["2"] = item[str(j)]
					if item[str(j)] != "":
						detail["key"] = heads[j]
						if heads[j] == "company":
							detail["content_type"] = "ORG"
						elif heads[j] == "title":
							detail["content_type"] = "TITLE"
						elif heads[j] == "phone":
							detail["content_type"] = "TEL"
						elif heads[j] == "mobile":
							detail["content_type"] = "TEL"
						elif heads[j] == "iphone":
							detail["content_type"] = "TEL"
						elif heads[j] == "fax":
							detail["content_type"] = "TEL"
						elif heads[j] == "email":
							detail["content_type"] = "EMAIL"
						else:
							detail["content_type"] = "text"
						detail["value"] = check_float(item[str(j)])
				elif define[j] == "level3":
					if item[str(j)] not in level3:
						level3.append(item[str(j)])
					levels["3"] = item[str(j)]
					if item[str(j)] != "":
						detail["key"] = heads[j]
						if heads[j] == "company":
							detail["content_type"] = "ORG"
						elif heads[j] == "title":
							detail["content_type"] = "TITLE"
						elif heads[j] == "phone":
							detail["content_type"] = "TEL"
						elif heads[j] == "mobile":
							detail["content_type"] = "TEL"
						elif heads[j] == "iphone":
							detail["content_type"] = "TEL"
						elif heads[j] == "fax":
							detail["content_type"] = "TEL"
						elif heads[j] == "email":
							detail["content_type"] = "EMAIL"
						else:
							detail["content_type"] = "text"
						detail["value"] = check_float(item[str(j)])
				else:
					if item[str(j)] != "":
						detail["key"] = heads[j]
						if heads[j] == "company":
							detail["content_type"] = "ORG"
						elif heads[j] == "title":
							detail["content_type"] = "TITLE"
						elif heads[j] == "phone":
							detail["content_type"] = "TEL"
						elif heads[j] == "mobile":
							detail["content_type"] = "TEL"
						elif heads[j] == "iphone":
							detail["content_type"] = "TEL"
						elif heads[j] == "fax":
							detail["content_type"] = "TEL"
						elif heads[j] == "email":
							detail["content_type"] = "EMAIL"
						else:
							detail["content_type"] = "text"
						detail["value"] = check_float(item[str(j)])
			if detail:
				details.append(detail)
			j+=1
		contact = Contacts(
							first_name = first_name,
							last_name = last_name,
							middle_name = middle_name,
							managed_contact = 1,
							created_at = datetime.now()
						)
		db.session.add(contact)
		db.session.commit()

		for item in details:
			detail = Contact_Details(
							name = item["key"],
							content_type = item["content_type"],
							value = item["value"],
							contact_id = contact.id
						)
			db.session.add(detail)
		db.session.commit()

		if len(levels) < 2:
			if levels["1"]:
				directory = Directories.query.filter(Directories.name == levels["1"],Directories.root_id == root_id).first()
				if not directory:
					directory = Directories(
									name = levels["1"],
									parent_id = root_id,
									root_id = root_id
								)
					db.session.add(directory)
					db.session.commit()
				mapping = Directory_Mappings(
							directory_id = directory.id,
							contact_id = contact.id,
							status = 0
						)
				db.session.add(mapping)
				db.session.commit()
		else:
			if len(levels) == 2:
				directory = Directories.query.filter(Directories.name == levels["1"],Directories.root_id == root_id).first()
				if not directory:
					directory = Directories(
									name = levels["1"],
									parent_id = root_id,
									root_id = root_id
								)
					db.session.add(directory)
					db.session.commit()
				bottom = Directories.query.filter(Directories.name == levels["2"],Directories.parent_id == directory.id,Directories.root_id == root_id).first()
				if not bottom:
					bottom = Directories(
									name = levels["2"],
									parent_id = directory.id,
									root_id = root_id
								)
					db.session.add(bottom)
					db.session.commit()
				mapping = Directory_Mappings(
							directory_id = bottom.id,
							contact_id = contact.id,
							status = 0
						)
				db.session.add(mapping)
				db.session.commit()
			elif levels["2"] and levels["3"]:
				directory = Directories.query.filter(Directories.name == levels["1"],Directories.root_id == root_id).first()
				if not directory:
					directory = Directories(
									name = levels["1"],
									parent_id = root_id,
									root_id = root_id
								)
					db.session.add(directory)
					db.session.commit()

				parent = Directories.query.filter(Directories.name == levels["2"],Directories.parent_id == directory.id, Directories.root_id == root_id).first()
				if not parent:
					parent = Directories(
									name = levels["2"],
									parent_id = root_id,
									root_id = root_id
								)
					db.session.add(parent)
					db.session.commit()
				bottom = Directories.query.filter(Directories.name == levels["3"],Directories.parent_id == parent.id,Directories.root_id == root_id).first()
				if not bottom:
					bottom = Directories(
									name = levels["3"],
									parent_id = parent.id,
									root_id = root_id
								)
					db.session.add(bottom)
					db.session.commit()
				mapping = Directory_Mappings(
							directory_id = bottom.id,
							contact_id = contact.id,
							status = 0
						)
				db.session.add(mapping)
				db.session.commit()


	return "All contacts uploaded"