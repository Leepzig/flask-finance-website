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