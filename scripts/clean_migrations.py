import os
import shutil

def clean_versions():
    # Lấy đường dẫn tuyệt đối đến thư mục versions
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    versions_dir = os.path.join(current_dir, 'alembic', 'versions')
    
    print(f"Checking: {versions_dir}")
    
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        print("Created versions directory.")
        return

    # Xóa toàn bộ nội dung trong thư mục versions (trừ __init__.py nếu có)
    for item in os.listdir(versions_dir):
        if item == '__init__.py':
            continue
        item_path = os.path.join(versions_dir, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item}")
        except Exception as e:
            print(f"Error removing {item}: {e}")
            
    print("Cleanup successful. Directory is ready.")

if __name__ == "__main__":
    clean_versions()
