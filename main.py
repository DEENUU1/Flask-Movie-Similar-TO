from similar_movies import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="192.168.8.102", port=5000)