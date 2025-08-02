import sqlite3

def fix_sync(db_path):
    """
    Fixes a stuck pCloud sync by moving the first problematic folder creation
    task to the end of the task queue.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Find the ID of the first stuck folder creation task
        cursor.execute("SELECT MIN(id) FROM fstask WHERE type = 3 AND status = 2")
        result = cursor.fetchone()

        if not result or result[0] is None:
            print("No stuck folder creation tasks found.")
            conn.close()
            return

        stuck_task_id = result[0]
        print(f"Found stuck task with ID: {stuck_task_id}")

        # Find the maximum ID in the fstask table
        cursor.execute("SELECT MAX(id) FROM fstask")
        max_id = cursor.fetchone()[0]
        new_task_id = max_id + 1
        print(f"Current maximum task ID is: {max_id}. New ID will be: {new_task_id}")

        # Move the stuck task to the end of the queue
        print(f"Moving task {stuck_task_id} to the end of the queue (ID: {new_task_id})...")
        cursor.execute("UPDATE fstask SET id = ? WHERE id = ?", (new_task_id, stuck_task_id))
        conn.commit()

        print("Task moved successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_sync("data.db")