from similar_movies import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)