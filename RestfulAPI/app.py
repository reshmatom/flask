# Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

# Initialize the app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Resource model (e.g., Book or Movie)
class ResourceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)  # For books, use 'author'
    year = db.Column(db.Integer, nullable=False)  # Year for books or movies

# Create the database
with app.app_context():
    db.create_all()

# Resource class with CRUD operations
class ResourceResource(Resource):

    def get(self, resource_id=None):
        if resource_id:
            # Get a specific resource by ID
            resource = ResourceModel.query.get(resource_id)
            if not resource:
                return {'message': 'Resource not found'}, 404
            return jsonify({'id': resource.id, 'title': resource.title, 'author': resource.author, 'year': resource.year})
        else:
            # Get all resources
            resources = ResourceModel.query.all()
            return jsonify([{'id': r.id, 'title': r.title, 'author': r.author, 'year': r.year} for r in resources])

    def post(self):
        # Add a new resource
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        year = data.get('year')

        if not title or not author or not year:
            return {'message': 'Missing required fields'}, 400

        new_resource = ResourceModel(title=title, author=author, year=year)
        db.session.add(new_resource)
        db.session.commit()

        return jsonify({'message': 'Resource added successfully', 'id': new_resource.id})

    def put(self, resource_id):
        # Update a specific resource by ID
        data = request.get_json()
        resource = ResourceModel.query.get(resource_id)

        if not resource:
            return {'message': 'Resource not found'}, 404

        resource.title = data.get('title', resource.title)
        resource.author = data.get('author', resource.author)
        resource.year = data.get('year', resource.year)

        db.session.commit()
        return jsonify({'message': 'Resource updated successfully'})

    def delete(self, resource_id):
        # Delete a specific resource by ID
        resource = ResourceModel.query.get(resource_id)

        if not resource:
            return {'message': 'Resource not found'}, 404

        db.session.delete(resource)
        db.session.commit()
        return jsonify({'message': 'Resource deleted successfully'})

# API routes
api.add_resource(ResourceResource, '/resources', '/resources/<int:resource_id>')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
