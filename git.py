import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def get_git_logs(repo_url):
    try:
        logs = subprocess.check_output(['git', 'ls-remote', '--tags', '--heads', repo_url])
        logs = logs.decode('utf-8')
        commits = logs.split('\n')
        git_logs = []
        for commit in commits:
            if not commit:
                continue
            commit_hash = commit.split('\t')[0]
            git_log = subprocess.check_output(['git', 'show', '--name-status', '--format="%h","%an","%ad","%s"', commit_hash])
            git_logs.append(git_log.decode('utf-8'))
        return git_logs
    except subprocess.CalledProcessError as e:
        return str(e)

def fetch_logs():
    repo_url = url_entry.get()
    if not repo_url.endswith('.git'):
        repo_url += '.git'
    logs = get_git_logs(repo_url)
    if isinstance(logs, list):
        log_text.delete('1.0', tk.END)
        for log in logs:
            log_text.insert(tk.END, log + '\n')
        messagebox.showinfo("Success", "Git Logs fetched successfully.")
    else:
        messagebox.showerror("Error", f"Failed to fetch Git logs: {logs}")

def export_csv(filename):
    logs = log_text.get('1.0', tk.END)
    if not logs.strip():
        messagebox.showerror("Error", "No logs to export.")
        return
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Commit Hash", "Author", "Date", "Message"])
        writer.writerows(csv.reader(logs.splitlines()))

def export_xlsx(filename):
    logs = log_text.get('1.0', tk.END)
    if not logs.strip():
        messagebox.showerror("Error", "No logs to export.")
        return
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    row = 0
    for line in logs.splitlines():
        col = 0
        for value in line.split(','):
            worksheet.write(row, col, value.strip('"'))
            col += 1
        row += 1
    workbook.close()

def export_pdf(filename):
    logs = log_text.get('1.0', tk.END)
    if not logs.strip():
        messagebox.showerror("Error", "No logs to export.")
        return
    c = canvas.Canvas(filename, pagesize=letter)
    textobject = c.beginText(100, 750)
    textobject.setFont("Helvetica", 12)
    for line in logs.splitlines():
        textobject.textLine(line)
    c.drawText(textobject)
    c.save()

def export_logs(format_type):
    filename = filedialog.asksaveasfilename(defaultextension="." + format_type, filetypes=[(f"{format_type.upper()} files", f".{format_type.lower()}"), ("All Files", ".*")])
    if filename:
        if format_type == "csv":
            export_csv(filename)
        elif format_type == "xlsx":
            export_xlsx(filename)
        elif format_type == "pdf":
            export_pdf(filename)
        messagebox.showinfo("Success", f"Logs exported as {format_type.upper()} successfully.")

# Create the main window
root = tk.Tk()
root.title("Git Log Fetcher")

# Create and place widgets
url_label = tk.Label(root, text="Repository URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

fetch_button = tk.Button(root, text="Fetch Logs", command=fetch_logs)
fetch_button.pack()

export_frame = tk.Frame(root)
export_frame.pack()

export_buttons = [
    ("Export as CSV", "csv"),
    ("Export as XLSX", "xlsx"),
    ("Export as PDF", "pdf")
]

for text, format_type in export_buttons:
    button = tk.Button(export_frame, text=text, command=lambda f=format_type: export_logs(f))
    button.pack(side=tk.LEFT)

log_text = tk.Text(root, height=20, width=100)
log_text.pack()

# Start the event loop
root.mainloop()