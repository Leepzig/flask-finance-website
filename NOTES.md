## Incorrect Query with injection dangers
        cur.execute(f"""
        INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
        VALUES('{record['transaction_date']}'::date,'{record['posted_date']}'::date,{record['card_number']},'{record['description']}','{record['category']}',{record['debited_amount']},{record['credited_amount']})
        """)

## Correct Way to Avoid sql injection
        cur.execute("""
            INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
            VALUES(%(transaction_date)s::date, %(posted_date)s::date, %(card_number)s, %(description)s, %(category)s, %(debited_amount)s, %(credited_amount)s);
            """, (record['transaction_date'], record['posted_date'], record['card_number'], record['description'], record['category'], record['debited_amount'], record['credited_amount']))

## Did not transform to dictionary, instead called tuple indices
        cur.execute("""
            INSERT INTO transactions (transaction_date, posted_date, card_number, description, category, debited_amount, credited_amount)
            VALUES(%(transaction_date)s, %(posted_date)s, %(credited_amount)s, %(card_number)s, %(description)s, %(category)s, %(debited_amount)s, %(credited_amount)s);
            """, (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))


## Use this link to rework the insert logic:
- https://www.tutorialspoint.com/python_data_access/python_postgresql_where_clause.htm

def get_obj(row):
    keys = ['transaction_date', 'posted_date', 'card_number', 'description', 'category', 'debited_amount', 'credited_amount']
    obj = {}
    for index in range(len(row)):
        if row[index] == "":
            obj[keys[index]] = 0
        elif 'date' in keys[index]:
            obj[keys[index]] = convert_date(row[index])
        else:
            obj[keys[index]] = row[index]
    return obj

DONE
# View different Tables
### Input a Calendar where you can select dates DONE
### a submit button should send the dates to the backend DONE
### the dates should get passed to the database DONE
### the backend should respond with a new table DONE

# Enable csv upload
### Make upload input DONE
### MAke location for the upload files to get stored DONE
### trigger an automated process to upload the data to the database DONE
### Return the data? Return what? at least a confirmation message. DONE
### Put a timestamp of when the data was uploaded and we can query for the data like that. DONE
https://stackoverflow.com/questions/38245025/how-to-insert-current-datetime-in-postgresql-insert-query


