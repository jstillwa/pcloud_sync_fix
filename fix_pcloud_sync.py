import sqlite3
import os
import time

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
            cleanup_and_close(conn)
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
            cleanup_and_close(conn)

def cleanup_and_close(conn):
    """
    Properly clean up SQLite WAL files by forcing a checkpoint and optionally
    changing the journal mode before closing the connection.
    """
    try:
        cursor = conn.cursor()
        
        # Get current journal mode
        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]
        print(f"Current journal mode: {journal_mode}")
        
        # Force a checkpoint to ensure all WAL data is written to the main database file
        cursor.execute("PRAGMA wal_checkpoint(FULL);")
        checkpoint_result = cursor.fetchone()
        print(f"Checkpoint result: {checkpoint_result}")
        
        # Optionally switch journal mode to DELETE to remove WAL files
        # Uncomment the next line if you want to completely remove WAL files
        # cursor.execute("PRAGMA journal_mode = DELETE;")
        
        # Close the connection
        conn.close()
        
        # Check if WAL files still exist and wait for them to be cleaned up
        wal_file = f"{conn.database}-wal"
        shm_file = f"{conn.database}-shm"
        
        if os.path.exists(wal_file) or os.path.exists(shm_file):
            print("Waiting for WAL files to be cleaned up...")
            time.sleep(1)  # Give SQLite a moment to clean up
            
            # Check again
            if os.path.exists(wal_file):
                print(f"WAL file still exists: {wal_file}")
            if os.path.exists(shm_file):
                print(f"SHM file still exists: {shm_file}")
        else:
            print("WAL files cleaned up successfully.")
            
    except Exception as e:
        print(f"Error during cleanup: {e}")
        if not conn.closed:
            conn.close()

if __name__ == "__main__":
    import os
    
    # Use the pCloud database in the user's home directory
    home_dir = os.path.expanduser("~")
    pcloud_db_path = os.path.join(home_dir, ".pcloud", "data.db")
    
    if os.path.exists(pcloud_db_path):
        print(f"Using pCloud database at: {pcloud_db_path}")
        fix_sync(pcloud_db_path)
    else:
        print(f"pCloud database not found at: {pcloud_db_path}")
        print("Falling back to local data.db file...")
        fix_sync("data.db")