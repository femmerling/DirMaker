from app import db


class Contacts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50))
	last_name = db.Column(db.String(50))
	middle_name = db.Column(db.String(50))
	managed_contact = db.Column(db.Integer)
	user_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	addressbook_id = db.Column(db.Integer)
	details = db.relationship("Contact_Details",backref='contacts',lazy='dynamic')

class Contact_Details(db.Model):
	__tablename__ = "contact_details"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	content_type = db.Column(db.String(50))
	value = db.Column(db.String(500))
	contact_id = db.Column(db.Integer,db.ForeignKey('contacts.id'))

	def dto(self):
		return dict(
			id=self.id,
			name=self.name,
			content_type = self.content_type,
			value=self.value,
			contact_id = self.contact_id
			)

class Directory_Mappings(db.Model):
	__tablename__ = "directory_mappings"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	directory_id = db.Column(db.Integer)
	status = db.Column(db.Integer)
	contact_id = db.Column(db.Integer)

class Directories(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.String(50))
	user_id = db.Column(db.Integer)
	parent_id = db.Column(db.Integer)
	icon = db.Column(db.String(100),default=None)
	root_id = db.Column(db.Integer)


	# data transfer object to form JSON
	def dto(self):
		return dict(
				id = self.id,
				name = self.name,
				description = self.description,
				user_id = self.user_id,
				parent_id = self.parent_id,
				root_id = self.root_id)
