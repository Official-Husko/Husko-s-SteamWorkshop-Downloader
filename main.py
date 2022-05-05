from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

"""    <script defer src="{{ url_for('static', filename='theme.js') }}"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />"""