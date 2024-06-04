import pyodbc
import definition

def retrieve_user_info(worker_id):
    try:
        conn = pyodbc.connect(definition.DATABASE)
        cursor = conn.cursor()

        query = f"select WorkerName, Position from [MES_V1].[dbo].[User]where WorkerID =  '{worker_id}'"
        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result  # Return the retrieved user information

    except pyodbc.Error as e:
        print(f"An error occurred while connecting to the database: {str(e)}")
        return None
    
def retrieve_work_order_info(qr_data):
    try:
        conn = pyodbc.connect(definition.DATABASE)
        cursor = conn.cursor()

        query = f"select WorkOrder, JobOrder, PartNumber, CycleTime from [MES_V1].[dbo].[WorkOrder] where WorkOrder ='{qr_data}'"
        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result  # Return the retrieved user information

    except pyodbc.Error as e:
        print(f"An error occurred while connecting to the database: {str(e)}")
        return None
   
def insert_rfid_workorder_info(WorkOrder, JobOrder, PartNumber, CycleTime, Status, RFID, terminal, worker_id ):
    try:
        conn = pyodbc.connect(definition.DATABASE)
        cursor = conn.cursor()

        query = f"""DECLARE @Terminal NVARCHAR(50)
                  DECLARE @InputBy NVARCHAR(50)
                  SELECT @Terminal = Terminal FROM [MES_V1].[dbo].[Station] WHERE ID = '{terminal}'
                  SELECT @InputBy = WorkerName FROM [MES_V1].[dbo].[User] WHERE WorkerID = '{worker_id}'
                  insert into [MES_V1].[dbo].[RFID_Process] (WorkOrder, JobOrder, PartNumber, CycleTime, Status, RFID, Terminal, InputBy, InputTime )
                  values('{WorkOrder}', 
                  '{JobOrder}', 
                  '{PartNumber}', 
                  '{CycleTime}', 
                  '{Status}',
                  '{RFID}', 
                  @Terminal, 
                  @InputBy,
                  GETDATE())"""
                  
        cursor.execute(query)
        cursor.commit()

        cursor.close()
        conn.close()

        return True  # Indicate successful insertion

    except pyodbc.Error as e:
        print(f"An error occurred while connecting to the database: {str(e)}")
        return None
    