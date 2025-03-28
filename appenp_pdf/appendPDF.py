import PyPDF2
import os

def merge_pdfs(input_folder="tomerge", output_folder="merged", output_filename="IA_geral.pdf"):
    input_path = os.path.abspath(input_folder)
    output_path = os.path.abspath(output_folder)
    
    os.makedirs(output_path, exist_ok=True)
    
    pdf_files = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".pdf")])
    
    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta de origem.")
        return
    
    output_file = os.path.join(output_path, output_filename)
    
    with PyPDF2.PdfMerger() as merger:
        for pdf in pdf_files:
            merger.append(pdf)
        merger.write(output_file)
    
    print(f"Novo PDF criado com sucesso: {output_file}")

# Exemplo de uso
merge_pdfs()
