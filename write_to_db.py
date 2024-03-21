import psycopg2

def save_to_postgresql(item):
    postgresql_settings = {
            'host': 'localhost',
            'port': 5432,
            'database': 'bids',
            'user': 'postgres',
            'password': 'postgres'
            }
    connection = psycopg2.connect(**postgresql_settings)
    cursor = connection.cursor()
    insert_query = "INSERT INTO bids VALUES (%s, %s, ...)"
    values = (
                item['Bid No'],
                item['Ra No'],
                item['Items'],
                item['Quantity'],
                item['Department'],
                item['Start date'],
                item['End date'],
                item['doclink']
            )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

if __name__=="__main__":
    bid = {"Bid No": "", "Ra No": ["GEM/2022/B/2823092"], "Items": "Cleaning, Sanitation and Disin", "Quantity": [49747], "Department": ["Mechanical"], "Start date": "", "End date": "", "doclink": ""},
    save_to_postgresql(bid)
