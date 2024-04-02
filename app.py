import streamlit as st
import boto3
from streamlit_lottie import st_lottie
import requests
import os
import subprocess
import tempfile
import en
def upload_file_to_s3(file_path, bucket_name, access_key, access_secret,tt):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=access_secret)
    s3.upload_file(file_path, bucket_name,tt)
    print("File uploaded successfully!")

def list_virtualbox_vms(vboxmanage_path):
    try:
        # Execute VBoxManage to list VMs
        result = subprocess.run([vboxmanage_path, "list", "vms"], capture_output=True, text=True, check=True)
        vm_list = result.stdout.splitlines()
        return vm_list
    except subprocess.CalledProcessError as e:
        print(f"Error listing VirtualBox VMs: {e}")
        return []

def export_virtualbox_vm(vboxmanage_path, vm_name,local_dir):
    # Specify the export filename
    export_file = vm_name + "1.ova"
    export_path = os.path.join(os.getcwd(), export_file)
    print(f"Exporting '{vm_name}' to '{export_path}'...")

    try:
        # Export the selected VM to the current directory
        subprocess.run([vboxmanage_path, "export", vm_name, "--output", export_path], check=True)
        print(f"Exported '{vm_name}' to '{export_path}' successfully.")
        return export_path  # Return the path to the exported OVA file
    except subprocess.CalledProcessError as e:
        print(f"Error exporting '{vm_name}': {e}")
        return None
# Function to get AWS credentials and S3 details from the user
def get_user_input():
    friend_access_key = ""
    friend_secret_key = ""
    friend_s3_bucket = ""
    friend_vm_image_key = ""
    
    return friend_access_key, friend_secret_key, friend_s3_bucket, friend_vm_image_key
def import_virtualbox_vm(vboxmanage_path, ova_path):
    try:
        # Import the OVA file
        subprocess.run([vboxmanage_path, "import", ova_path], check=True)
        print(f"Imported '{ova_path}' successfully.")
        
        # Get the VM name from the OVA file (without the file extension)
        imported_vm_name = os.path.splitext(os.path.basename(ova_path))[0]
        
        # Unregister and remove the imported VM
        subprocess.run([vboxmanage_path, "unregistervm", imported_vm_name, "--delete"], check=True)
        print(f"Removed '{imported_vm_name}' after import.")
    except subprocess.CalledProcessError as e:
        print(f"Error importing '{ova_path}': {e}")
def download_ova_from_s3(access_key, secret_key, s3_bucket, s3_key, local_directory):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    try:
        s3_client.download_file(s3_bucket, s3_key, local_directory)
        print(f"Downloaded OVA VM image from S3 to {local_directory}")
    except Exception as e:
        print(f"Error downloading OVA VM image: {str(e)}")
        exit(1)
def fetch(access_key, secret_key, s3_bucket):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    keys = []
    try:
        bucket = s3.Bucket(s3_bucket)
        for obj in bucket.objects.all():
            keys.append(obj.key)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return keys
                           
def app(keys):
    friend_access_key, friend_secret_key, friend_s3_bucket, friend_vm_image_key = get_user_input()
    st.title("VM Migration Capston Project")
    tab1,tab2 =st.tabs(["Export","Import"])
    with tab2:
        key = st.selectbox("Select VM",["Select"]+keys)
        if key.endswith(".enc"):
            local_path = rf"C:\Users\dipes\Downloads\final capstron\temp\{key}"
            dec_key = st.text_input("Provide key to decrypt")
            flag = True
        else:
            local_path = rf"C:\Users\dipes\Downloads\final capstron\{key}"
            flag = False
        bt1 = st.button("Import")
        hh = r"C:\Users\dipes\Downloads\final capstron\kalilinux1.ova"
        if bt1:
            with st.spinner("Downloading in progress..."):
                download_ova_from_s3(friend_access_key, friend_secret_key, friend_s3_bucket, key, local_path)
            if flag:
                dec_data = en.decrypt_file(local_path,bytes.fromhex(dec_key))
                with open(os.path.splitext(key)[0]+".txt", 'wb') as file:
                    file.write(dec_data)

            st.success("Downloaded successfully")
            os.remove(local_path)
            # with st.spinner("Importin in Vertual Box is in progress..."):
            #     import_virtualbox_vm(vboxmanage_path,hh)
            # st.success("Imported Successfully")
    with tab1:
        # st.file_uploader("Upload Your VM Instance")
        loca_dir = r"C:\Users\dipes\Downloads\final capstron"
        # fake = r"C:\Users\dipes\Downloads\final capstron\mye.txt"
        real = list_virtualbox_vms(vboxmanage_path)
        vm_img = st.selectbox("Select-img",["Select"]+real)
        choice = st.checkbox("Encypt file")
        if choice:
            key_str = st.text_input("Enter key")
            en_key = bytes.fromhex(key_str)
        selected_vm_name = vm_img.split()[0].strip('"')
        ex_btn = st.button("Export")
        if ex_btn:
            with st.spinner("Exporting..."):
                ex_path = export_virtualbox_vm(vboxmanage_path,selected_vm_name,loca_dir)
            st.success("Expored SUccessfully")
            # upbtn = st.button("Upload in s3 Bucket")
            # if upbtn:
            #     with st.spinner("Please wait it may take several minute.."):
            if choice:
                    data = en.encrypt_file("test.txt",en_key)
                    path = os.path.join(r"C:\Users\dipes\Downloads\final capstron\temp","temp.enc")
                    file_name = "test.enc"
                    with open(path, 'wb') as file:
                        file.write(data)
            else:
                path = "test.txt"
                file_name = "test.txt"

            upload_file_to_s3(path,friend_s3_bucket,friend_access_key,friend_secret_key,file_name)
            st.success("Uploaded hey Congo...")
            os.remove(path)
if __name__ == "__main__":
    vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    friend_access_key, friend_secret_key, friend_s3_bucket, friend_vm_image_key = get_user_input()
    keys = fetch(friend_access_key,friend_secret_key,friend_s3_bucket)
    app(keys)
