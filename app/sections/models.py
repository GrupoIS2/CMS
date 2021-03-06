from app import db


class Sections(db.Model):

    __tablename__ = 'cms_sections'

    id = db.Column('id', db.Integer, primary_key=True,
                   autoincrement='ignore_fk')
    section_name = db.Column(db.String(128),  nullable=False)
    description = db.Column(db.String(128),  nullable=True)

    def __init__(self, section_, description_):

        self.section_name = section_.title()
        self.description = description_

    def __repr__(self):
        return '<Sections %r>' % (self.section_name)
