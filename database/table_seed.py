import db_connection

db_con = db_connection.db_con
cursor = db_con.cursor()

table_seed_queries = [
    """
    CREATE TABLE IF NOT EXISTS rack (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(250) UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(250) UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(250) NOT NULL,
        stock INT NOT NULL DEFAULT 0,
        rack_id INT,
        category_id INT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (rack_id) REFERENCES rack(id) ON DELETE SET NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
    );
    """,
    """
        create table if not exists access_logs (
            id int auto_increment primary key,
            client_ip int not null,
            client_hostname varchar(250) not null,
            action_performed varchar(250) not null,
            created_at timestamp not null
        )    
    """
]

for query in table_seed_queries:
    cursor.execute(query)

db_con.commit()
cursor.close()
db_con.close()