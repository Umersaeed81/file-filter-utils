from file_filter import get_filtered_files

reference_folder = r"D:/TXN/Pure_TNL"
candidate_folder = r"D:/LTE/KPIs"

filtered = get_filtered_files(
    reference_folder,
    candidate_folder
)

print(filtered)
