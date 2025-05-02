# import tkinter as tk

# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Game Menu")
# root.configure(bg="black")

# # Tạo danh sách các button
# buttons = [
#     "UNDO MOVE", "UNDO MOVE",
#     "RESET MAZE", "RESET MAZE",
#     "OPTIONS", "OPTIONS",
#     "WORLD MAP", "WORLD MAP", "WORLD MAP",
#     "QUIT TO MAIN", "QUIT TO MAIN"
# ]

# # Tạo và hiển thị các button
# for text in buttons:
#     btn = tk.Button(root, text=text, font=("Arial", 14, "bold"), fg="yellow", bg="brown", relief="ridge", width=20, height=2)
#     btn.pack(pady=2)

# # Chạy ứng dụng
# root.mainloop()


# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = ""

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "johnsmith88/heart-disease-dataset",
  file_path,
  # Provide any additional arguments like 
  # sql_query or pandas_kwargs. See the 
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

print("First 5 records:", df.head())