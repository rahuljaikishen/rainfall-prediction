from common.db import write_data

q1 = """
CREATE TABLE IF NOT EXISTS public.rainfall_test_data
(
    created_on date,
    file_location character varying,
    id SERIAL PRIMARY KEY,
    processed integer

);
CREATE TABLE IF NOT EXISTS public.rainfall_predicted_value
(
    id SERIAL PRIMARY KEY,
    date date,
    prediction float,
    active boolean
    
    
);"""

res = write_data(q1)

