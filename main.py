import streamlit as st
import pandas as pd
import mysql.connector

# Function to create a database connection
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo"
    )
    return conn

# Function to create a table to store tasks if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task TEXT NOT NULL,
        status ENUM('ToDo', 'Doing', 'Done') NOT NULL,
        due_date DATE NOT NULL
    );
    '''
    cursor.execute(query)
    conn.commit()

# Function to add a task to the database
def add_task(conn, task, status, due_date):
    cursor = conn.cursor()
    query = "INSERT INTO tasks (task, status, due_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (task, status, due_date))
    conn.commit()

# Function to retrieve tasks from the database
def retrieve_tasks(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    tasks = cursor.fetchall()
    return tasks

def main():
    conn = create_connection()
    create_table(conn)

    st.title("My Todo App")
    menu=["Create","Read","Update","Delete","About"]
    choice= st.sidebar.selectbox("Menu",menu)

    if choice == "Create":
        st.subheader("Add Item")

        col1,col2 =st.columns(2)

        with col1:
            task=st.text_area("Task to do")
        with col2:
            task_status=st.selectbox("status",["ToDo","Doing","Done"])
            task_due_date=st.date_input("Due Date")
        if st.button("Add"):
            due_date_str = task_due_date.strftime('%Y-%m-%d')
            add_task(conn, task, task_status, due_date_str)
            st.success("Added Successfully: {}".format(task))
    
    elif choice == "Read":
        st.subheader("View Task Details")
        tasks = retrieve_tasks(conn)
        if tasks:
            df = pd.DataFrame(tasks, columns=["ID", "Task", "Status", "Due Date"])
            st.dataframe(df)

    elif choice == "Update":
        st.subheader("Edit and Update")

        # Retrieve tasks from the database
        tasks = retrieve_tasks(conn)

        if tasks:
            # Display tasks in a DataFrame
            df = pd.DataFrame(tasks, columns=["ID", "Task", "Status", "Due Date"])

            # Display tasks in a selectable list
            selected_task = st.selectbox("Select Task to Edit", df["Task"])

            # Retrieve task details
            selected_task_details = df[df["Task"] == selected_task].iloc[0]

            # Display current details of the selected task
            st.write("Current Task Details:")
            st.write("ID:", selected_task_details["ID"])
            st.write("Task:", selected_task_details["Task"])
            st.write("Status:", selected_task_details["Status"])
            st.write("Due Date:", selected_task_details["Due Date"])

            # Allow user to edit task details
            st.subheader("Edit Task Details")
            edited_task = st.text_area("Edit Task", selected_task_details["Task"])
            edited_status = st.selectbox("Edit Status", ["ToDo", "Doing", "Done"], index=["ToDo", "Doing", "Done"].index(selected_task_details["Status"]))
            edited_due_date = st.date_input("Edit Due Date", selected_task_details["Due Date"])

            # Update task in the database if "Update" button is clicked
            if st.button("Update"):
                edited_due_date_str = edited_due_date.strftime('%Y-%m-%d')
                # Update task in the database
                cursor = conn.cursor()
                query = "UPDATE tasks SET task = %s, status = %s, due_date = %s WHERE id = %s"
                cursor.execute(query, (edited_task, edited_status, edited_due_date_str, selected_task_details["ID"]))
                conn.commit()
                st.success("Task Updated Successfully!")

    elif choice == "Delete":
        st.subheader("Delete")
    
    else:
        st.subheader("About")

if __name__=='__main__':
    main()
