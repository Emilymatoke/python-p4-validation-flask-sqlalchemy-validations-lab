from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Author name should not be empty.")
        existing_author = Author.query.filter(name == name).first()
        if existing_author:
            raise ValueError("Author name should be unique")
        return name
        
    @validates('phone_number')    
    def validate_phone_number(self, key,phone_number):
        if not phone_number.isdigit():
            raise ValueError("Phone number should contain only digits.")
        
        if len(phone_number) != 10:
            raise ValueError("Phone number should be exactly ten digits long.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Content must not be empty.")
        elif len(content) < 250:
            raise ValueError("Content length must be at least 250 characters.")
        return content

    
    @validates('summary')
    def validate_summary(self,key,summary):
        if summary and len(summary) > 250:
            raise ValueError("sumarry should be at most 250 characters long")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category should be either 'Fiction' or 'Non-Fiction'.")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        
        click_baits = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in click_baits):
            raise ValueError("Title should contain either 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title
        
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'