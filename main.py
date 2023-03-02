from similar_movies import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="172.20.10.4", port=5000)