import pymysql

# Connect to SQLite (you can replace this with another database if needed)
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='3nT3R#mysql',
    database='LDSRags',
    port=3307
)
cursor = conn.cursor()

# Function to process the text file
def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = None
    content_lines = []
    for line in lines:
        if "chapter" in line.lower():
            # If there is a current title and content, insert it into the database
            if title:
                insert_into_db(title, "\n".join(content_lines))
                content_lines = []  # Reset content lines for the next chapter

            # Extract the title and author from the current line
            title = line.strip()
        else:
            content_lines.append(line.strip())

    # Insert the last chapter's content
    if title:
        insert_into_db(title, "\n".join(content_lines))


# Function to insert data into the database
def insert_into_db(title, content):
    # Extract the author's name before "chapter"
    author = title.split("Chapter")[0].strip()

    # Insert into the database
    print(title)
    print(author)
    # Insert into the database using parameterized query for pymysql
    try:
        cursor.execute('''
        INSERT INTO Scripture (title, content, author, source, year, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (title, content, author, "book of mormon", 1830, "scripture"))
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")


# Usage
process_file('book_of_mormon.txt')

# Close the connection when done
conn.close()