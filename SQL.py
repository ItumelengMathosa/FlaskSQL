"""   if request.method == 'POST':

        #Collect entered form data from "signup.html"
        name = request.form.get("username")
        password = request.form.get("password")
        role = "student"

        # Create MySQL cursor
        cursor = db.connection.cursor()

        # Execute the query to insert data
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (name, password, role))

        db.connection.commit()
        cursor.close()"""