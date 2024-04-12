this is a data generater package can be accessible using 


from gen_data import generate_syn_data, save_data

prompt = "Once upon a time, there was a magical kingdom where"
data_type = input("Enter the data type ('text' or 'research'): ")
file_name = input("Enter the file name: ")

synthetic_data = generate_syn_data(prompt, data_type, max_length=200, num_samples=3)
save_data(synthetic_data, data_type, file_name)
