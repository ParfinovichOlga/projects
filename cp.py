from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contracts_projects.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    creation_date = db.Column(db.Date(), default=date.today())
    signing_date = db.Column(db.Date())
    status = db.Column(db.String(25), default='draft', nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def create_contract(self, contract_name):
        if contract_name == "":
            return "Please, enter a contract name"
        else:
            with app.app_context():
                new_contract = Contract(
                    name=contract_name,
                    creation_date=date.today(),
                    status='draft',
                    signing_date=None
                )
                try:
                    db.session.add(new_contract)
                    db.session.commit()
                    return "The contract successfully created"
                except IntegrityError:
                    return "Such contract's name already exists"


    def confirm_contract(self, contract_to_confirm):
        with app.app_context():
            contract_to_change = db.session.execute(db.select(Contract).where(Contract.name == contract_to_confirm))\
                .scalar()
            if contract_to_change is None:
                print("Such contract doesn't exist")
            else:
                contract_to_change.status = 'active'
                contract_to_change.signing_date = date.today()
                db.session.commit()

    def complete_contract(self, contract_to_complete):
        with app.app_context():
            contract_to_complete = db.session.execute(
                db.select(Contract).where(Contract.name == contract_to_complete)).scalar()
            if contract_to_complete is not None:
                contract_to_complete.status = 'completed'
                db.session.commit()
            else:
                print("Such contract doesn't exist")

    def get_all_contracts(self):
        with app.app_context():
            results = db.session.execute(db.select(Contract).order_by(Contract.id)).scalars()
            all_contracts = [{'id': result.id,
                              'name': result.name,
                              'creation_date': str(result.creation_date).split(")")[0],
                              'signing_date': str(result.signing_date).split(")")[0],
                              'status': result.status,
                              'project_id': result.project_id} for result in results]
            return all_contracts


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    creation_date = db.Column(db.Date(), default=date.today())
    contracts = db.relationship("Contract", backref='project')

    def create_project(self, project_name):
        all_contracts = Contract.get_all_contracts(self)
        if all_contracts:
            if project_name == "":
                return "Please, enter a project name"
            else:
                with app.app_context():
                    new_project = Project(
                            name=project_name,
                            creation_date=date.today()
                        )
                    try:
                        db.session.add(new_project)
                        db.session.commit()
                        return "The project successfully created"
                    except IntegrityError:
                        return "Such project already exists"
        else:
            return "Please, previously add a contract"

    def get_all_projects(self):
        with app.app_context():
            result = db.session.execute(db.select(Project).order_by(Project.id)).scalars()
            all_projects = [{'id': project.id,
                             'name': project.name,
                             'creation_date': str(project.creation_date).split(")")[0],
                             'contracts': project.contracts} for project in result]
            return all_projects

    def add_contract(self, project_name, contract_name):
        with app.app_context():
            project_to_change = db.session.execute(db.select(Project).where(Project.name == project_name)).scalar()
            if project_to_change is not None:
                contract_selected = db.session.execute(
                    db.select(Contract).where(Contract.name == contract_name)).scalar()
                if contract_selected is None:
                    return "Such contract doesn't exist"

                else:
                    if contract_selected.status == "active":
                        statuses = [pr.status for pr in project_to_change.contracts]
                        if 'active' in statuses:
                            return "You can use only 1 active contract"
                        else:
                            all_projects = self.get_all_projects()
                            contracts_using = [pr['contracts'] for pr in all_projects]
                            contracts_id = []
                            for element in contracts_using:
                                for n in element:
                                    contracts_id.append(n.id)
                            if contract_selected.id in contracts_id:
                                return "You can't use contract more than for one project"
                            else:
                                contract_selected.project_id = project_to_change.id
                                db.session.commit()
                                return "The Contract was added to the Project"

                    else:
                        return 'You can choose active contract only'


    def close_contract(self, project_name):
        with app.app_context():
            project_to_close = db.session.execute(
                db.select(Project).where(Project.name == project_name)).scalar()
            if project_to_close is not None:
                if project_to_close.contracts:
                    for element in project_to_close.contracts:
                        if element.status == "active":
                            element.status = "completed"
                            db.session.commit()
                            return f"The {element.name} completed"
            else:
                return "The contract doesn't exist"


with app.app_context():
    db.create_all()










