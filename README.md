# AlternaBrand - Product Alternative Finder

A Python Flask web application that uses deep learning to recognize American products and suggest non-American alternatives.

## Features

- **Camera Recognition**: Use your device camera to scan product labels
- **Text Search**: Search for products by name
- **Alternative Suggestions**: Discover non-American alternatives to popular American products

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Image Processing**: NumPy, Pillow
- **Database**: PostgreSQL (configurable to use SQLite for development)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/alternabrand.git
   cd alternabrand
   ```

2. Install dependencies:
   ```
   pip install -r deployment_requirements.txt
   ```

3. Set environment variables:
   ```
   export DATABASE_URL=your_database_url
   export SESSION_SECRET=your_secret_key
   ```

4. Run the application:
   ```
   gunicorn main:app
   ```

## Project Structure

- `app.py`: Main Flask application and routes
- `main.py`: Entry point for the application
- `models.py`: Database models
- `product_database.py`: Functions for interacting with the product database
- `product_recognition.py`: Product recognition functionality
- `static/`: Static files (CSS, JavaScript, images)
- `templates/`: HTML templates

## Deployment

This application can be deployed on Heroku, AWS, or any platform that supports Python and Flask applications.

## License

This project is licensed under the MIT License - see the LICENSE file for details.