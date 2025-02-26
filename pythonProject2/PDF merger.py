import os
import PyPDF2
from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, filedialog, ttk

# Function to merge PDFs
def merge_pdfs(pdf_files, output_path):
    try:
        pdf_merger = PyPDF2.PdfMerger()
        for pdf in pdf_files:
            pdf_merger.append(pdf)
        with open(output_path, 'wb') as output_pdf:
            pdf_merger.write(output_pdf)
        pdf_merger.close()
        messagebox.showinfo("Success", "PDFs merged successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")

# Function to split a PDF
def split_pdf(pdf_file, output_folder):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)
                output_path = os.path.join(output_folder, f"page_{i + 1}.pdf")
                with open(output_path, 'wb') as output_pdf:
                    writer.write(output_pdf)
        messagebox.showinfo("Success", "PDF split successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to split PDF: {e}")

# GUI Application
class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Custom font
        self.custom_font = ("Helvetica", 12)

        # Header
        self.header = Label(root, text="PDF Merge & Split Tool", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333333")
        self.header.pack(pady=20)

        # Drag and drop area
        self.drop_area = Label(root, text="Drag and drop PDF files here", font=self.custom_font, bg="#ffffff", relief="sunken", width=60, height=10)
        self.drop_area.pack(pady=20, padx=20)

        # Button frame
        self.button_frame = Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        # Merge button
        self.merge_button = Button(self.button_frame, text="Merge PDFs", font=self.custom_font, bg="#4CAF50", fg="white", command=self.merge_pdfs_gui)
        self.merge_button.pack(side=LEFT, padx=10, ipadx=10, ipady=5)

        # Split button
        self.split_button = Button(self.button_frame, text="Split PDF", font=self.custom_font, bg="#2196F3", fg="white", command=self.split_pdf_gui)
        self.split_button.pack(side=RIGHT, padx=10, ipadx=10, ipady=5)

        # Enable drag and drop
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        # Store dropped files
        self.pdf_files = []

    # Handle file drop
    def on_drop(self, event):
        self.pdf_files = event.data.strip().split()
        self.drop_area.config(text=f"{len(self.pdf_files)} file(s) dropped")

    # Merge PDFs GUI
    def merge_pdfs_gui(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "No files dropped!")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            merge_pdfs(self.pdf_files, output_path)

    # Split PDF GUI
    def split_pdf_gui(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "No files dropped!")
            return
        if len(self.pdf_files) > 1:
            messagebox.showwarning("Warning", "Please drop only one PDF to split!")
            return
        output_folder = filedialog.askdirectory()
        if output_folder:
            split_pdf(self.pdf_files[0], output_folder)

# Main function
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFToolApp(root)
    root.mainloop()